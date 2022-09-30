from review_crawler_smartstore import *
from product_crawler import *
from category_id_info import *
import multiprocessing
from functools import partial
import time

# url 텍스트가 존재하는지 확인. 없으면 프로덕트 크롤러 실행


# url 텍스트의 url을 리스트로 다 저장한 후 하나씩 리뷰 클로러 실행
with open("data/naver/ids_100002454.txt", "r", encoding='utf-8-sig') as f:
    URLs = f.read().splitlines()
    products = [url[43:] for url in URLs]

if __name__ == '__main__':
    start_time = time.time()
    pool = multiprocessing.Pool(processes=8)
    func = partial(reviewCrawler, sortTypeNum=3)
    pool.map(func, URLs, products)
    pool.close()
    pool.join()
    print("--- elapsed time %s seconds ---" % (time.time() - start_time))

# 데이터 폴더에 카테고리 있는지 확인하고 폴더 만들기