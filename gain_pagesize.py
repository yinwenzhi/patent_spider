from utils.envs import initEnv
import argparse
import logging as log
from pprint import pformat
from engine._gain_pagesize import GainPageSize
import time

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='patent spider: an excellent spider program')
    parser.add_argument('patent_class', help='patent class', default=None, choices=['publish','authorization'])
    args = parser.parse_args()

    config = initEnv(patent_class=args.patent_class)

    log.info('config\n\n%s\n' % pformat(config))

    eng = GainPageSize(config)

    # run eng

    eng.start_spider()

