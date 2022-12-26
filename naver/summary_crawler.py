import requests
from bs4 import BeautifulSoup
import json
from csv import DictWriter
import os
import time

headersCSV = [
    "review_id",
    "review_user_grade",
    'review_user_name',
    "review_time",
    "review_help_cnt",
    "review_text",
    'product_name',
    "product_id",
    "review_topics"
]

def productCrawler(category_id, catId, minReviewNum):
    url = 'https://search.shopping.naver.com/search/category/{}?catId={}&origQuery&pagingSize=80&productSet=total&query&sort=review&timestamp=&viewType=thumb'.format(
        category_id, catId
    )
    headers = {
        'authority': 'search.shopping.naver.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ko',
        'logic': 'PART',
        'referer': url,
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    }
    params = {
        'sort': 'review',
        'pagingIndex': '1',
        'pagingSize': '80',
        'viewType': 'thumb',
        'productSet': 'model',
        'catId': '{}'.format(catId),
        'spec': '',
        'deliveryFee': '',
        'deliveryTypeValue': '',
        'frm': 'NVSHMDL',
        'iq': '',
        'eq': '',
        'xq': '',
        'window': '',
    }
    response = requests.get(
        'https://search.shopping.naver.com/api/search/category/{}'.format(category_id),
        params=params,
        headers=headers,
    )
    json_object = response.json()
    products = json_object['shoppingResult']['products']
    totalPages = json_object['productSetFilter']['filterValues'][1]['productCount']//80 # 가격비교 탭의 상품 수 / 80

    nowLoc = os.getcwd() # C:\Users\CJ\project\review_crawler
    f_object = open('{}/data/naverSmry/ids_{}.txt'.format(nowLoc,
                    category_id), 'w', encoding='utf-8-sig')

    endSearch = False
    errorFlag = False

    for page in range(totalPages):
        print(page)
        for product in products:
            if errorFlag:
                errorFlag = False
                break
            if product['reviewCountSum'] > minReviewNum:
                if product['smryReview'] != '':
                    f_object.write(product['productName']+'\001')
                    f_object.write(product['smryReview']+'\001')
                    f_object.write(product['crUrl']+'\n')
            else:
                endSearch = True
                break
        if endSearch:
            break
        params['pagingIndex'] = str(int(params['pagingIndex'])+1)
        if int(params['pagingIndex']) > totalPages:
            break
        response = requests.get('https://search.shopping.naver.com/api/search/category/{}'.format(
            category_id), params=params, headers=headers)
        time.sleep(0.5) # 429 에러 대응
        if response.status_code == 307: # 307 에러 대응
            print("307 에러 발생")
            time.sleep(5)
            response = requests.get('https://search.shopping.naver.com/api/search/category/{}'.format(
                category_id), params=params, headers=headers)
        try:
            json_object = response.json()
        except: # 주로 429 에러 발생함. Too many requests. 일정 시간 IP 차단함. 초당 10건 밑으로 요청해보자.
            print("응답 코드:", response.status_code)
            print("에러 발생.", page, "번째 페이지 건너뜀")
            errorFlag = True
            continue
        products = json_object['shoppingResult']['products']

    f_object.close()
    print('The URL of products have been crawled.')

def reduceUrl(category_id):
    nowLoc = os.getcwd()
    f_object = open('{}/data/naverSmry/ids_{}.txt'.format(nowLoc, category_id), 'r', encoding='utf-8-sig')
    lines = f_object.readlines()
    result = []
    mySet = set()
    for x in lines:
        y = x.split('\001')[0] + '\001' + x.split('\001')[1]
        if y not in mySet:
            mySet.add(y)
            result.append(x)
    f_object.close()
    os.rename('{}/data/naverSmry/ids_{}.txt'.format(nowLoc, category_id), '{}/data/naverSmry/ids_{}_origin.txt'.format(nowLoc, category_id))
    with open('{}/data/naverSmry/ids_{}.txt'.format(nowLoc, category_id), 'w', encoding='utf-8-sig') as file:
        file.writelines(result)


def get_review_topics(review_text, topics):
    text = ''
    for topic in topics:
        text += '({}){}\n'.format(topic['topicCodeName'],
                                  review_text[topic['startIdx']:topic['endIdx'] + 1])
    return text


def reviewCrawler(target_url, category_id):
    response = requests.get(target_url)
    refererUrl = response.url
    topicList = ['taste', 'price', 'amount', 'capacity', 'packing', 'smell', 'food-texture', 'size', 'component']
    # 용량, 양, 음식량 셋 다 amount
    # 용량 capacity
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        dict = soup.select_one('body > script:nth-child(2)').get_text()
    except: # 비동기식 스크립트 에러 발생. 나중에 고치기
        return
    dict = dict[27:]
    if not dict.find('async') == -1: # 비동기식 스크립트 에러 발생. 나중에 고치기
        return
    try:
        json_object = json.loads(dict)
    except: # 비동기식 스크립트 에러 발생. 나중에 고치기
        return
    if response.url[:13] == 'https://brand': # 브랜드 스토어
        merchant_num = json_object['channel']['A']['payReferenceKey']
    else: # 스마트 스토어
        merchant_num = json_object['smartStoreV2']['channel']['payReferenceKey']
    product_num = json_object['product']['A']['productNo']

    headers = {
        'authority': 'smartstore.naver.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ko',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://smartstore.naver.com',
        'referer': target_url,
        'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
    }

    json_data = {
        'page': 1,
        'pageSize': 20,
        'merchantNo': merchant_num,
        'originProductNo': product_num,
    }

    response = requests.post(
        'https://smartstore.naver.com/i/v1/reviews/paged-reviews', headers=headers, json=json_data)
    data = response.json()
    totalPages = data['totalPages']

    # 크롤링할 마지막 페이지, 스마트스토어 리뷰는 천 페이지까지만 조회가능
    lastPage = totalPages if totalPages < 1001 else 1000

    f_object = open('data/naver/{}/{}.csv'.format(category_id, target_url[43:]), 'w',
                    encoding='utf-8-sig', newline='')
    dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
    dictwriter_object.writeheader()

    for page in range(lastPage):
        if page % 100 == 0:
            print("제품번호 {}, 페이지 {}번째 크롤링 중".format(target_url[43:], page))
        for i in range(len(data['contents'])):
            review = data['contents'][i]
            dict = {
                "review_id": review['id'],
                "review_user_grade": review['reviewScore'],
                'review_user_name': review['writerMemberId'],
                "review_time": review['createDate'],
                "review_help_cnt": review['helpCount'] if 'helpCount' in review.keys() else '0',
                "review_text": review['reviewContent'],
                'product_name': review['productName'],
                "product_id": review['productNo'],
                "review_topics": get_review_topics(review['reviewContent'], review['reviewTopics']) if 'reviewTopics' in review.keys() else '',
            }
            dictwriter_object.writerow(dict)
        json_data['page'] += 1  # 다음 페이지 넘어가기
        if json_data['page'] > lastPage:
            break
        response = requests.post(
            'https://smartstore.naver.com/i/v1/reviews/paged-reviews', headers=headers, json=json_data)
        data = response.json()

    f_object.close()
    print('The reviews of URL have been crawled.')

# # 간편조리식품
# category_id = 100002364
# catId = 50000026
# # 밀키트
# category_id = 100002371
# catId = 50014240
# # 과자/떡/베이커리
# category_id = 100002372
# catId = 50000149

if __name__ == '__main__':
    # target_url = 'https://smartstore.naver.com/main/products/574268591'
    # category_id = 100007947
    # reviewCrawler(target_url, category_id, 3)
    productCrawler(100002364, 50000026, 0)