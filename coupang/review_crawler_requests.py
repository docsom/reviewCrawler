#https://waytothem.com/blog/163/
#https://curlconverter.com/

import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
from csv import DictWriter
import time

nowLoc = os.getcwd()
min_text_len = 1
max_num_of_review_per_star = 15

headersCSV = [
    'review_id',
    "review_title",
    "review_user_grade",
    "review_user_name",
    "review_time",
    "review_help_cnt",
    "review_text",
    "review_survey",
    'product_name',
    "product_id"
]

cookies = {
    'PCID': '20118162313960784610299',
    'X-CP-PT-locale': 'ko_KR',
    '_fbp': 'fb.1.1659588906314.1251726976',
    'MARKETID': '20118162313960784610299',
    'sid': '196c96d64d494f0ca994055f6bfb350f6d55a8e9',
    'x-coupang-origin-region': 'KOREA',
    'x-coupang-target-market': 'KR',
    '_ga': 'GA1.2.644421614.1663552878',
    'ILOGIN': 'Y',
    'gd1': 'Y',
    'rememberme': 'true',
    'trac_src': '1042016',
    'trac_spec': '10304903',
    'trac_addtag': '900',
    'trac_ctag': 'HOME',
    'trac_lptag': '%EC%BF%A0%ED%8C%A1',
    'trac_itime': '20220926095636',
    'searchSoterTooltip': 'OFF',
    'bm_sz': '7749705569E9172FA9005DE0EC0DE358~YAAQbQI1FymRvHCDAQAAaQQleBHPg1RSd45YJATaJes5KGQafo8noUH5hGBYn40iv+BL9gVM6tKVLkNZRDC29rCkzZ6bqDKMIh1ZhRPo1B5VfjvSkr5PpihPDS/kqfrcX128IyGNEWsYSm/nQwappHSZ0NT4M8t/IqVMGnz0qnnh+6o4rAdnPAct30a3ckW9gZS917pWLVFgUdXMx+5EkIgl4vTUkq34OCIXySnWvnPJ36P5f/UjUE3idGVrWkKnjkynCkobZa/UacLQaX1OWcpQ6pI1hlsuvLE7ZAajuLYndk8r9+x0aXNYsrvkvH7tpSXZq/4J+E+qe15F~3163442~4276545',
    'overrideAbTestGroup': '%5B%5D',
    'bm_mi': '95634CFF5907175AE08CB9E42082E124~YAAQt5c7Fx4gck+DAQAAdgNteBGbBSCH1h1q/xFvMS1gBtsG4Odw8T7pNy1lHuBVZnXZdQStCyTS+bGkCXqcIR+pzbv1Q9j7fpZE8cLUQT6bqTCH0M51ZNPaxaf45WFRs2tetjWDlJRT0qSI1fvnmkUajj5FhzNSGqqRMC06Z2ban2HHh2+7exkyw3lKN5BTOCFNEwiNp3lZ810VPbrjihgHBwAEpF3+GjynOLVIg2BstF9D1hX/oJJOGVLViHwsy5Uv7jDkoQEciwiqS77lYTim2GI1IX7qUnq5XoZJOy/TBmBxeAPHOitRd22/3B7efP7nKjQSd51tRCpUnuTY2FbaaisgiRVktHTyDvVtRQCqhTuR~1',
    'ak_bmsc': '27642A0BAA81998174E481E14B9F41E1~000000000000000000000000000000~YAAQt5c7F0Ynck+DAQAAsCNteBEVGBhn+LoeKzqJ+CSlc4l4Vcy4FTS22wkFuUsITFCHoG51YGFuxtvwvMIYT44Vjdp9A54whRw1jK6P2AxNz2Xa2tjGLEr7rZOdu4lKbWQycoVE+uAKiNjVnG05KW9QogizeFUg+v9WjeWUjlPzwyaWBEQCYNbaZUpJtXA6VjfFteWkKf7i7yPjeUyUiMfbmbFm5OMGH2O+sH9SVIM064KD0z2CCHIdKMs535pIG1TVNg5gk3sA8k2hLe06etwEpXZ4EMXUeyImGnZgv+19f0iJOd3Xe5SrzQ+iQgz207K7j6RJbSVSaHb2RWPVdAeV7zgFalsKLSJqUt+2Z+qDPkUguYQSdUUd1rjgJIjxLyYTZyFrv4SzyzBpSTNb1ovLBgrYS91GYYVkU5jgEX5Nn+/R3BpS6IV7qUA39NdlMXjDIu+oOlIfJzVJ/oT/wmaLzBikR1MXtU0KpG8zIAH9V6E3jRWGY0QWAiXQK4s5jcYqCu84oIILq+xTZOpGs4axQQnzJ0rb1zVHQXgMFbXp/KQcxqATag==',
    'searchKeyword': '%ED%94%84%EB%A0%88%EC%8B%9C%EC%A7%80%20%EB%8D%94%ED%81%B0%20%ED%96%84%EA%B0%80%EB%93%9D%20%EB%B6%80%EB%8C%80%EC%A0%84%EA%B3%A8',
    'searchKeywordType': '%7B%22%ED%94%84%EB%A0%88%EC%8B%9C%EC%A7%80%20%EB%8D%94%ED%81%B0%20%ED%96%84%EA%B0%80%EB%93%9D%20%EB%B6%80%EB%8C%80%EC%A0%84%EA%B3%A8%22%3A0%7D',
    'FUN': '"{\'search\':[{\'reqUrl\':\'/search.pang\',\'isValid\':true}]}"',
    'x-coupang-accept-language': 'ko_KR',
    'baby-isWide': 'small',
    'cto_bundle': 'KKVoOV8wSTBCNmtVdmVUT0RCc3Vlc09YVlcxbDVVWDZPRDB5aFFraDVYbGYwZEFYTVAxS1Vac0YlMkZGMCUyRmc2eUJPN0VvZVJjdncydm1UbDFkWGlRNmp1dWVzR01xeGZGMzNBQk5HZ1NudWxsY3VLQlFQU091ZjJlVUc1ZHFCYVBqNXRsZHJocE9MMSUyQkdWRENGbVB5NWdvYXZpa3clM0QlM0Q',
    '_abck': 'B00E0DF2BD0B5CCE34434E7DA8E8E605~0~YAAQtwI1F726NHCDAQAAiEV+eAhJzB9Zn3YmDnNhcD7rAtlSng0OQkYib0YkSfKtivF96PBcIsxRDhoYEpd0M/1WAv18/EFLU9dQlQaSRNUaESa3G6+EQwYqsWldQ9pZsFcHeQsjFD9s8LsvxcVfpj9TkNvf6dDo1ic5eyzeV22/WYP7uinWW3N8/vTlSL15PiifKuaOvOEtAaM36Sj9dU7yLpA83cfETbg9Xy538fOCx27PtMMFd+EuHxz9hxxOMP4OnnogJtRywiH3Kduz/pNB5T4iWQtubmVTEWEvoMgmnpwmE/6bSJsqqfq1PNRmxdQ0RfNVSYocKoG+RkC5q/udOP1xsC5m8hOOeWZkVGASAPjmVkUbIYFfLLM=~-1~-1~-1',
    'bm_sv': '4853930EBB3EC2598A320D85528673F9~YAAQtwI1F766NHCDAQAAiEV+eBH7WUXpfWx3oLch/LsVkodOjBf2IMaM7PnTn7p8xQgOZjIwHTyOmHh9BBotXTqUZjG8/8wnvTcZjPvT12QDeqfA2xI4ZcDRGC62KzRDVaRdljub6gsbj37GDCgGq84GA7RdDc/ZA5W456+HkAqELKoYiKNKID9r0+XbIYpgk7YVi4DGXiyU1GCyqwuLDx6tbtMA35zmMjMfV2RUZ579QGn7ljo1BP+XX4LAaGWU8CM=~1',
}

