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
                continue
            else:
                for page in range(2,result['page_size']+1):
                    result['patent'][page] = []
    with open(pklfile_filter, 'wb') as f:
        pickle.dump(results, f)

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

# 输出pklfile文件中的专利内容
def output_content(pklfile):
    with open(pklfile, 'rb') as f:
        results = pickle.load(f)
    for result in results:
        for num in range(1):
        # for num in range(result['page_size']):
            if result['page_size'] != 0:
                print(result['company'])
                print(result['page_size'])
                print(result['patent'][num+1])

# 切分pklfile为若干等份
def split_pkl(pklfile, num=8):
    with open(pklfile, 'rb') as f:
        results = pickle.load(f)
        step = len(results) // num

    for i in range(num):
        pklfile_split = pklfile.split('.')[0] + '_' + str(i) + '.pkl'
        # print(pklfile_split)
        start = i * step
        if i != num-1:
            end = (i + 1) * step
        else:
            end = len(results)
        results_split = results[start:end]
        with open(pklfile_split, 'wb') as f:
            pickle.dump(results_split, f)

# 合并几份pklfile为一
def concentrate_pkl(pklfile, num=8):
    results=[]
    for i in range(num):
        pklfile_split = pklfile.split('.')[0] + '_' + str(i) + '.pkl'
        with open(pklfile_split, 'rb') as f:
            results_split = pickle.load(f)
        results.extend(results_split)

    with open(pklfile, 'wb') as f:
        pickle.dump(results, f)

def main():
    excelfile='C:\\Files\\Documents\\apollo项目组\\国防科工局成果转化目录\\海淀区的企业名称.xlsx'
    patent_class = 'publish'
    # patent_class = 'authorization'
    # patent_class = 'utility_model'
    # patent_class = 'design'

    pklfile = 'results\\' + patent_class + '\\' + patent_class + '.pkl'

    pklfile_filter = 'results\\' + patent_class + '\\' + patent_class + '_filter.pkl'

    # # create a new pkl file
    # wb = xlrd.open_workbook(excelfile)
    # sheet = wb.sheet_by_name('Sheet1')
    # companys = sheet.col_values(0)[1:8672]
    # new_companys_pkl(pklfile, companys)
    # split_pkl(pklfile, num=8)

    for i in range(8):
        pklfile_split = pklfile.split('.')[0] + '_' + str(i) + '.pkl'
        count(pklfile_split)

    # output_content(pklfile)

    # concentrate_pkl(pklfile, pklfile_1, pklfile_2, pklfile_3)

if __name__ == "__main__":
    main()
