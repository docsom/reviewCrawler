#https://waytothem.com/blog/163/

#from multiprocessing import Pool

#pepp8 해보기 control k fz

#https://www.coupang.com/vp/products/1717552921/items/2923167957/vendoritems/70911802261
# import json
# from bs4 import BeautifulSoup
# import requests
# import os

# nowLoc = os.getcwd()
# with open("{}/Coupang/Headers.json".format(nowLoc), 'r') as f_object:
#     headers = json.load(f_object)
# class Coupang:
#     def get_product_code(self, url):
#         prod_code = url.split('products/')[-1].split('?')[0]
#         return prod_code
    
#     def __init__(self):
#         self.__headers = headers['headers']
        
#     def main(self):
        
#         #URL = self.input_review_url()
#         URL = "https://www.coupang.com/vp/products/6638786505?itemId=15167378523&vendorItemId=82388756551&sourceType=cmgoms&isAddedCart="
        
#         prod_code = self.get_product_code(url=URL)
    
#         URLS = [f'https://www.coupang.com/vp/product/reviews?productId={prod_code}&amp;page={page}&amp;size=5&amp;sortBy=ORDER_SCORE_ASC&amp;ratings=&amp;q=&amp;viRoleCode=3&amp;ratingSummary=true' for page in range(1,1 + 1)]

        
#         self.__headers['referer'] = URL

#         print(self.__headers)

#         with requests.Session() as session:
#             [self.fetch(url=url,session=session) for url in URLS]

#         print("hi")
#         return None
        
#     def fetch(self,url,session):
#         print("fetch")
#         with session.get(url=url,headers=self.__headers) as response:
#             print("response")
#             html = response.text
#             soup = BeautifulSoup(html,'html.parser')
#             print(soup.prettify())
            
# coupang = Coupang()
# coupang.main()



#https://curlconverter.com/
import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
from csv import DictWriter
import time

