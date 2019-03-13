import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os
import pickle
import time
import random
import sys



def get_content(html):
    soup = BeautifulSoup(html.text, 'lxml')
    print(soup)
    main_tbs = soup.find_all("div", class_="cp_linr")
    for main_tb in main_tbs:
        title = main_tb.h1.text.split("\xa0")[1]
        li_list = {' '.join(e.text.split()).split("：")[0]: ' '.join(e.text.split()).split("：")[1] for e in
                   main_tb.find_all('li') if e.text.strip() != '' and len(' '.join(e.text.split()).split("：")) >= 2}
        abstract =main_tb.find("div", class_="cp_jsh").find_all('span')[1].text
        li_list['title'] = title
        li_list['abstract'] = abstract
        print(li_list)
        print("**************************************************************")



def get_error_content(html):
    soup = BeautifulSoup(html.text, 'lxml')
    title = soup.title
    return title.text

def loop_get():
    with open('./patent.pkl', 'rb') as rf:
        # 这里用的pickle，可以换成普通文件，这里是一个pandas的Dataframe
        patent = pickle.load(rf)
        ip_gene = get_ip()
    for i in range(patent.shape[0]):
        print(patent['tag'][i])

        #if type(patent['applicant'][i]) is not float and patent['tag'][i] == 0 and patent['tag_2'][i] == 0:
        if type(patent['applicant'][i]) is not float and patent['tag_2'][i] == "http_error":
            time.sleep(1)
            patent.loc[i, 'tag'] = 1
            try:
                try:
                    # 直接获取IP
                    ip = next(ip_gene)
                except:
                    # 尝试获取新IP
                    ip_gene = get_ip()
                    print("New IP")
                    ip = next(ip_gene)
                html = get_patent(patent['applicant'][i].strip(), ip)  # 获取网页
                with open("./html/%s.html" % patent['applicant'][i], 'wb') as wf:
                    wf.write(html.content)
                patent.loc[i, 'tag_2'] = 0
            except:
                print(patent.loc[i, 'applicant'], 'http-error', sys.exc_info()[1])
                patent.loc[i, 'tag_2'] = 'http_error'
                with open("./patent.pkl", 'wb') as wf:
                    pickle.dump(patent, wf)
                continue
            try:
                result = get_content(html) # 解析内容
                print(patent['applicant'][i], result['申请号'])
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
                print(patent.loc[i, 'applicant'], result)
                patent.loc[i, 'tag_2'] = result
            with open("./patent.pkl", 'wb') as wf:
                pickle.dump(patent, wf)
        else:
            patent.loc[i, 'tag'] = 1
    with open("./patent.pkl", 'wb') as wf:
        pickle.dump(patent, wf)
    print("over!")



if __name__ == "__main__":
    ip_gene = get_ip()
    # loop_get()
    try:
        # 直接获取IP
        ip = next(ip_gene)
    except:
        # 尝试获取新IP
        ip_gene = get_ip()
        print("New IP")
        ip = next(ip_gene)
    html = get_patent(ip)
    # html = get_patent()
    get_content(html)