import requests
from bs4 import BeautifulSoup
import json
from csv import DictWriter
import os

headers = {
    'authority': 'search.shopping.naver.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ko',
    'logic': 'PART',
    #'referer': 'https://search.shopping.naver.com/search/category/100002454?catId=50001081&origQuery&pagingIndex=1&pagingSize=60&productSet=total&query&sort=review&timestamp=&viewType=list',
    'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50',
}

params = {
    'sort': 'review',
    'pagingIndex': '1',
    'pagingSize': '80',
    'viewType': 'list',
    'productSet': 'total',
    'catId': '50001081',
    'spec': '',
    'deliveryFee': '',
    'deliveryTypeValue': '',
    'iq': '',
    'eq': '',
    'xq': '',
}

nowLoc = os.getcwd()
category_id = 100002454
filename = str(category_id)+'_products.txt'
page = 1
url = 'https://search.shopping.naver.com/search/category/{}?origQuery&pagingIndex={}&pagingSize=80&productSet=total&query&sort=review&timestamp=&viewType=list'.format(category_id, page)

html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')
data = soup.find_all('em', 'basicList_num__sfz3h')



response = requests.get('https://search.shopping.naver.com/api/search/category/100002454', params=params, headers=headers)

f_object = open('{}/data/naver/{}'.format(nowLoc, filename), 'a', encoding='utf-8-sig')



f_object.close()