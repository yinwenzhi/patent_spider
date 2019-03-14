import pickle
from bs4 import BeautifulSoup
import os
import time
import sys
import logging as log
import random
import requests
import argparse

from utils.envs import initEnv
from engine._gain_content import GainContent

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='patent spider: an viewer of company by idx')
    parser.add_argument('--patent_class', help='patent class', default=None)
    parser.add_argument('--idxnum', help='please input idx number', default=None)
    args = parser.parse_args()

    config = initEnv(patent_class=args.patent_class)
    pklfilepath = config['pklfile']
    idx = int(args.idxnum)


    #fiel = super(GainContent, self).__init__(config)#调用父类的__init__函数load pickfile 并付给results
    with open(pklfilepath, 'rb') as f:
        results = pickle.load(f)
    
    for i in range(100):
        view = results[i]['patent']
        if view != {}:
            print(i)
            print(view)




