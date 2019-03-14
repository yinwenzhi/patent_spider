import pickle
from bs4 import BeautifulSoup
import os
import time
import sys
import logging as log
from .engine import SpiderEngine
import random
import requests

class GainContent(SpiderEngine):
    def __init__(self, config):
        self.config = config
        # all in args

        self.trytimes = config['trytimes']
        self.strSources = config['strSources']
        self.start = config['start']
        self.end = config['end']

        super(GainContent, self).__init__(config)#调用父类的__init__函数load pickfile 并付给results

        self.end = len(self.results) if self.end == None or self.end > len(self.results) else self.end

    def prase_cp_box(self,cp_box):
        print("**********************") 
        title = cp_box.h1.text.split("\xa0")[1]
        li_list = {' '.join(e.text.split()).split("：")[0]: ' '.join(e.text.split()).split("：")[1] for e in
                cp_box.find_all('li') if e.text.strip() != '' and len(' '.join(e.text.split()).split("：")) >= 2}
        li_list['tile']= title
        abstract =cp_box.find("div", class_="cp_jsh").find_all('span')[1].text
        li_list['abstract'] = abstract
        return li_list
    
    def prase_page_cp_boxes(self,soup):
        
        cp_boxes_text = soup.findAll("div", class_="cp_box")
        result_page_contents = []
        for cp_box in cp_boxes_text:
                
                #print(cp_box)
                result_content = self.prase_cp_box(cp_box)
                print(result_content)
                result_page_contents.append(result_content)
        return result_page_contents

    def start_spider(self):

        ip_gene = self.get_ip()
        idx = self.start
        t1 = time.time()
        while idx < self.end:
            flag = 0
            company = self.results[idx]['company']
            page_size = self.results[idx]['page_size']
            for pagenow in range(page_size):
                pagenow += 1
                if self.results[idx]['patent'][pagenow] == []:
                    try:
                        ip = next(ip_gene)
                        # print(ip)
                        log.info(f" # {idx+1}-{pagenow}-{flag+1}: 提取IP成功: {ip['http']}")
                    except:
                        log.error(f"# {idx+1}-{pagenow}-{flag+1}: 提取IP失败")                        
                        ip_gene = self.get_ip()
                        continue
                    i = random.randint(1, 3)
                    time.sleep(i)

                    try:
                        html = self.get_html(applicant=company, ip=ip, strSources=self.strSources,pageNow=pagenow)
                    except requests.exceptions.ProxyError as e:
                        log.error(f"# {idx+1}-{pagenow}-{flag+1}: 连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败")
                        continue
                    except requests.exceptions.ReadTimeout as e:
                        log.error(f"# {idx+1}-{pagenow}-{flag+1}: ReadTimeout({self.timeout})")
                        continue
                    except requests.exceptions.ConnectionError as e:
                        log.error(f"# {idx+1}-{pagenow}-{flag+1}: Connection aborted")
                        continue
                    except requests.exceptions.ChunkedEncodingError as e:
                        log.error(f"# {idx+1}-{pagenow}-{flag+1}: Connection broken: IncompleteRead")
                        continue
                    html.encoding = 'utf-8'
                    soup = BeautifulSoup(html.text, 'lxml')
                    # print(soup)
                    try:
                        result_page_contents = self.prase_page_cp_boxes(soup)
                        self.results[idx]['patent'][pagenow] = result_page_contents
                    except:
                        if soup.find("h1", class_="head_title") == None:
                            log.error(f"# {idx+1}-{pagenow}-{flag+1}: 没有您要查询的结果")
                            flag += 1
                            if flag >= self.trytimes:
                                self.spider_all+=1
                                log.info(f' # {idx+1}-{pagenow}-{flag}: {company} failed')
                                flag = 0
                                t2 = time.time()
                                log.info(f' # 耗时{round((t2-t1),1)}seconds, 成功爬取了{self.spider_success}/{self.spider_all}张页面\n')
                                if pagenow == page_size:
                                    idx += 1
                                    break
                            continue
                        else:
                            log.error(f"# {idx+1}-{pagenow}-{flag+1}: 被认为是机器人")  
                            continue
                    log.info(f' # {idx+1}-{pagenow}-{flag+1}: {company} success\n')

                    self.spider_success += 1
                    self.spider_all += 1
                    with open(self.pklfile, 'wb') as f:
                        pickle.dump(self.results, f)
                    log.info(f" # {idx+1}-{pagenow}-{flag+1}: 保存到文件")
                    t2 = time.time()
                    log.info(f' # 耗时{t2-t1}seconds, 成功爬取了{self.spider_success}/{self.spider_all}家公司\n')
                    flag = 0
                    if pagenow == page_size:
                        idx += 1
                        break
                else:
                    log.info(f' # {idx+1}-{pagenow}-{flag+1}: {company} has successed\n')
                    flag = 0
                    if pagenow == page_size:
                        idx += 1
                        break      


