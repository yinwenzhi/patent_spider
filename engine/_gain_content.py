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
from utils.change_color import red, green, yellow

class GainContent(engine.SpiderEngine):
    def __init__(self, config):
        self.config = config
        # all in args

        self.trytimes = config['trytimes']
        self.strSources = config['strSources']
        self.start = config['start']
        self.end = config['end']

        super(GainContent, self).__init__(config)

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
                                log.info(' # {}-{}-{}: {} {}\n'.format(idx+1, pagenow, flag, company, red('failed')))

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
                    log.info(' # {}-{}-{}: {}, {} 保存到文件 {}\n'.format(idx+1, pagenow, flag+1, company, green('success'), ip['http']))
                    
                    self.spider_success += 1
                    self.spider_all += 1

                    with open(self.pklfile, 'wb') as f:
                        pickle.dump(self.results, f)

                    t2 = time.time()
                    lasttime = countlasttime((t2-t1), self.spider_all, self.spider_hassuccessed, self.pages_all)
                    log.info(f' # 耗时{secondstohour(t2-t1)}, 成功爬取了{self.spider_success}/{self.spider_all}张页面, 预计剩余{lasttime}\n')

                    ipNeedChange = True
                    flag = 0
                    if pagenow == page_size:
                        idx += 1
                        break
                else:
                    log.info(' # {}-{}-{}: {} {}\n'.format(idx+1, pagenow, flag+1, company, yellow('has successed')))
                    flag = 0
                    if pagenow == page_size:
                        idx += 1
                        break


