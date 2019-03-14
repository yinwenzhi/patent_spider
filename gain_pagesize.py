from utils.envs import initEnv
import argparse
import logging as log
from pprint import pformat
from engine._gain_pagesize import GainPageSize
import time

if __name__ == '__main__':

    #parser解析命令行参数
    parser = argparse.ArgumentParser(description='patent spider: an excellent spider program')
    parser.add_argument('patent_class', help='patent class', default=None, choices=['publish','authorization'])
    args = parser.parse_args()
    #initEnv接受的参数就是paent_class对应的参数值
    config = initEnv(patent_class=args.patent_class) 
    #打印配置信息到日志
    log.info('config\n\n%s\n' % pformat(config))

    eng = GainPageSize(config)

    # run eng

    eng.start_spider()