nowLoc = os.getcwd()
min_text_len = 50

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
    'gd1': 'Y',
    'trac_src': '1042016',
    'trac_spec': '10304903',
    'trac_addtag': '900',
    'trac_ctag': 'HOME',
    'trac_lptag': '%EC%BF%A0%ED%8C%A1',
    'trac_itime': '20220926095636',
    'searchSoterTooltip': 'OFF',
    'bm_mi': 'F2B9CF442450293E6FBE345640AB306E~YAAQdQI1F6IFOl6DAQAAwmL8dxGMtkQMVY4mvahnTJ483SLRmlqJNhgMb26YNM2kXplUqVoqR6oCKeG7DWugn91LRlLJLxtcfgU8ZsockJYTv4liaoFg6mlmIjhCTP2Q0A7KyHkkTU3IkHEqZ6Wjwz5Yw5r7XsbBOVTKQFZq1gRkh/STOpYVXb762LKsa9wF2OrrL5W6j+apDgAFUu/qP27k+XjlbAlDj9K2xqJsm1CDRtXw5Txgdzx6Eh1ADUbVz/qaylZ27lzJcfsrZwRlKtNgLj9zvLvu9xL5/mQm4wtZNqTZHSoRaFRZy74n+wXz/uUbNqg1lleCh1btSeb/BY0=~1',
    'ak_bmsc': 'B433A5739E538973951E23833D4C60E0~000000000000000000000000000000~YAAQdQI1F8cYOl6DAQAAcrf8dxGNgpjEzUmHDfD0k/X2bTlKgfck6XgXiGZWeGUCON2fflUNHaoNkvlgjBcH6BnP/90/j3O2c6Bd5FkIqMGkZtcVtkws3/mrytkGRIFjF0OF6BxVMsfcA8dkIBsWm/Z2yHR1YX3xYAN3oPSmmwyJMC2X9iwiX4gmzf85Kb/lKxpINn7XGwzpK1BRitZJ00Z0Bi9uW59mv0XKtXVj+4IkSrofda0Zg25Ss2Pidd3bQR2TM/LZl5+Ls5df0sLvwHK0/kiDDBRqUhIj1Au9suyhNzf/MkIOxuNLm36L3SS2JRVcJVFgWnHLnq5W/Lf5soRMhInityYC8ymeoj5Pek4ozr8+Cae+5GGIVvxSpMY3rw+Iwl0I6bWPXtew/tRrY0nAM4OKkWkPpNpZZLj9NzHFppMAyrADF8crnN48rPZ30nkZIb4JFaU=',
    'x-coupang-accept-language': 'ko_KR',
    'overrideAbTestGroup': '%5B%5D',
    'bm_sz': '7749705569E9172FA9005DE0EC0DE358~YAAQbQI1FymRvHCDAQAAaQQleBHPg1RSd45YJATaJes5KGQafo8noUH5hGBYn40iv+BL9gVM6tKVLkNZRDC29rCkzZ6bqDKMIh1ZhRPo1B5VfjvSkr5PpihPDS/kqfrcX128IyGNEWsYSm/nQwappHSZ0NT4M8t/IqVMGnz0qnnh+6o4rAdnPAct30a3ckW9gZS917pWLVFgUdXMx+5EkIgl4vTUkq34OCIXySnWvnPJ36P5f/UjUE3idGVrWkKnjkynCkobZa/UacLQaX1OWcpQ6pI1hlsuvLE7ZAajuLYndk8r9+x0aXNYsrvkvH7tpSXZq/4J+E+qe15F~3163442~4276545',
    'baby-isWide': 'small',
    'cto_bundle': 'ysPLul8wSTBCNmtVdmVUT0RCc3Vlc09YVlc4c0Z3MjYzazNqJTJCNXdWTSUyRjJ1OEhaVUJtOUdDbnhxOTlTMFRFNmMlMkZla2tzWDRmZk5UcmtJT3RZQmZSbXJUMnZKdTU1YURLeHR0MTZYeGJKUEFrMUhidk9ZZDNiRVdHd1clMkIxR1VaQ2EwaUxDc2pXdEkxQmQ5Q094RHE5NXB0cFNwQSUzRCUzRA',
    '_abck': 'B00E0DF2BD0B5CCE34434E7DA8E8E605~0~YAAQZCPJF+q1aGuDAQAAcJc+eAhq0hN3wXlAwGmc7BJ/EpHYqK98BZvrC1DrEWIkI1SjpoG2XORCT0/ihZNe9pokMKQidmEWuc1NLn4HLJAJ1TiJBJL0d/JMkAcsRAZIjX9Tquf1o+kE3LjmPuDqSBUBjmDBhchqeqJ70+5wWS8l6fQs6GKJUqP7u0CJZ74lx1ziFtEZzjvdc7xiUR2k9xAq5QkFnsXfjyQDvlYsMDEoXSI1tj/iCiNF7PuFJSNDbrKTmLkzJiNsdN4DcC8wbGWhHxsyc5aEUEr+8Am5Y+MnWwokTr/YpGDs4KCd82BdYjKkzgSrU0fViNOQVIFbOl1p82teV/WlA27y0nuLKnNbog5uAxIDSG+9skE=~-1~-1~-1',
    'bm_sv': '31B48C7DA69206183ED35B13A94C00EB~YAAQZCPJF+u1aGuDAQAAcJc+eBH4XLf+Sm9wgV2/N5byDnE0nE4edL5g/IaJRYRowKtgKUNIO+ul/N/2oZ4QGgKya/s0CRL4EQWZ+0CU6YO25b+UzY2dBBrsNH5jp16jjTV1RYIqBNnEnVZ0xy3lX0gScMWjVMrsUO6LltU7gmUnWjlpjh+W3ICSUmWbbPBEq8+e43Xgzd1U+7yQPtijfRl4Azr2saLybOwwpacAl5VS7VwM2GACDyDsxYEfN2KOL6Q=~1',
}

