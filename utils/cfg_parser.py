import yaml
import os

def parse(fp):
    with open(fp, 'r') as fd:
        cont = fd.read()
        y = yaml.load(cont)
        return y
#从yaml文件读取配置信息到config
def getConfig(cfgs_root, patent_class):
    cfg_fp = './' + cfgs_root + '/' + patent_class + '.yml'
    config =  parse(cfg_fp)
    return config