headers = {
    'authority': 'www.coupang.com',
    'accept': '*/*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'PCID=20118162313960784610299; X-CP-PT-locale=ko_KR; _fbp=fb.1.1659588906314.1251726976; MARKETID=20118162313960784610299; sid=196c96d64d494f0ca994055f6bfb350f6d55a8e9; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; _ga=GA1.2.644421614.1663552878; gd1=Y; trac_src=1042016; trac_spec=10304903; trac_addtag=900; trac_ctag=HOME; trac_lptag=%EC%BF%A0%ED%8C%A1; trac_itime=20220926095636; searchSoterTooltip=OFF; bm_sz=7749705569E9172FA9005DE0EC0DE358~YAAQbQI1FymRvHCDAQAAaQQleBHPg1RSd45YJATaJes5KGQafo8noUH5hGBYn40iv+BL9gVM6tKVLkNZRDC29rCkzZ6bqDKMIh1ZhRPo1B5VfjvSkr5PpihPDS/kqfrcX128IyGNEWsYSm/nQwappHSZ0NT4M8t/IqVMGnz0qnnh+6o4rAdnPAct30a3ckW9gZS917pWLVFgUdXMx+5EkIgl4vTUkq34OCIXySnWvnPJ36P5f/UjUE3idGVrWkKnjkynCkobZa/UacLQaX1OWcpQ6pI1hlsuvLE7ZAajuLYndk8r9+x0aXNYsrvkvH7tpSXZq/4J+E+qe15F~3163442~4276545; overrideAbTestGroup=%5B%5D; bm_mi=95634CFF5907175AE08CB9E42082E124~YAAQt5c7Fx4gck+DAQAAdgNteBGbBSCH1h1q/xFvMS1gBtsG4Odw8T7pNy1lHuBVZnXZdQStCyTS+bGkCXqcIR+pzbv1Q9j7fpZE8cLUQT6bqTCH0M51ZNPaxaf45WFRs2tetjWDlJRT0qSI1fvnmkUajj5FhzNSGqqRMC06Z2ban2HHh2+7exkyw3lKN5BTOCFNEwiNp3lZ810VPbrjihgHBwAEpF3+GjynOLVIg2BstF9D1hX/oJJOGVLViHwsy5Uv7jDkoQEciwiqS77lYTim2GI1IX7qUnq5XoZJOy/TBmBxeAPHOitRd22/3B7efP7nKjQSd51tRCpUnuTY2FbaaisgiRVktHTyDvVtRQCqhTuR~1; ak_bmsc=27642A0BAA81998174E481E14B9F41E1~000000000000000000000000000000~YAAQt5c7F0Ynck+DAQAAsCNteBEVGBhn+LoeKzqJ+CSlc4l4Vcy4FTS22wkFuUsITFCHoG51YGFuxtvwvMIYT44Vjdp9A54whRw1jK6P2AxNz2Xa2tjGLEr7rZOdu4lKbWQycoVE+uAKiNjVnG05KW9QogizeFUg+v9WjeWUjlPzwyaWBEQCYNbaZUpJtXA6VjfFteWkKf7i7yPjeUyUiMfbmbFm5OMGH2O+sH9SVIM064KD0z2CCHIdKMs535pIG1TVNg5gk3sA8k2hLe06etwEpXZ4EMXUeyImGnZgv+19f0iJOd3Xe5SrzQ+iQgz207K7j6RJbSVSaHb2RWPVdAeV7zgFalsKLSJqUt+2Z+qDPkUguYQSdUUd1rjgJIjxLyYTZyFrv4SzyzBpSTNb1ovLBgrYS91GYYVkU5jgEX5Nn+/R3BpS6IV7qUA39NdlMXjDIu+oOlIfJzVJ/oT/wmaLzBikR1MXtU0KpG8zIAH9V6E3jRWGY0QWAiXQK4s5jcYqCu84oIILq+xTZOpGs4axQQnzJ0rb1zVHQXgMFbXp/KQcxqATag==; searchKeyword=%ED%94%84%EB%A0%88%EC%8B%9C%EC%A7%80%20%EB%8D%94%ED%81%B0%20%ED%96%84%EA%B0%80%EB%93%9D%20%EB%B6%80%EB%8C%80%EC%A0%84%EA%B3%A8; searchKeywordType=%7B%22%ED%94%84%EB%A0%88%EC%8B%9C%EC%A7%80%20%EB%8D%94%ED%81%B0%20%ED%96%84%EA%B0%80%EB%93%9D%20%EB%B6%80%EB%8C%80%EC%A0%84%EA%B3%A8%22%3A0%7D; FUN="{\'search\':[{\'reqUrl\':\'/search.pang\',\'isValid\':true}]}"; x-coupang-accept-language=ko_KR; baby-isWide=small; cto_bundle=KKVoOV8wSTBCNmtVdmVUT0RCc3Vlc09YVlcxbDVVWDZPRDB5aFFraDVYbGYwZEFYTVAxS1Vac0YlMkZGMCUyRmc2eUJPN0VvZVJjdncydm1UbDFkWGlRNmp1dWVzR01xeGZGMzNBQk5HZ1NudWxsY3VLQlFQU091ZjJlVUc1ZHFCYVBqNXRsZHJocE9MMSUyQkdWRENGbVB5NWdvYXZpa3clM0QlM0Q; _abck=B00E0DF2BD0B5CCE34434E7DA8E8E605~0~YAAQtwI1F726NHCDAQAAiEV+eAhJzB9Zn3YmDnNhcD7rAtlSng0OQkYib0YkSfKtivF96PBcIsxRDhoYEpd0M/1WAv18/EFLU9dQlQaSRNUaESa3G6+EQwYqsWldQ9pZsFcHeQsjFD9s8LsvxcVfpj9TkNvf6dDo1ic5eyzeV22/WYP7uinWW3N8/vTlSL15PiifKuaOvOEtAaM36Sj9dU7yLpA83cfETbg9Xy538fOCx27PtMMFd+EuHxz9hxxOMP4OnnogJtRywiH3Kduz/pNB5T4iWQtubmVTEWEvoMgmnpwmE/6bSJsqqfq1PNRmxdQ0RfNVSYocKoG+RkC5q/udOP1xsC5m8hOOeWZkVGASAPjmVkUbIYFfLLM=~-1~-1~-1; bm_sv=4853930EBB3EC2598A320D85528673F9~YAAQtwI1F766NHCDAQAAiEV+eBH7WUXpfWx3oLch/LsVkodOjBf2IMaM7PnTn7p8xQgOZjIwHTyOmHh9BBotXTqUZjG8/8wnvTcZjPvT12QDeqfA2xI4ZcDRGC62KzRDVaRdljub6gsbj37GDCgGq84GA7RdDc/ZA5W456+HkAqELKoYiKNKID9r0+XbIYpgk7YVi4DGXiyU1GCyqwuLDx6tbtMA35zmMjMfV2RUZ579QGn7ljo1BP+XX4LAaGWU8CM=~1',
    'referer': 'https://www.coupang.com/vp/products/1717552921?itemId=2923167957&vendorItemId=70911802261&pickType=COU_PICK&q=%ED%94%84%EB%A0%88%EC%8B%9C%EC%A7%80+%EB%8D%94%ED%81%B0+%ED%96%84%EA%B0%80%EB%93%9D+%EB%B6%80%EB%8C%80%EC%A0%84%EA%B3%A8&itemsCount=21&searchId=1032de1086f04364816de479fe55e46d&rank=0&isAddedCart=',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

params = {
    'productId': '1717552921',
    'page': '1',
    'size': '5',
    'sortBy': 'ORDER_SCORE_ASC',
    'ratings': '',
    'q': '',
    'viRoleCode': '3',
    'ratingSummary': 'true',
}

def extract_review_info(review_html, _product_id=None):
    '''
    각 페이지에서 받아온 html element에서 정보를 뽑아내는 함수
    input: html element
    output: python dictionary
    '''
    reviewer_html = review_html.select('article > div > div')
    
    review_user_name = reviewer_html[1].get_text().strip()
    review_user_grade = reviewer_html[2].select('div > div > div > div')[0]['data-rating']
    review_time = reviewer_html[2].select('div > div > div')[2].get_text().strip()
    product_name = reviewer_html[4].get_text().strip()
    review_title = review_html.select_one('article > div.sdp-review__article__list__headline')
    review_title = review_title.get_text().strip() if review_title != None else None
    review_text = review_html.select_one('article > div.sdp-review__article__list__review')
    review_text = review_text.get_text().strip() if review_text != None else None
    review_survey = review_html.select_one('article > div.sdp-review__article__list__survey')
    review_survey = review_survey.get_text().strip() if review_survey != None else None
    review_help = review_html.select_one('article > div.sdp-review__article__list__help')
    review_help_cnt = review_help['data-count'] if review_help != None else None
    review_id = review_help['data-review-id'] if review_help != None else None
    
    review_dict = {
        'review_id' : review_id,
        "review_title": review_title,
        "review_user_grade" : review_user_grade,
        "review_user_name" : review_user_name,
        "review_time" : review_time, 
        "review_help_cnt" : review_help_cnt,
        "review_text" : review_text,
        "review_survey" : review_survey,
        'product_name' : product_name,
        "product_id" : _product_id,
    }
    return review_dict


def judge_value_of_review(_text):
    '''
    리뷰 퀄리티에 따라 더 수집할지 말지를 결정하는 함수
    input: str(review's text)
    output: boolean(if quality is good True else False)
    '''
    if _text == None:
        return False
    
    if len(_text) >= min_text_len:
        return True
    else:
        return False
    
    
def get_reviews_in_single_page(product_id, item_id, page, ratings):
    referer = 'https://www.coupang.com/vp/products/{}?itemId={}&isAddedCart='.format(product_id, item_id)
    params['productId'] = product_id
    params['page'] = page
    params['ratings'] = ratings
    headers['referer'] = referer

    response = requests.get('https://www.coupang.com/vp/product/reviews', params=params, cookies=cookies, headers=headers, timeout=3)
    
    if response.status_code == 200:
        bad_review = 0
        review_list = []
        html = response.text
        bsObject = BeautifulSoup(html, 'lxml')
        
        review_htmls = bsObject.select('article.sdp-review__article__list')
        for review_html in review_htmls:
            review_info = extract_review_info(review_html, product_id)
            if judge_value_of_review(review_info['review_text']) == True:
                review_list.append(review_info)
            else:
                bad_review += 1
                
        if len(review_list) <= 2:
            should_stop = True
        else:
            should_stop = False
            
        return review_list, should_stop

    else:
        print(response.status.code)
        
        
def save_reviews(_category_id, _product_id, _review_list):
    '''
    리스트로 들어온 리뷰 info를 저장하는 함수
    '''
    try:
        dir_loc = '{}/data/coupang/{}/reviews'.format(nowLoc, _category_id)
        try:
            dirExist = os.path.exists(dir_loc)
            if not dirExist :
                os.makedirs(dir_loc)
        except OSError:
                print("Error: Creating Dir {}".format(dir_loc))
                
        try:
            fileExist = os.path.exists("{}/{}.csv".format(dir_loc, _product_id))
            if not fileExist:
                with open('{}/{}.csv'.format(dir_loc, _product_id), 'a', newline='', encoding="utf-8-sig") as f_object:
                    dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
                    dictwriter_object.writeheader()
        except OSError:
                print("Error: Creating Csv {}/{}.csv".format(dir_loc, _product_id))
    
        with open('{}/{}.csv'.format(dir_loc, _product_id), 'a', newline='', encoding="utf-8-sig") as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
            for i in _review_list:
                dictwriter_object.writerow(i)
    except:
        print("I think there is something wrong with saving...")


def get_save_reviews_in_single_product(category_id, product_id, item_id):
    for ratings in range(1, 6):
        page = 0
        num_of_review_per_star = 0
        while 1:
            page += 1
            review_list, should_stop = get_reviews_in_single_page(product_id, item_id, page, str(ratings))
            save_reviews(category_id, product_id, review_list)
            num_of_review_per_star += len(review_list)
            if should_stop == True:
                break
            if num_of_review_per_star >= max_num_of_review_per_star:
                break
    print("all reviews in product:{} is taken".format(product_id))
    
    
category_id = '502382'
product_id = '1717552921'
item_id = '2923167957'
get_save_reviews_in_single_product(category_id, product_id, item_id)