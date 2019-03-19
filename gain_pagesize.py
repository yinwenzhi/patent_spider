import argparse
import logging as log
from pprint import pformat
import sys
import time

sys.path.insert(0, '.')
from engine._gain_pagesize import GainPageSize
from utils.envs import initEnv



if __name__ == '__main__':

    #parser解析命令行参数
    parser = argparse.ArgumentParser(description='patent spider: an excellent spider program')
    parser.add_argument('patent_class', help='patent class', default=None, choices=['publish','authorization','utility_model','design'])
    args = parser.parse_args()
    #initEnv接受的参数就是paent_class对应的参数值
    config = initEnv(patent_class=args.patent_class) 
    #打印配置信息到日志
    log.info('config\n\n%s\n' % pformat(config))

    eng = GainPageSize(config)

    # run eng
    eng.start_spider()

