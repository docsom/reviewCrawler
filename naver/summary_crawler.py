import requests
from bs4 import BeautifulSoup
import json
from csv import DictWriter
import os
import time

headersCSV = [
    'mallId',
    'mallProductId',
    'updateType',
    'mallReviewId',
    'mallSeq',
    'nvMid',
    'matchNvMid',
    'userId',
    'title',
    'content',
    'registerDate',
    'modifyDate',
    'createTime',
    'qualityScore',
    'starScore',
    'topicYn',
    'topicCount',
    'topics',
    'uniqueKey',
    'mallName',
    'cleanContent', # 리뷰 내용에서 태그 문자 제거 버전
    'topicSpans', # 인덱싱하여 뽑은 속성 문자열
    'naverSmry' # 네이버의 요약문
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
    # print(review_text)
    result = bytes(review_text, 'utf-8')
    for topic in topics:
        try:
            text += '({}){}\n'.format(topic['topicName'],
            result[topic['startPosition']:topic['endPosition'] + 1].decode('utf-8'))
        except: # 원인불명의 디코딩 에러로 임시방편 디버깅
            try:
                text += '({}){}\n'.format(topic['topicName'],
                result[topic['startPosition'] + 1:topic['endPosition'] + 2].decode('utf-8'))
            except:
                continue
    return text


def topicReviewCrawler(target_url, category_id, naverSmry):
    response = requests.get(target_url)
    refererUrl = response.url
    tmp = refererUrl.split('?')[0]
    productNum = tmp.split('/')[-1]
    print('Start', productNum)

    # 용량, 양, 음식량 = amount
    # 용량 = capacity
    topicList = ['taste', 'price', 'amount', 'capacity', 'packing', 'smell', 'food-texture', 'size', 'component']
    keys = ['mallId', 'mallProductId', 'updateType', 'mallReviewId', 'mallSeq', 'nvMid', 'matchNvMid', 'userId', 'title', 'content', 'registerDate', 'modifyDate', 'createTime', 'qualityScore', 'starScore', 'topicYn', 'topicCount', 'topics', 'uniqueKey', 'mallName',]

    f_object = open('data/naverSmry/{}/{}.csv'.format(category_id, productNum), 'w',
                    encoding='utf-8-sig', newline='')
    dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
    dictwriter_object.writeheader()

    putNaverSmry = True
    for topic in topicList:
        headers = {
            'authority': 'search.shopping.naver.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ko',
            'referer': '{}'.format(refererUrl),
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
        }
        params = {
            'nvMid': '{}'.format(productNum),
            'topicCode': '{}'.format(topic),
            'reviewType': 'ALL',
            'sort': 'QUALITY',
            'isNeedAggregation': 'N',
            'isApplyFilter': 'Y',
            'page': '1',
            'pageSize': '20',
        }
        while(True):
            print('속성:', topic, '-', '페이지 {}번째 크롤링 중'.format(params['page']))
            response = requests.get('https://search.shopping.naver.com/api/review', params=params, headers=headers)
            time.sleep(0.5) # 차단 방지 나중에 개선
            # 속성 리뷰는 100 페이지까지만 조회가능
            if response.status_code != 200:
                print('응답 코드:', response.status_code)
                break
            data = response.json()
            # print(response.text)
            rawReviews = data['reviews']
            # print(rawReviews)
            if rawReviews == []:
                break
            for rawReview in rawReviews:
                review = dict((key, value) for key, value in rawReview.items() if key in keys)
                myDict = review
                content = review['content']
                content = content.replace('<em>', '')
                content = content.replace('</em>', '')
                myDict['topicSpans'] = get_review_topics(content, review['topics'])
                soup = BeautifulSoup(content, "html.parser")
                myDict['cleanContent'] = soup.text.replace('\r', '')
                if putNaverSmry:
                    myDict['naverSmry'] = naverSmry
                    putNaverSmry = False
                dictwriter_object.writerow(myDict)
            params['page'] = str(int(params['page'])+1)

        print('The {} reviews have been crawled.'.format(topic))

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
    category_id = 100002372
    f_object = open('data/naverSmry/ids_{}.txt'.format(category_id), 'r', encoding='utf-8-sig')
    lines = f_object.readlines()
    for line in lines:
        label = line.split('\001')[1]
        target_url = line.split('\001')[2]
        topicReviewCrawler(target_url, category_id, label)
    f_object.close()
    # target_url = 'https://cr.shopping.naver.com/adcr.nhn?x=8GiJOSTLnh39lObRmoUXO%2F%2F%2F%2Fw%3D%3Ds3UZ2T%2FH%2F6i2Wc71WcBbR4mss%2BDezz%2FPflB1qDLdWh5p5hkeImw66W5qs9aR1r7Z%2B%2FnRoq7YcJSxtMWn3v9ljcd9%2BKy%2Fm0d%2BgYWHtEf61Jo4hrX7i8ROREiNblWok2%2BM4oYeAqlreQxCn%2BOAbX6Xeh7Gg3nKmLbEMYSaftqeFnbrGpelaC3%2FK22mNkRoW9cmDnQubh9F08nN12zHsJEXRo4ZnlrSZr8PDPdBCvs8uWtdeJxHcKH4rYUhc5SxvGs%2FQIsksK7dd6ha3p3XZi36XM8ezX%2BiQ7LEkmIBpqnvCtIb84irqoupb5cHtoCFQH9lAJV03cukp%2F9sq6JmLvPVclAAQkM7F6TjwnGOyP%2BG99QPsoDTOjL%2FRwnN1Cm2LdaiIlmZqbWD5MrHBf672VYogS2HbbaXf3hnVKPBhSrO6MxDTnT7wrQ1XXGtOix8nYxu2UF4nJnyC41n0rMVn4Cj2YgRzTktOJsG39rC0oovAKqd6%2FPFyiqK0iBpqFnOtt1BIo64ifB9DVeZ8ffla9GlFdjFnjNpze14buYlWa7lHYeGukIuG8eXjARXROG%2Bb%2Brf%2Bi1X14H%2Bkq4Y3XEq%2BgyImSZeYgeOTEnI58BVLCkG%2FvJdjtEEnHZo%2B%2FVuCJHvsmHjrNWltBIaVSLNVGpbfcEUD4g%3D%3D&nvMid=10776362971&catId=50001876'
    # productCrawler(100002364, 50000026, 0)