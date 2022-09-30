import requests
from bs4 import BeautifulSoup
import json
from csv import DictWriter
import os

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


def get_review_topics(review_text, topics):
    text = ''
    for topic in topics:
        text += '({}){}\n'.format(topic['topicCodeName'],
                                  review_text[topic['startIdx']:topic['endIdx'] + 1])
    return text


def reviewCrawler(target_url, filename, category_id, sortTypeNum):
    html = requests.get(target_url).text
    soup = BeautifulSoup(html, 'html.parser')
    dict = soup.select_one('body > script:nth-child(2)').get_text()
    dict = dict[27:]
    json_object = json.loads(dict)
    merchant_num = json_object['smartStoreV2']['channel']['payReferenceKey']
    product_num = json_object['product']['A']['productNo']
    sortType = [
        'REVIEW_RANKING',           # 랭킹순
        'REVIEW_CREATE_DATE_DESC',  # 최신순
        'REVIEW_SCORE_DESC',        # 평점 높은순
        'REVIEW_SCORE_ASC',         # 평점 낮은순
    ]

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
        'sortType': sortType[sortTypeNum],
    }

    response = requests.post(
        'https://smartstore.naver.com/i/v1/reviews/paged-reviews', headers=headers, json=json_data)
    data = response.json()
    totalPages = data['totalPages']

    # 크롤링할 마지막 페이지, 스마트스토어 리뷰는 천 페이지까지만 조회가능
    lastPage = totalPages if totalPages < 1001 else 1000

    f_object = open('data/naver/{}/{}.csv'.format(category_id, filename), 'w',
                    encoding='utf-8-sig', newline='')
    dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
    dictwriter_object.writeheader()

    for page in range(lastPage):
        if page % 100 == 0:
            print("제품번호 {}, 페이지 {}번째 크롤링 중".format(filename, page))
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


if __name__ == '__main__':
    target_url = 'https://smartstore.naver.com/main/products/139208874'
    filename = 'test3'
    category_id = 100002454
    reviewCrawler(target_url, filename, category_id, 3)
