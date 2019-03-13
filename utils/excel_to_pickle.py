import xlrd
import pickle
import os

def new_companys_pkl(pklfile, companys):
    with open(pklfile, 'wb') as f:
        results = []
        for company in tqdm(companys):
            result = {}
            company = company.strip()
            result['company'] = company
            result['page_size'] = 0
            results.append(result)

        pickle.dump(results, f)

def count(pklfile):
    num = 0
    with open(pklfile, 'rb') as f:
        results = pickle.load(f)
        for result in results:
            if result['page_size'] != 0:
                num += 1
        print(f'共有{num}/{len(results)}家公司存在专利')

def split_pkl(pklfile,pklfile_1,pklfile_2,pklfile_3):
    with open(pklfile, 'rb') as f:
        results = pickle.load(f)
        results_1 = results[:2892]
        results_2 = results[2892:5784]
        results_3 = results[5784:]
        with open(pklfile_1, 'wb') as f:
            pickle.dump(results_1, f)
        with open(pklfile_2, 'wb') as f:
            pickle.dump(results_2, f)
        with open(pklfile_3, 'wb') as f:
            pickle.dump(results_3, f)

def concentrate_pkl(pklfile,pklfile_1,pklfile_2,pklfile_3):
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
    pklfile='C:\\Users\\qhykk\\Desktop\\spider\\companys_publish.pkl'
    pklfile_1='C:\\Users\\qhykk\\Desktop\\spider\\companys_publish_1.pkl'
    pklfile_2='C:\\Users\\qhykk\\Desktop\\spider\\companys_publish_2.pkl'
    pklfile_3='C:\\Users\\qhykk\\Desktop\\spider\\companys_publish_3.pkl'

    # pklfile='C:\\Users\\qhykk\\Desktop\\companys_authorization.pkl'

    # create a new pkl file
    wb = xlrd.open_workbook(excelfile)
    sheet = wb.sheet_by_name('Sheet1')
    companys = sheet.col_values(0)[1:8672]
    new_companys_pkl(pklfile, companys)

    # count(pklfile)
    # count(pklfile_1)
    # count(pklfile_2)
    # count(pklfile_3)
    # split_pkl(pklfile,pklfile_1,pklfile_2,pklfile_3)
    # concentrate_pkl(pklfile,pklfile_1,pklfile_2,pklfile_3)

if __name__ == "__main__":
    main()
