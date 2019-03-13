import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os
import pickle
import time
import random
import sys



def get_ip():
    # 这里使用西瓜代理池，www.xiguadaili.com
    time.sleep(1)
    #i = random.randint(1, 3)
    #i = 2
    ip_url ='http://api3.xiguadaili.com/ip/?tid=557817999530467&num=1000'
    ip = requests.get(ip_url)
    ip_list = ip.text.splitlines()
    for each in ip_list:
        yield {"http": each}


def get_patent(patent_number, ip):
    url = "http://epub.sipo.gov.cn/patentoutline.action"
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 70.0.3538.77Safari / 537.36"
        }
    form_data = {"showType": 1,
                 "strSources": "",
                 "strWhere": "AN, DPR, IAN += '{}%' or ABH='{}'".format(patent_number.replace('.', ''), patent_number),
                 "numSortMethod": 4,
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
                 "pageNow": 1}

    html = requests.post(url, data=form_data, headers=headers, proxies=ip, timeout=30)
    return html

def get_content(html):
    soup = BeautifulSoup(html.text, 'lxml')
    main_tb = soup.find("div", class_="cp_linr")
    title = main_tb.h1.text.split("\xa0")[1]
    li_list = {' '.join(e.text.split()).split("：")[0]: ' '.join(e.text.split()).split("：")[1] for e in
               main_tb.find_all('li') if e.text.strip() != '' and len(' '.join(e.text.split()).split("：")) >= 2}
    abstract =main_tb.find("div", class_="cp_jsh").find_all('span')[1].text
    li_list['title'] = title
    li_list['abstract'] = abstract
    return li_list

def get_error_content(html):
    soup = BeautifulSoup(html.text, 'lxml')
    title = soup.title
    return title.text

def loop_get():
    with open('./patent_0118.pkl', 'rb') as rf:
        # 这里用的pickle，可以换成普通文件，这里是一个pandas的Dataframe
        patent = pickle.load(rf)
        ip_gene = get_ip()
    for i in range(patent.shape[0]):
        print(patent['tag'][i])

        #if type(patent['number'][i]) is not float and patent['tag'][i] == 0 and patent['tag_2'][i] == 0:
        if type(patent['number'][i]) is not float and patent['tag_2'][i] == "http_error":
            time.sleep(1)
            patent.loc[i, 'tag'] = 1
            try:
                try:
                    ip = next(ip_gene)
                except:
                    ip_gene = get_ip()
                    print("New IP")
                    ip = next(ip_gene)
                html = get_patent(patent['number'][i].strip(), ip)  # 获取网页
                with open("./html/%s.html" % patent['number'][i], 'wb') as wf:
                    wf.write(html.content)
                patent.loc[i, 'tag_2'] = 0
            except:
                print(patent.loc[i, 'number'], 'http-error', sys.exc_info()[1])
                patent.loc[i, 'tag_2'] = 'http_error'
                with open("./patent_0118.pkl", 'wb') as wf:
                    pickle.dump(patent, wf)
                continue
            try:
                result = get_content(html) # 解析内容
                print(patent['number'][i], result['申请号'])
                try:
                    patent.loc[i, '授权公告号'] = result['授权公告号']
                except:
                    pass
                try:
                    patent.loc[i, '申请公布号'] = result['申请公布号']
                except:
                    pass
                try:
                    patent.loc[i, '授权公告日'] = result['授权公告日']
                except:
                    pass
                try:
                    patent.loc[i, '申请公布日'] = result['申请公布日']
                except:
                    pass
                try:
                    patent.loc[i, '解密公告日'] = result['解密公告日']
                except:
                    pass
                try:
                    patent.loc[i, '申请号'] = result['申请号']
                except:
                    pass
                try:
                    patent.loc[i, '申请日'] = result['申请日']
                except:
                    pass
                try:
                    patent.loc[i, '申请人'] = result['申请人']
                except:
                    pass
                try:
                    patent.loc[i, '专利权人'] = result['专利权人']
                except:
                    pass
                try:
                    patent.loc[i, '发明人'] = result['发明人']  
                except:
                    pass
                try:
                    patent.loc[i, '地址'] = result['地址']
                except:
                    pass
                try:
                    patent.loc[i, '分类号'] = result['分类号']
                except:
                    pass
                try:
                    patent.loc[i, 'title'] = result['title']
                except:
                    pass
                try:
                    patent.loc[i, 'abstract'] = result['abstract']
                except:
                    pass
                
                patent.loc[i, 'tag'] = 1
            except:
                try:
                    result = get_error_content(html)
                except:
                    result = 'error'
                print(patent.loc[i, 'number'], result)
                patent.loc[i, 'tag_2'] = result
            with open("./patent_0118.pkl", 'wb') as wf:
                pickle.dump(patent, wf)
        else:
            patent.loc[i, 'tag'] = 1
    with open("./patent_0118.pkl", 'wb') as wf:
        pickle.dump(patent, wf)
    print("over!")



if __name__ == "__main__":
    #patent_number = "200710082558.9"
    #html = get_patent(patent_number)
    #print(html.text)
    #with open("./html/%s.html" % patent_number, 'wb') as wf:
    #    wf.write(html.content)
    #result = get_content(html)
    #print(result)
    loop_get()