headers = {
    'authority': 'www.coupang.com',
    'accept': '*/*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'PCID=20118162313960784610299; X-CP-PT-locale=ko_KR; _fbp=fb.1.1659588906314.1251726976; MARKETID=20118162313960784610299; sid=196c96d64d494f0ca994055f6bfb350f6d55a8e9; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; _ga=GA1.2.644421614.1663552878; gd1=Y; trac_src=1042016; trac_spec=10304903; trac_addtag=900; trac_ctag=HOME; trac_lptag=%EC%BF%A0%ED%8C%A1; trac_itime=20220926095636; searchSoterTooltip=OFF; bm_mi=F2B9CF442450293E6FBE345640AB306E~YAAQdQI1F6IFOl6DAQAAwmL8dxGMtkQMVY4mvahnTJ483SLRmlqJNhgMb26YNM2kXplUqVoqR6oCKeG7DWugn91LRlLJLxtcfgU8ZsockJYTv4liaoFg6mlmIjhCTP2Q0A7KyHkkTU3IkHEqZ6Wjwz5Yw5r7XsbBOVTKQFZq1gRkh/STOpYVXb762LKsa9wF2OrrL5W6j+apDgAFUu/qP27k+XjlbAlDj9K2xqJsm1CDRtXw5Txgdzx6Eh1ADUbVz/qaylZ27lzJcfsrZwRlKtNgLj9zvLvu9xL5/mQm4wtZNqTZHSoRaFRZy74n+wXz/uUbNqg1lleCh1btSeb/BY0=~1; ak_bmsc=B433A5739E538973951E23833D4C60E0~000000000000000000000000000000~YAAQdQI1F8cYOl6DAQAAcrf8dxGNgpjEzUmHDfD0k/X2bTlKgfck6XgXiGZWeGUCON2fflUNHaoNkvlgjBcH6BnP/90/j3O2c6Bd5FkIqMGkZtcVtkws3/mrytkGRIFjF0OF6BxVMsfcA8dkIBsWm/Z2yHR1YX3xYAN3oPSmmwyJMC2X9iwiX4gmzf85Kb/lKxpINn7XGwzpK1BRitZJ00Z0Bi9uW59mv0XKtXVj+4IkSrofda0Zg25Ss2Pidd3bQR2TM/LZl5+Ls5df0sLvwHK0/kiDDBRqUhIj1Au9suyhNzf/MkIOxuNLm36L3SS2JRVcJVFgWnHLnq5W/Lf5soRMhInityYC8ymeoj5Pek4ozr8+Cae+5GGIVvxSpMY3rw+Iwl0I6bWPXtew/tRrY0nAM4OKkWkPpNpZZLj9NzHFppMAyrADF8crnN48rPZ30nkZIb4JFaU=; x-coupang-accept-language=ko_KR; overrideAbTestGroup=%5B%5D; bm_sz=7749705569E9172FA9005DE0EC0DE358~YAAQbQI1FymRvHCDAQAAaQQleBHPg1RSd45YJATaJes5KGQafo8noUH5hGBYn40iv+BL9gVM6tKVLkNZRDC29rCkzZ6bqDKMIh1ZhRPo1B5VfjvSkr5PpihPDS/kqfrcX128IyGNEWsYSm/nQwappHSZ0NT4M8t/IqVMGnz0qnnh+6o4rAdnPAct30a3ckW9gZS917pWLVFgUdXMx+5EkIgl4vTUkq34OCIXySnWvnPJ36P5f/UjUE3idGVrWkKnjkynCkobZa/UacLQaX1OWcpQ6pI1hlsuvLE7ZAajuLYndk8r9+x0aXNYsrvkvH7tpSXZq/4J+E+qe15F~3163442~4276545; baby-isWide=small; cto_bundle=ysPLul8wSTBCNmtVdmVUT0RCc3Vlc09YVlc4c0Z3MjYzazNqJTJCNXdWTSUyRjJ1OEhaVUJtOUdDbnhxOTlTMFRFNmMlMkZla2tzWDRmZk5UcmtJT3RZQmZSbXJUMnZKdTU1YURLeHR0MTZYeGJKUEFrMUhidk9ZZDNiRVdHd1clMkIxR1VaQ2EwaUxDc2pXdEkxQmQ5Q094RHE5NXB0cFNwQSUzRCUzRA; _abck=B00E0DF2BD0B5CCE34434E7DA8E8E605~0~YAAQZCPJF+q1aGuDAQAAcJc+eAhq0hN3wXlAwGmc7BJ/EpHYqK98BZvrC1DrEWIkI1SjpoG2XORCT0/ihZNe9pokMKQidmEWuc1NLn4HLJAJ1TiJBJL0d/JMkAcsRAZIjX9Tquf1o+kE3LjmPuDqSBUBjmDBhchqeqJ70+5wWS8l6fQs6GKJUqP7u0CJZ74lx1ziFtEZzjvdc7xiUR2k9xAq5QkFnsXfjyQDvlYsMDEoXSI1tj/iCiNF7PuFJSNDbrKTmLkzJiNsdN4DcC8wbGWhHxsyc5aEUEr+8Am5Y+MnWwokTr/YpGDs4KCd82BdYjKkzgSrU0fViNOQVIFbOl1p82teV/WlA27y0nuLKnNbog5uAxIDSG+9skE=~-1~-1~-1; bm_sv=31B48C7DA69206183ED35B13A94C00EB~YAAQZCPJF+u1aGuDAQAAcJc+eBH4XLf+Sm9wgV2/N5byDnE0nE4edL5g/IaJRYRowKtgKUNIO+ul/N/2oZ4QGgKya/s0CRL4EQWZ+0CU6YO25b+UzY2dBBrsNH5jp16jjTV1RYIqBNnEnVZ0xy3lX0gScMWjVMrsUO6LltU7gmUnWjlpjh+W3ICSUmWbbPBEq8+e43Xgzd1U+7yQPtijfRl4Azr2saLybOwwpacAl5VS7VwM2GACDyDsxYEfN2KOL6Q=~1',
    'referer': 'https://www.coupang.com/vp/products/293473519?itemId=926572599&isAddedCart=',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

params = {
    'productId': '293473519',
    'page': '1',
    'size': '5',
    'sortBy': 'ORDER_SCORE_ASC',
    'ratings': '5',
    'q': '',
    'viRoleCode': '3',
    'ratingSummary': 'true',
}

product_id = '293473519'
item_id = '926572599'
page = '1'
size = '5'
ratings = '5'
referer = 'https://www.coupang.com/vp/products/{}?itemId={}&isAddedCart='.format(product_id, item_id)

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
    
    
def get_reviews_in_single_page(product_id, item_id, page, size, ratings):
    referer = 'https://www.coupang.com/vp/products/{}?itemId={}&isAddedCart='.format(product_id, item_id)
    params['productId'] = product_id
    params['page'] = page
    params['size'] = size
    params['ratings'] = ratings
    headers['referer'] = referer

    response = requests.get('https://www.coupang.com/vp/product/reviews', params=params, cookies=cookies, headers=headers)
    
    if response.status_code == 200:
        bad_review = 0
        review_list = []
        html = response.text
        bsObject = BeautifulSoup(html, 'lxml')
        
        review_htmls = bsObject.select('article.sdp-review__article__list')
        for review_html in review_htmls:
            review_info = extract_review_info(review_html, product_id)
            review_list.append(review_info)
            if judge_value_of_review(review_info['review_text']) == True:
                review_list.append(review_info)
            else:
                bad_review += 1
                
        if bad_review >= 2:
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
        "I think there is something wrong with saving..."
    
    
get_reviews_in_single_page(product_id, item_id, page, size, ratings)