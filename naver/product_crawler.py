import requests
import os

def productCrawler(category_id, catId, minReviewNum):
    url = 'https://search.shopping.naver.com/search/category/{}?catId={}&origQuery&pagingSize=80&productSet=total&query&sort=review&timestamp=&viewType=list'.format(
        category_id, catId)

    headers = {
        'authority': 'search.shopping.naver.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ko',
        'logic': 'PART',
        'referer': url,
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
        'catId': '{}'.format(catId),
        'spec': '',
        'deliveryFee': '',
        'deliveryTypeValue': '',
        'iq': '',
        'eq': '',
        'xq': '',
    }

    response = requests.get('https://search.shopping.naver.com/api/search/category/{}'.format(
        category_id), params=params, headers=headers)
    json_object = response.json()
    products = json_object['shoppingResult']['products']
    totalPages = json_object['productSetFilter']['filterValues'][0]['productCount']//80

    nowLoc = os.getcwd()
    f_object = open('{}/data/naver/ids_{}.txt'.format(nowLoc,
                    category_id), 'w', encoding='utf-8-sig')

    endSearch = False

    for page in range(totalPages):
        print(page)
        for product in products:
            if product['reviewCountSum'] > minReviewNum:
                if product['mallProductUrl'][:18] == 'https://smartstore':
                    f_object.write(product['mallProductUrl']+'\n')
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
        json_object = response.json()
        products = json_object['shoppingResult']['products']

    f_object.close()
    print('The URL of products have been crawled.')

if __name__ == "__main__":
    category_id = 100002684
    catId = 50012960
    productCrawler(category_id, catId, 5000)