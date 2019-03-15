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

        super(GainContent, self).__init__(config)

        self.end = len(self.results) if self.end == None or self.end > len(self.results) else self.end

    def start_spider(self):

        ip_gene = self.get_ip()
        idx = self.start
        t1 = time.time()
        while idx < self.end:
            flag = 0
            company = self.results[idx]['company']
            page_size = self.results[idx]['page_size']
            if page_size == 1:
                idx += 1
                continue
            for pagenow in range(2, page_size+1):
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
                    except requests.exceptions.ContentDecodingError as e:
                        log.error(f"# {idx+1}-{flag+1}: Received response with content-encoding: gzip, but failed to decode it.")
                        continue                        
                    html.encoding = 'utf-8'
                    soup = BeautifulSoup(html.text, 'lxml')
                    # print(soup)
                    try:
                        self.results[idx]['patent'][1] = self.prase_page_cp_boxes(soup)
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


