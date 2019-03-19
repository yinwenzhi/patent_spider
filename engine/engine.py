import logging as log
import pickle
import os
import time
import shutil
import requests
import random
from abc import ABC, abstractmethod
#abc模块是一个基类，继承于 abc基类的子类中的方法带有@abstractmethod的方法在使用时必须自定义实现

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

    def get_html(self, idx, flag, applicant, ip=None, strSources='pip', pagenow=1):
        url = self.url
        timeout = self.timeout

        headers = {
            "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 70.0.3538.77 Safari / 537.36"
            # "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 70.0.3538.77 Safari / 537.36"
            }
        form_data = {"showType": 1,
                     "strSources": strSources,
                     "strWhere": "PA='%{}%'".format(applicant),
                     "numSortMethod": "",
                     "strLicenseCode": "",
                     "numIp": "",
                     "numIpc": "",
                     "numIg": "",
                     "numIgc": "",
                     "numIgd": "",
                     "numUg": "",
                     "numUgc": "",
                     "numUgd": "",
                     "numDg": "",
                     "numDgc": "",
                     "pageSize": 3,
                     "pageNow": pagenow}
        try:
            html = requests.post(url=url, data=form_data, headers=headers, proxies=ip, timeout=timeout)
        except requests.exceptions.ProxyError as e:
            log.error(f"# {idx+1}-{pagenow}-{flag+1}: 连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败")
            return False
        except requests.exceptions.ReadTimeout as e:
            log.error(f"# {idx+1}-{pagenow}-{flag+1}: ReadTimeout({self.timeout})")
            return False
        except requests.exceptions.ConnectionError as e:
            log.error(f"# {idx+1}-{pagenow}-{flag+1}: Connection aborted")
            return False
        except requests.exceptions.ChunkedEncodingError as e:
            log.error(f"# {idx+1}-{pagenow}-{flag+1}: Connection broken: IncompleteRead")
            return False
        except requests.exceptions.ContentDecodingError as e:
            log.error(f"# {idx+1}-{flag+1}: Received response with content-encoding: gzip, but failed to decode it.")
            return False
        except requests.exceptions.TooManyRedirects as e:
            log.error(f"# {idx+1}-{flag+1}: e")
            return False
        return html

    def prase_cp_box(self, cp_box):
        # print("**********************")
        title = cp_box.h1.text.split("\xa0")[1]
        li_list = {' '.join(e.text.split()).split("：")[0]: ' '.join(e.text.split()).split("：")[1] for e in
                cp_box.find_all('li') if e.text.strip() != '' and len(' '.join(e.text.split()).split("：")) >= 2}
        li_list['tile']= title
        abstract =cp_box.find("div", class_="cp_jsh").find_all('span')[1].text
        li_list['abstract'] = abstract
        return li_list

    def prase_page_cp_boxes(self, soup):
        cp_boxes_text = soup.findAll("div", class_="cp_box")
        result_page_contents = []
        for cp_box in cp_boxes_text:
            #print(cp_box)
            result_content = self.prase_cp_box(cp_box)
            # print(result_content)
            result_page_contents.append(result_content)
        return result_page_contents

    @abstractmethod
    def start_spider(self):
        """
        This function start running the spider.
        """
        pass