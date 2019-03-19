import xlrd
import pickle
import os
from tqdm import tqdm
import math

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

# 计算单个pklfile文件中包含专利的公司数和页数
def count(pklfile):
    company_num = 0
    page_num = 0
    with open(pklfile, 'rb') as f:
        results = pickle.load(f)
    for result in results:
        page_size = result['page_size']
        company = result['company']
        if page_size != 0:
            company_num += 1
            page_num += result['page_size']
        # if page_size > 3000:
        #     print(f'{company}共有{page_size}页专利')
    print(f'共有{company_num}/{len(results)}家公司存在专利, 共有{page_num}页专利信息')
    return company_num, page_num

# 计算多个pklfile文件中包含专利的公司数和页数
def count_all(pklfile, num=8):
    company_all = 0
    page_all = 0
    for i in range(num):
        pklfile_split = pklfile.split('.')[0] + '_' + str(i) + '.pkl'
        company_num, page_num = count(pklfile_split)
        company_all += company_num
        page_all += page_num
    print(f'共有{company_all}家公司，{page_all}页专利')

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

# 对获取了pagesize的pklfile依据专利页数切分为若干等份
def split_content_pkl(pklfile, num=8):
    page_sizes = 0
    with open(pklfile, 'rb') as f:
        results = pickle.load(f)

    for result in results:
        page_size = result['page_size']
        page_sizes += page_size

    step = math.ceil(page_sizes / num)
    print(f"共有{page_sizes}页专利，{num}等份step选取为{step}")
    # print(page_sizes,step)
    # steps中存入切分节点
    steps = [0]
    _page_size = 0
    i = 1
    for idx, result in enumerate(results):
        page_size = result['page_size']
        _page_size += page_size
        if _page_size > step * i:
            i += 1
            steps.append(idx+1)

    # 开始依据steps进行切分
    for i in range(num):
        pklfile_split = pklfile.split('.')[0] + '_' + str(i) + '.pkl'
        start = steps[i]
        if i != num-1:
            end = steps[i+1]
        else:
            end = len(results)
        results_split = results[start:end]

        # 输出每段实际总页数
        page_sizes = 0
        for result in results_split:
            page_size = result['page_size']
            page_sizes += page_size
        print(f"第{i}个pickle包含了{len(results_split)}家公司，{page_sizes}页专利信息")

        # # 保存到文件
        # with open(pklfile_split, 'wb') as f:
        #     pickle.dump(results_split, f)

# 切分原始的空pklfile为若干等份
def split_empty_pkl(pklfile, num=8):
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

    # concentrate_pkl(pklfile)
    # count(pklfile)
    count_all(pklfile, num=8)

    # output_content(pklfile)
    # split_content_pkl(pklfile)

if __name__ == "__main__":
    main()
