import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
from csv import DictWriter
from category_id_info import product_category_splited_section
import time
import random
import json

nowLoc = os.getcwd()

max_product_info = 100

headersCSV = [
    'category_id',
    'product_id',
    'item_id',
    'vendor_item_id',
    'product_name',
    'product_price',
    'average_star',
    'rating_count',
]

cookies_loc = '{}/coupang/cookies.json'.format(nowLoc)
with open(cookies_loc, 'r') as f:
    cookies = json.load(f)

headers = {
    'authority': 'www.coupang.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'PCID=20118162313960784610299; X-CP-PT-locale=ko_KR; _fbp=fb.1.1659588906314.1251726976; MARKETID=20118162313960784610299; sid=196c96d64d494f0ca994055f6bfb350f6d55a8e9; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; _ga=GA1.2.644421614.1663552878; gd1=Y; trac_src=1042016; trac_spec=10304903; trac_addtag=900; trac_ctag=HOME; trac_lptag=%EC%BF%A0%ED%8C%A1; trac_itime=20220926095636; searchSoterTooltip=OFF; bm_sz=7749705569E9172FA9005DE0EC0DE358~YAAQbQI1FymRvHCDAQAAaQQleBHPg1RSd45YJATaJes5KGQafo8noUH5hGBYn40iv+BL9gVM6tKVLkNZRDC29rCkzZ6bqDKMIh1ZhRPo1B5VfjvSkr5PpihPDS/kqfrcX128IyGNEWsYSm/nQwappHSZ0NT4M8t/IqVMGnz0qnnh+6o4rAdnPAct30a3ckW9gZS917pWLVFgUdXMx+5EkIgl4vTUkq34OCIXySnWvnPJ36P5f/UjUE3idGVrWkKnjkynCkobZa/UacLQaX1OWcpQ6pI1hlsuvLE7ZAajuLYndk8r9+x0aXNYsrvkvH7tpSXZq/4J+E+qe15F~3163442~4276545; bm_mi=95634CFF5907175AE08CB9E42082E124~YAAQt5c7Fx4gck+DAQAAdgNteBGbBSCH1h1q/xFvMS1gBtsG4Odw8T7pNy1lHuBVZnXZdQStCyTS+bGkCXqcIR+pzbv1Q9j7fpZE8cLUQT6bqTCH0M51ZNPaxaf45WFRs2tetjWDlJRT0qSI1fvnmkUajj5FhzNSGqqRMC06Z2ban2HHh2+7exkyw3lKN5BTOCFNEwiNp3lZ810VPbrjihgHBwAEpF3+GjynOLVIg2BstF9D1hX/oJJOGVLViHwsy5Uv7jDkoQEciwiqS77lYTim2GI1IX7qUnq5XoZJOy/TBmBxeAPHOitRd22/3B7efP7nKjQSd51tRCpUnuTY2FbaaisgiRVktHTyDvVtRQCqhTuR~1; ak_bmsc=27642A0BAA81998174E481E14B9F41E1~000000000000000000000000000000~YAAQt5c7F0Ynck+DAQAAsCNteBEVGBhn+LoeKzqJ+CSlc4l4Vcy4FTS22wkFuUsITFCHoG51YGFuxtvwvMIYT44Vjdp9A54whRw1jK6P2AxNz2Xa2tjGLEr7rZOdu4lKbWQycoVE+uAKiNjVnG05KW9QogizeFUg+v9WjeWUjlPzwyaWBEQCYNbaZUpJtXA6VjfFteWkKf7i7yPjeUyUiMfbmbFm5OMGH2O+sH9SVIM064KD0z2CCHIdKMs535pIG1TVNg5gk3sA8k2hLe06etwEpXZ4EMXUeyImGnZgv+19f0iJOd3Xe5SrzQ+iQgz207K7j6RJbSVSaHb2RWPVdAeV7zgFalsKLSJqUt+2Z+qDPkUguYQSdUUd1rjgJIjxLyYTZyFrv4SzyzBpSTNb1ovLBgrYS91GYYVkU5jgEX5Nn+/R3BpS6IV7qUA39NdlMXjDIu+oOlIfJzVJ/oT/wmaLzBikR1MXtU0KpG8zIAH9V6E3jRWGY0QWAiXQK4s5jcYqCu84oIILq+xTZOpGs4axQQnzJ0rb1zVHQXgMFbXp/KQcxqATag==; searchKeyword=%ED%94%84%EB%A0%88%EC%8B%9C%EC%A7%80%20%EB%8D%94%ED%81%B0%20%ED%96%84%EA%B0%80%EB%93%9D%20%EB%B6%80%EB%8C%80%EC%A0%84%EA%B3%A8; searchKeywordType=%7B%22%ED%94%84%EB%A0%88%EC%8B%9C%EC%A7%80%20%EB%8D%94%ED%81%B0%20%ED%96%84%EA%B0%80%EB%93%9D%20%EB%B6%80%EB%8C%80%EC%A0%84%EA%B3%A8%22%3A0%7D; FUN="{\'search\':[{\'reqUrl\':\'/search.pang\',\'isValid\':true}]}"; overrideAbTestGroup=%5B%5D; baby-isWide=small; cto_bundle=Ylvgl18wSTBCNmtVdmVUT0RCc3Vlc09YVld6bEFFS0hpUUtISXNRRDYlMkZVaXRpYyUyQmNpbzQlMkIyJTJGendVUnRxYkowYiUyRnhxYyUyRnFkRWhvNlZITVRkM1l5d3hQTnBQYzhqJTJGRDl5b1JnajhmS243OU1jMmNFY29ybVdRWEVHaWNoWHNlV3BpV0hpRDhiUjE3OTZvSDRCNWxFZUFPUE42dyUzRCUzRA; bm_sv=4853930EBB3EC2598A320D85528673F9~YAAQ3Zc7F6s9sW+DAQAAJYu/eBEKmMt+DoEAlRInUH7A00f1Y9PCmG8wu0kX4g50XEum1juWdIA4syvL5npi/Luzz50iP6thdayFFEEOH9ZCUzF15nMIJ9F2eVE4Ve9ilOU2Y8h8OBnooDQKGE07Kk7o01s4wAfQiQxOvvV8dz3tMe1/FWcNKT1lvJz++B9hX/y2Be0IZ2b+3F7PYBRRqk/WX0h4+L//lS+ETLVGwYHf8nnVqEY42SVNN8TN8G7iXR8=~1; x-coupang-accept-language=ko-KR; _abck=B00E0DF2BD0B5CCE34434E7DA8E8E605~0~YAAQ3Zc7F8I9sW+DAQAAR4u/eAjF3ndjC8HX4njLnCQ1eNTBUeqmXX+bDZLx6q+5Zbe4oDBfxm8+1sASl1RBHfsVrwUQQcEt3ME3ZnyyqcX4e8j7TqFgwSczSsPYLUbE7T6mEwNKDEq/T2IidvZ/tH4yqmKhPd6NPjsuswmnjzAs87Xi8y1t8IdW+hlblYroxosQEItRP/DIwrWj518gLZ8wndoiQInjRux9Q/38bHzXKLF0aZj59nCGbN57PhzvBtgqUrzpHUi+uTAdr3fe6QuTzebEQ4Tft+8c1H6mbOwpR7eROCqHPHS6te1qLAOA6B3pK5J7WxZ4VVU4hvNSdWRn3G709Vm0k8DiBksT0DpDwK+F2CAsRyzjHL4=~-1~-1~-1; CLICKED_PAGE=2',
    'referer': 'https://www.coupang.com/np/categories/486687',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

params = {
    'page': '2',
}


def rantime(_min = 0., _max = 1.):
    num = random.random()
    return _min + num * (_max - _min)


def extract_product_info(product_html, category_id):
    product_id = product_html['data-product-id']
    vendor_item_id = product_html['data-vendor-item-id']
    item_id = product_html.select_one('a.baby-product-link')['data-item-id']
    product_name = product_html.select_one('div.name')
    product_name = product_name.get_text().strip() if product_name != None else None
    product_price = product_html.select_one('strong.price-value')
    product_price = product_price.get_text().strip() if product_price != None else None
    average_star = product_html.select_one('em.rating')
    average_star = average_star.get_text().strip() if average_star != None else None
    rating_count = product_html.select_one('span.rating-total-count')
    rating_count = rating_count.get_text().lstrip('(').rstrip(')') if rating_count != None else None
    
    product_dict = {
        'category_id' : category_id,
        'product_id' : product_id,
        'item_id' : item_id,
        'vendor_item_id' : vendor_item_id,
        'product_name' : product_name,
        'product_price' : product_price,
        'average_star' : average_star,
        'rating_count' : rating_count,
    }
    
    return product_dict


def judge_value_of_review(review_dict):
    rating_count = int(review_dict['rating_count']) if review_dict['rating_count'] != None else 0
    if rating_count <= 500:
        return False # bad product
    else:
        return True # good product


def judge_crawl_to_stop(num_bad_product):
    if num_bad_product > 10:
        return True # time to stop
    else:
        return False # keep crawling


def get_products_info_in_single_page(category_id, page):
    '''
    page 하나에서 product info를 뽑아내는 함수
    '''
    cookies['CLICKED_PAGE'] = str(page)
    params['page'] = str(page)
    headers['referer'] = 'https://www.coupang.com/np/categories/{}'.format(category_id)

    response = requests.get('https://www.coupang.com/np/categories/{}'.format(category_id), params=params, cookies=cookies, headers=headers, timeout=3.)

    if response.status_code == 200:
        product_list = []
        
        num_bad_product = 0
        
        html = response.text
        bsObject = BeautifulSoup(html, 'lxml')
        
        product_htmls = bsObject.select('li.baby-product')
        for product_html in product_htmls:
            review_dict = extract_product_info(product_html, category_id)
            if judge_value_of_review(review_dict) == False:
                num_bad_product += 1
            else:
                product_list.append(review_dict)
                
        return product_list, num_bad_product
    else:
        print(response.status.code)
        
        
def save_product_info(category_id, product_list):
    try:
        dir_loc = '{}/data/coupang/{}'.format(nowLoc, category_id)
        try:
            dirExist = os.path.exists(dir_loc)
            if not dirExist :
                os.makedirs(dir_loc)
        except OSError:
                print("Error: Creating Dir {}".format(dir_loc))
                
        try:
            fileExist = os.path.exists("{}/{}.csv".format(dir_loc, category_id))
            if not fileExist:
                with open('{}/{}.csv'.format(dir_loc, category_id), 'a', newline='', encoding="utf-8-sig") as f_object:
                    dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
                    dictwriter_object.writeheader()
        except OSError:
                print("Error: Creating Csv {}/{}.csv".format(dir_loc, category_id))
    
        with open('{}/{}.csv'.format(dir_loc, category_id), 'a', newline='', encoding="utf-8-sig") as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
            for i in product_list:
                dictwriter_object.writerow(i)
    except:
        print("I think there is something wrong with saving...")
        

def get_save_products_info_in_single_category(category_id):
    print("Start doing category: {}...".format(category_id))
    num_product = 0
    page = 0
    
    while 1:
        page += 1
        product_list, num_bad_product = get_products_info_in_single_page(category_id, page)
        save_product_info(category_id, product_list)
        num_product += len(product_list)
        
        if judge_crawl_to_stop(num_bad_product) == True:
            print("So many bad product: # of {} in category:{}".format(num_bad_product, category_id))
            break
        if num_product >= max_product_info:
            print("num of product in category:{} are bigger than {}".format(category_id, max_product_info))
            break
        
        time.sleep(rantime(0.5, 0.7))
        

def get_save_products_info_in_given_categories(category_list):
    for category_id in category_list:
        get_save_products_info_in_single_category(category_id)
        overwrite_drop_duplicates_in_existing_single_category(category_id)
        

def overwrite_drop_duplicates_in_existing_single_category(category_id):
    '''
    중복을 삭제해주는 함수
    이미 지금 있는 거에는 처리 다 했음
    '''
    product_info_loc = '{}/data/coupang/{}/{}.csv'.format(nowLoc, category_id, category_id)
    try:
        products_info = pd.read_csv(product_info_loc)
        products_info.drop_duplicates('product_id', inplace = True)
        products_info.reset_index(drop=True, inplace = True)
        products_info.to_csv('./data/coupang/{}/{}.csv'.format(category_id, category_id), index=False, encoding='utf-8-sig')
    except:
        print("Error!")
#category_list = product_category_splited_section
#get_save_products_info_in_given_categories(category_list)

#link test
# category_id = '225481'
# page = 1
# get_products_info_in_single_page(category_id, page)