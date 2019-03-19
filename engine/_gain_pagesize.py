import pickle
from bs4 import BeautifulSoup
import os
import time
import sys
import logging as log
from . import engine
import random
import requests
from utils.time_conversion import secondstohour, countlasttime

class GainPageSize(engine.SpiderEngine):
    def __init__(self, config):
        self.config = config
        # all in args

        self.trytimes = config['trytimes']
        self.strSources = config['strSources']
        self.start = config['start']
        self.end = config['end']

        super(GainPageSize, self).__init__(config)

        self.end = len(self.results) if self.end == None or self.end > len(self.results) else self.end

        self.spider_hassuccessed = 0
        for result in self.results[self.start:self.end]:
            if result['page_size'] != 0:
                self.spider_hassuccessed += 1

    def start_spider(self):

        ip_gene = self.get_ip()
        flag = 0
        pagenow = 1
        idx = self.start
        t1 = time.time()
        ipNeedChange = True

        while idx < self.end:
            company = self.results[idx]['company']
            if self.results[idx]['page_size'] == 0:
                if ipNeedChange:
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

                html = self.get_html(idx, flag, applicant=company, ip=ip, strSources=self.strSources, pagenow=pagenow)
                if html == False:
                    ipNeedChange = True
                    flag = 0
                    continue

                html.encoding = 'utf-8'
                soup = BeautifulSoup(html.text, 'lxml')
                # print(soup)
                try:
                    main_tb = soup.find("div", class_="next")
                    posion = main_tb.find('input')['onkeypress']
                    start = posion.find('zl_tz')+6
                    page_size = int(posion[start:-1])
                    self.results[idx]['page_size'] = page_size
                    self.results[idx]['patent'][1] = self.prase_page_cp_boxes(soup)
                except :
                    if soup.find("h1", class_="head_title") == None:
                        log.error(f"# {idx+1}-{pagenow}-{flag+1}: 没有您要查询的结果: {company} {ip['http']}")
                        ipNeedChange = False
                        flag+=1
                        if flag >= self.trytimes:
                            self.spider_all+=1
                            log.info(f' # {idx+1}-{pagenow}-{flag}: {company} failed\n')
                            idx += 1
                            flag = 0
                            t2 = time.time()
                            lasttime = countlasttime((t2-t1), self.spider_all, self.spider_hassuccessed, self.end-self.start)
                            log.info(f' # 耗时{secondstohour(t2-t1)}, 成功爬取了{self.spider_success}/{self.spider_all}家公司, 预计剩余{lasttime}\n')
                            ipNeedChange = True
                        continue
                    else:
                        log.error(f"# {idx+1}-{pagenow}-{flag+1}: 被认为是机器人")
                        ipNeedChange = True
                        continue

                log.info(f' # {idx+1}-{pagenow}-{flag+1}: {company} success\n')
                ipNeedChange = True
                self.spider_success+=1
                self.spider_all+=1

                with open(self.pklfile, 'wb') as f:
                    pickle.dump(self.results, f)
                log.info(f" # {idx+1}-{pagenow}-{flag+1}: 保存到文件")

                t2 = time.time()
                lasttime = countlasttime((t2-t1), self.spider_all, self.spider_hassuccessed, self.end-self.start)
                log.info(f' # 耗时{secondstohour(t2-t1)}, 成功爬取了{self.spider_success}/{self.spider_all}家公司, 预计剩余{lasttime}\n')

                idx += 1
                flag = 0
            else:
                log.info(f' # {idx+1}-{pagenow}-{flag+1}: {company} has successed\n')
                idx += 1
                flag = 0


