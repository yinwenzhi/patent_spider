import logging as log
import pickle
import os
import time
import shutil
import requests
import random
from abc import ABC, abstractmethod

class SpiderEngine(ABC):
    def __init__(self, config):
        # all in args
        self.timeout = config['timeout']
        self.url = config['url']
        self.ip_url = config['ip_url']
        self.spider_all = 0
        self.spider_success = 0
        self.pklfile = config['pklfile']

        with open(self.pklfile, 'rb') as f:
            self.results = pickle.load(f)

    def get_ip(self):
        # 这里使用西瓜代理池，www.xiguadaili.com，获取可用的IP地址
        i = random.randint(1, 3)
        time.sleep(i)
        ip_url = self.ip_url
        ip = requests.get(ip_url)
        ip_list = ip.text.splitlines()
        for each in ip_list:
            yield {"http": each}

    def get_html(self, applicant, ip=None, strSources='pip', pageNow=1):
        url = self.url
        timeout = self.timeout

        headers = {
            "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 70.0.3538.77 Safari / 537.36"
            # "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 70.0.3538.77 Safari / 537.36"
            }
        form_data = {"showType": 1,
                     "strSources": strSources,
                     "strWhere": "PA='%{}%'".format(applicant),
                     "numSortMethod": 4,
                     "strLicenseCode": "",
                     "numIp": 0,
                     "numIpc": "",
                     "numIg": 0,
                     "numIgc": "",
                     "numIgd": "",
                     "numUg": "",
                     "numUgc": "",
                     "numUgd": "",
                     "numDg": "",
                     "numDgc": "",
                     "pageSize": 3,
                     "pageNow": pageNow}

        html = requests.post(url=url, data=form_data, headers=headers, proxies=ip, timeout=timeout)
        return html

    @abstractmethod
    def start_spider(self):
        """ 
        This function start running the spider.
        """
        pass