import xlrd
import pickle
import os
from tqdm import tqdm

# 根据公司名列表初始化一个新的pklfile, 每个公司的第一个专利设置为空列表
def new_companys_pkl(pklfile, companys):
    with open(pklfile, 'wb') as f:
        results = []
        for company in tqdm(companys):
            result = {}
            company = company.strip()
            result['company'] = company
            result['page_size'] = 0
            result['patent'] = {}
            result['patent'][1] = []
            results.append(result)

        pickle.dump(results, f)

# 根据pagesize追加公司专利字典, 并删除pagesize为0的条目
def filter_companys_pkl(pklfile, pklfile_filter):
    with open(pklfile, 'rb') as f:
        results = pickle.load(f)
        for result in tqdm(results):
            if result['page_size'] == 0:
                results.remove(result)
            elif result['page_size'] == 1:
                contine
            else:
                for page in range(2,result['page_size']+1):
                    result['patent'][page] = []
    with open(pklfile_filter, 'wb') as f:
        pklfile_filter.dump(results, f)

# 计算pklfile文件中包含专利的公司数和页数
def count(pklfile):
    company_num = 0
    page_num = 0
    with open(pklfile, 'rb') as f:
        results = pickle.load(f)
    for result in results:
        if result['page_size'] != 0:
            company_num += 1
            page_num += result['page_size']
    print(f'共有{company_num}/{len(results)}家公司存在专利, 共有{page_num}页专利信息')

# 切分pklfile为三等份
def split_pkl(pklfile, pklfile_1, pklfile_2, pklfile_3):
    with open(pklfile, 'rb') as f:
        results = pickle.load(f)
        one_third = len(results) // 3
        results_1 = results[:one_third]
        results_2 = results[one_third:one_third*2]
        results_3 = results[one_third*2:]
        with open(pklfile_1, 'wb') as f:
            pickle.dump(results_1, f)
        with open(pklfile_2, 'wb') as f:
            pickle.dump(results_2, f)
        with open(pklfile_3, 'wb') as f:
            pickle.dump(results_3, f)

# 合并三份pklfile为一
def concentrate_pkl(pklfile, pklfile_1, pklfile_2, pklfile_3):
    results=[]
    with open(pklfile_1, 'rb') as f:
        results_1 = pickle.load(f)
    with open(pklfile_2, 'rb') as f:
        results_2 = pickle.load(f)
    with open(pklfile_3, 'rb') as f:
        results_3 = pickle.load(f)
    results.extend(results_1)
    results.extend(results_2)
    results.extend(results_3)
    with open(pklfile, 'wb') as f:
        pickle.dump(results, f)

def main():
    excelfile='C:\\Files\\Documents\\apollo项目组\\国防科工局成果转化目录\\海淀区的企业名称.xlsx'
    patent_class = 'publish'
    # patent_class = 'authorization'

    pklfile = 'results\\' + patent_class + '\\' + patent_class + '.pkl'
    pklfile_1 = 'results\\' + patent_class + '\\' + patent_class + '_1.pkl'
    pklfile_2 = 'results\\' + patent_class + '\\' + patent_class + '_2.pkl'
    pklfile_3 = 'results\\' + patent_class + '\\' + patent_class + '_3.pkl'

    pklfile_filter = 'results\\' + patent_class + '\\' + patent_class + '_filter.pkl'
    pklfile_filter_1 = 'results\\' + patent_class + '\\' + patent_class + '_filter_1.pkl'
    pklfile_filter_2 = 'results\\' + patent_class + '\\' + patent_class + '_filter_2.pkl'
    pklfile_filter_3 = 'results\\' + patent_class + '\\' + patent_class + '_filter_3.pkl'

    # create a new pkl file
    # wb = xlrd.open_workbook(excelfile)
    # sheet = wb.sheet_by_name('Sheet1')
    # companys = sheet.col_values(0)[1:8672]
    # new_companys_pkl(pklfile, companys)

    # count(pklfile)
    # count(pklfile_1)
    count(pklfile_2)
    # count(pklfile_3)
    # split_pkl(pklfile, pklfile_1, pklfile_2, pklfile_3)
    # concentrate_pkl(pklfile, pklfile_1, pklfile_2, pklfile_3)

if __name__ == "__main__":
    main()
