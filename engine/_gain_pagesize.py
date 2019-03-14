import pickle
from bs4 import BeautifulSoup
import os
import time
import sys
import logging as log
from .engine import SpiderEngine
import random
import requests

class GainPageSize(SpiderEngine):
    def __init__(self, config):
        self.config = config
        # all in args

        self.trytimes = config['trytimes']
        self.strSources = config['strSources']
        self.start = config['start']
        self.end = config['end']

        super(GainPageSize, self).__init__(config)#调用父类的__init__函数load pickfile 并付给results

        self.end = len(self.results) if self.end == None or self.end > len(self.results) else self.end

    def start_spider(self):

        ip_gene = self.get_ip()
        flag = 0
        idx = self.start
        t1 = time.time()
        while idx < self.end:
            company = self.results[idx]['company']
            if self.results[idx]['page_size'] == 0:
                try:
                    ip = next(ip_gene)
                    # print(ip)
                    log.info(f" # {idx+1}-{flag+1}: 提取IP成功: {ip['http']}")
                except:
                    log.error(f"# {idx+1}-{flag+1}: 提取IP失败")                        
                    ip_gene = self.get_ip()
                    continue
                i = random.randint(1, 3)
                time.sleep(i)

                try:
                    html = self.get_html(applicant=company, ip=ip, strSources=self.strSources)
                except requests.exceptions.ProxyError as e:
                    log.error(f"# {idx+1}-{flag+1}: 连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败")
                    continue
                except requests.exceptions.ReadTimeout as e:
                    log.error(f"# {idx+1}-{flag+1}: ReadTimeout({self.timeout})")
                    continue
                except requests.exceptions.ConnectionError as e:
                    log.error(f"# {idx+1}-{flag+1}: Connection aborted")
                    continue
                except requests.exceptions.ChunkedEncodingError as e:
                    log.error(f"# {idx+1}-{flag+1}: Connection broken: IncompleteRead")
                    
                html.encoding = 'utf-8'
                soup = BeautifulSoup(html.text, 'lxml')
                # print(soup)
                try:
                    main_tb = soup.find("div", class_="next")
                    posion = main_tb.find('input')['onkeypress']
                    start = posion.find('zl_tz')+6
                    page_size = int(posion[start:-1])
                    self.results[idx]['page_size'] = page_size
                    
                except:
                    if soup.find("h1", class_="head_title") == None:
                        log.error(f"# {idx+1}-{flag+1}: 没有您要查询的结果")
                        flag+=1
                        if flag >= self.trytimes:
                            self.spider_all+=1
                            log.info(f' # {idx+1}-{flag}: {company} failed')
                            idx += 1
                            flag = 0
                            t2 = time.time()
                            log.info(f' # 耗时{round((t2-t1),1)}seconds, 成功爬取了{self.spider_success}/{self.spider_all}家公司\n')
                        continue
                    else:
                        log.error(f"# {idx+1}-{flag+1}: 被认为是机器人")  
                        continue
                log.info(f' # {idx+1}-{flag+1}: {company} success\n')
                
                flag = 0
                self.spider_success+=1
                self.spider_all+=1

                with open(self.pklfile, 'wb') as f:
                    pickle.dump(self.results, f)
                log.info(f" # {idx+1}-{flag+1}: 保存到文件")
                t2 = time.time()
                log.info(f' # 耗时{t2-t1}seconds, 成功爬取了{self.spider_success}/{self.spider_all}家公司\n')
                idx += 1
            else:
                log.info(f' # {idx+1}-{flag+1}: {company} has successed\n')
                idx += 1
                flag = 0

