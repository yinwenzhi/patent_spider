import pickle
from bs4 import BeautifulSoup
import os
import time
import sys
import logging as log
from .engine import SpiderEngine
import random
import requests
from . import engine
import random
import reques
from utils.time_conversion import secondstohour, countlasttimets

class GainContent(engine.SpiderEngine):
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
        result_contents = []
        for cp_box in cp_boxes_text:
                
                #print(cp_box)
                result_content = self.prase_cp_box(cp_box)
                print(result_content)
                result_contents.append(result_content)
        return result_contents

    def prase_pages(self,html):
        try:
            #print("kaishibs4soup")
            result_contents=self.prase_page_cp_boxes(html)
        
        except ValueError as e:
            print(e)




        self.end = len(self.results) if self.end == None or self.end > len(self.results) else self.end

        self.spider_hassuccessed = 0
        self.pages_all = 0
        for result in self.results[self.start:self.end]:
            page_size = result['page_size']
            for pagenow in range(2, page_size+1):
                self.pages_all += 1
                if result['patent'][pagenow] != []:
                    self.spider_hassuccessed += 1

    def start_spider(self):

        ip_gene = self.get_ip()
        # flag = 0
        # idx = self.start
        # t1 = time.time()
        # while idx < self.end:
        #     company = self.results[idx]['company']
        #     # if self.results[idx]['page_size'] == 0:
        #     pagenow = 1
        #     while True:
        #             #if self.results[idx]['patent'][pagenow] == []:
        #             if not pagenow in self.results[idx]['patent']:
        idx = self.start
        t1 = time.time()
        ipNeedChange = True

        while idx < self.end:
            flag = 0
            company = self.results[idx]['company']
            page_size = self.results[idx]['page_size']
            if page_size == 1:
                idx += 1
                continue
            for pagenow in range(2, page_size+1):
                if self.results[idx]['patent'][pagenow] == []:
                    if ipNeedChange:
                        try:
                            ip = next(ip_gene)
                            # print(ip)
                            log.info(f" # {idx+1}-{pagenow}-{flag+1}: 提取IP成功: {ip['http']}")
                        except:
#<editor-fold desc="y原始代码">
                    #         log.error(f"# {idx+1}-{pagenow}-{flag+1}: 提取IP失败")                        
                    #         ip_gene = self.get_ip()
                    #         continue
                    #     i = random.randint(1, 3)
                    #     time.sleep(i)

                    #     try:
                    #         html = self.get_html(applicant=company, ip=ip, strSources=self.strSources,pageNow=pagenow)
                    #     except requests.exceptions.ProxyError as e:
                    #         log.error(f"# {idx+1}-{pagenow}-{flag+1}: 连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败")
                    #         continue
                    #     except requests.exceptions.ReadTimeout as e:
                    #         log.error(f"# {idx+1}-{pagenow}-{flag+1}: ReadTimeout({self.timeout})")
                    #         continue
                    #     except requests.exceptions.ConnectionError as e:
                    #         log.error(f"# {idx+1}-{pagenow}-{flag+1}: Connection aborted")
                    #         continue
                    #     except requests.exceptions.ChunkedEncodingError as e:
                    #         log.error(f"# {idx+1}-{pagenow}-{flag+1}: Connection broken: IncompleteRead")
                    #         continue
                    #     html.encoding = 'utf-8'
                    #     soup = BeautifulSoup(html.text, 'lxml')
                    #     # print(soup)
                    #     try:
                    #         main_tb = soup.find("div", class_="next")
                    #         posion = main_tb.find('input')['onkeypress']
                    #         start = posion.find('zl_tz')+6
                    #         page_size = int(posion[start:-1])
                    #         self.results[idx]['page_size'] = page_size
                            
                    #     except:
                    #         if soup.find("h1", class_="head_title") == None:
                    #             log.error(f"# {idx+1}-{pagenow}-{flag+1}: 没有您要查询的结果")
                    #             flag+=1
                    #             if flag >= self.trytimes:
                    #                 self.spider_all+=1
                    #                 log.info(f' # {idx+1}-{pagenow}-{flag}: {company} failed')
                    #                 idx += 1
                    #                 flag = 0
                    #                 t2 = time.time()
                    #                 log.info(f' # 耗时{round((t2-t1),1)}seconds, 成功爬取了{self.spider_success}/{self.spider_all}家公司\n')
                    #                 #wy break;
                    #                 if pagenow == 1:
                    #                     break
                    #                 pagenow += 1
                    #             continue
                    #         else:
                    #             log.error(f"# {idx+1}-{pagenow}-{flag+1}: 被认为是机器人")  
                    #             continue

                    #     result_page_contents=self.prase_page_cp_boxes(soup)
                    #     self.results[idx]['patent'][pagenow]=result_page_contents
                    #     log.info(f' # {idx+1}-{pagenow}-{flag+1}: {company} success\n')
                        
                    #     flag = 0
                    #     self.spider_success+=1
                    #     self.spider_all+=1

                    #     with open(self.pklfile, 'wb') as f:
                    #         pickle.dump(self.results, f)
                    #     log.info(f" # {idx+1}-{pagenow}-{flag+1}: 保存到文件")
                    #     t2 = time.time()
                    #     log.info(f' # 耗时{t2-t1}seconds, 成功爬取了{self.spider_success}/{self.spider_all}家公司\n')
                    #     pagenow += 1
                    #     if pagenow == page_size:
                    #         idx+=1
                    #         break
                    # else:
                    #     log.info(f' # {idx+1}-{pagenow}-{flag+1}: {company} has successed\n')
                    #     flag = 0
                    #     pagenow += 1
                    #     page_size = self.results[idx]['page_size']
                    #     if pagenow == page_size:
                    #         idx+=1
                    #         break  
