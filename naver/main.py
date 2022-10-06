from review_crawler_smartstore import reviewCrawler
from product_crawler import productCrawler
from category_id_info import *
import multiprocessing
from functools import partial
import time
import os
import pandas as pd


def getProductsList(company, category_id, catId, minReviewNum):
    txt = "data/{}/ids_{}.txt".format(company, category_id)
    if not os.path.isfile(txt):
        print("Starting product crawling")
        productCrawler(category_id, catId, minReviewNum)
    path = "data/{}/{}".format(company, category_id)
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(txt, "r", encoding='utf-8-sig') as f:
        return f.read().splitlines()


def missingUrlCheck(UrlList):
    URL = []
    for url in UrlList:
        txt = "data/{}/{}/{}.csv".format(company, category_id, url[43:])
        if os.path.isfile(txt):
            continue
        else:
            URL.append(url)
    return URL


def countReviewsProducts():
    reviewNum, productNum = 0, 0
    path = 'C:\\Users\\CJ\\project\\review_crawler\\data\\naver'
    dir = []
    (root, directories, files) = next(os.walk(path))
    for d in directories:
        d_path = os.path.join(root, d)
        dir.append(d_path)
    for filePath in dir:
        csvAll = os.listdir(filePath)
        csvAll = [filePath + '\\' + csv for csv in csvAll]
        for csv in csvAll:
            df = pd.read_csv(csv)
            reviewNum += len(df)
        productNum += len(csvAll)
    return (reviewNum, productNum)


company = 'naver'
category_id = drink[1][2][0]
catId = drink[1][2][1]
minReviewNum = 5000
sortTypeNum = 3

URLs = getProductsList(company, category_id, catId, minReviewNum)
# print(URLs)
# print(missingUrlCheck(URLs))
# print(countReviewsProducts())

start_time = time.time()
if __name__ == '__main__':
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool(processes=16)
    func = partial(reviewCrawler, category_id=category_id,
                   sortTypeNum=sortTypeNum)
    pool.map(func, URLs)
    pool.close()
    pool.join()
    print("--- elapsed time %s seconds ---" % (time.time() - start_time))
