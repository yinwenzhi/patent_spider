import sys
import os
import copy
from datetime import datetime
import logging
import random
import numpy as np

# individual packages
from .fileproc import safeMakeDirs
from .cfg_parser import getConfig

def setLogging(log_dir, stdout_flag):
    safeMakeDirs(log_dir)
    dt = datetime.now()
    log_name = dt.strftime('%Y-%m-%d_time_%H_%M_%S') + '.log'

    log_fp = os.path.join(log_dir, log_name)
    #print os.path.abspath(log_fp)

    if stdout_flag:
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)
    else:
        logging.basicConfig(filename=log_fp, format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)



def initEnv(patent_class):
    cfgs_root = 'cfgs'
    cur_cfg = getConfig(cfgs_root, patent_class)

    results_dir = os.path.join(cur_cfg['results_dir'], patent_class)
    logs_dir = os.path.join(cur_cfg['logs_dir'], patent_class)

    url = cur_cfg['url']
    ip_url = cur_cfg['ip_url']
    timeout = cur_cfg['timeout']
    stdout_flag = cur_cfg['stdout']
    pklfile = cur_cfg['pklfile']
    trytimes = cur_cfg['trytimes']
    setLogging(logs_dir, stdout_flag)

    return cur_cfg

if __name__ == '__main__':
    pass
