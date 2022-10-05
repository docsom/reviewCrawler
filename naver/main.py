from genericpath import isfile
from review_crawler_smartstore import reviewCrawler
from product_crawler import productCrawler
from category_id_info import *
import multiprocessing
from functools import partial
import time
import os


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


company = 'naver'
category_id = mealKit[1][0][0]
catId = mealKit[1][0][1]
minReviewNum = 5000
sortTypeNum = 3

URLs = getProductsList(company, category_id, catId, minReviewNum)

# print(URLs)
# for url in URLs:
#     txt = "data/{}/{}/{}.csv".format(company, category_id, url[43:])
#     if os.path.isfile(txt):
#         continue
#     else:
#         print(url)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    start_time = time.time()
    pool = multiprocessing.Pool(processes=16)
    func = partial(reviewCrawler, category_id=category_id,
                   sortTypeNum=sortTypeNum)
    pool.map(func, URLs)
    pool.close()
    pool.join()
    print("--- elapsed time %s seconds ---" % (time.time() - start_time))
