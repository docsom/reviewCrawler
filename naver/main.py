from genericpath import isfile
from review_crawler_smartstore import reviewCrawler
from product_crawler import productCrawler
from category_id_info import *
from multiprocessing import Pool
from functools import partial
import time
import os

# url 텍스트가 존재하는지 확인, 없으면 프로덕트 크롤러 실행
# 데이터 폴더에 카테고리 폴더 있는지 확인하고 폴더 만들기
# url 텍스트의 url을 리스트에 다 넣어서 리턴


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


# print(URLs)
# for url in URLs:
#     txt = "data/naver/100002454/{}.csv".format(url[43:])
#     if os.path.isfile(txt):
#         continue
#     else:
#         print(url)

def categoryCrawler(company, category_id, catId, minReviewNum):
    URLs = getProductsList(company, category_id, catId, minReviewNum)
    start_time = time.time()
    pool = Pool(processes=16)
    func = partial(reviewCrawler, category_id=category_id, sortTypeNum=3)
    pool.map(func, URLs)
    pool.close()
    pool.join()
    print("--- elapsed time %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    categoryCrawler('naver', coffee[1][2][0], coffee[1][2][1], 5000)
