from utils.envs import initEnv
import argparse
import logging as log
from pprint import pformat
from engine._gain_pagesize import GainPageSize
import time

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='patent spider: an excellent spider program')
    parser.add_argument('patent_class', help='patent class', default=None)
    args = parser.parse_args()

    config = initEnv(patent_class=args.patent_class)

    log.info('config\n\n%s\n' % pformat(config))

    eng = GainPageSize(config)

    # run eng
    t1 = time.time()
    eng.start_spider()
    t2 = time.time()
    log.info(f'\n耗时{t2-t1}seconds, 成功爬取了{eng.spider_success}/{eng.spider_all}家公司 ]')