#</editor-fold>    
                            log.error(f"# {idx+1}-{pagenow}-{flag+1}: 提取IP失败")
                            ip_gene = self.get_ip()
                            continue

                    i = random.randint(1, 3)
                    time.sleep(i)

                    html = self.get_html(idx, flag, applicant=company, ip=ip, strSources=self.strSources, pagenow=pagenow)
                    if html == False:
                        ipNeedChange = True
                        flag = 0
                        continue

                    html.encoding = 'utf-8'
                    soup = BeautifulSoup(html.text, 'lxml')
                    # print(soup)
                    try:
                        self.results[idx]['patent'][1] = self.prase_page_cp_boxes(soup)
                    except:
                        if soup.find("h1", class_="head_title") == None:
                            log.error(f"# {idx+1}-{pagenow}-{flag+1}: 没有您要查询的结果")
                            ipNeedChange = False
                            flag += 1
                            if flag >= self.trytimes:
                                self.spider_all+=1
                                log.info(f' # {idx+1}-{pagenow}-{flag}: {company} failed')
                                flag = 0
                                t2 = time.time()
                                lasttime = countlasttime((t2-t1), self.spider_all, self.spider_hassuccessed, self.pages_all)
                                log.info(f' # 耗时{secondstohour(t2-t1)}, 成功爬取了{self.spider_success}/{self.spider_all}张页面, 预计剩余{lasttime}\n')
                                ipNeedChange = True
                                if pagenow == page_size:
                                    idx += 1
                                    break
                            continue
                        else:
                            log.error(f"# {idx+1}-{pagenow}-{flag+1}: 被认为是机器人")
                            ipNeedChange = True
                            continue
                    log.info(f' # {idx+1}-{pagenow}-{flag+1}: {company} success\n')
                    ipNeedChange = True
                    self.spider_success += 1
                    self.spider_all += 1
                    with open(self.pklfile, 'wb') as f:
                        pickle.dump(self.results, f)
                    log.info(f" # {idx+1}-{pagenow}-{flag+1}: 保存到文件")
                    t2 = time.time()
                    lasttime = countlasttime((t2-t1), self.spider_all, self.spider_hassuccessed, self.pages_all)
                    log.info(f' # 耗时{secondstohour(t2-t1)}, 成功爬取了{self.spider_success}/{self.spider_all}张页面, 预计剩余{lasttime}\n')
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


