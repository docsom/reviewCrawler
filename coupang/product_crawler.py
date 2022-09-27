import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
from csv import DictWriter
import time

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
    'trac_addtag': '900',
    'trac_ctag': 'HOME',
    'searchSoterTooltip': 'OFF',
    'trac_spec': '10304902',
    'trac_lptag': 'coupang',
    'trac_itime': '20220926164908',
    'overrideAbTestGroup': '%5B%5D',
    '_abck': 'B00E0DF2BD0B5CCE34434E7DA8E8E605~0~YAAQteQ1F/euVnSDAQAAeepOfAjfaDm5aXyApRh4iCc+vl/zzONp7T9JMV5z+bHg2WQrknQhj6TQdBXKt30RfoLzzmA/AoaXlji8LL3e01Y58ZHMaH4TTHqdtSR/kW+po8qShJG8LQn47dvCHYQtxFDRJS4vGHJ/gmaPIeER1fU5eDzx8p+Sbnx6POXi0Z6PRcfrU4VQR4Umg59gggVlYCLVxRetW6tAbu7Zzs0sSpDFU/kxy3AK3yu5KZVJ7UHl51nebZAX8iyOReIlLqTMW/MhPLp+FwQFHcq6AVEXo6xRV2mKB6NeSsJqlGzKqd1CvDiQp363eWgjAWrNUHwt5C46KX5OpiW7AePizKsWqNJ+De11F63BfvXQDK9ySoBdr4CKXA0IkBd/1td/hzb9pe0tCZ4ASw==~-1~-1~-1',
    'bm_sz': 'A2539E0746184C37240F3B034FDB4326~YAAQteQ1F/quVnSDAQAAeepOfBGL0HzAz7lmz7uXdhQE7F2HKEVDeI1TcB3JLWEkUdP9hlENuj6Xh+1cJCNyovLx0TO8ce6oPbgd+0/BRcdZdajyjg8Oq84rpg1u3hgUVMHBWLGiahOzUNNu8ITxM/KUFyxlzSuktLowm/wgPmVCYCUn8OVOsHCJ43bFZ3iPnsUkhIRO8nA4f6++jcU52Tbs5UlSKowTvaHeJ5QIyno6eNsOxP2YO5E0sKXIb8J/dcAn7t6w3o2nUIJmQFaJrscgxzTz4cerkDYWG1gy0/x/zkz+~3290421~3551300',
    'bm_mi': 'AD8321FD4B7A4E6FE5E4A3B906F7887E~YAAQteQ1FxyxVnSDAQAAEfBOfBEX4X3hNhEJvZlwAj61lrPs6oc7OiqkSTYCpJwDg8xoGVMu881LSGEZVZVQJ5Z5hs8iKgjzf182JsYwLQE7ZAKi4Sp6MqsY6GJaghcF6aWinKiPuV4QB5ghbRLzIRLCbel9U7r2t0vUbzwjsSIzy+sUY/0bhHu8wx/yTnbEVv+AUCob0xIxZ63Nkb/eccqIib0ncM7PBuJ5GC7GC8d2gqJPZkt1nogP7UFbAuF/9WbmXhucmDA+lqRtH3S+phWbFcEA0Qeq1D53rxpIVGCbPhocoy8m94NcJauZG9s=~1',
    'ak_bmsc': 'A7FAC9BE4194233EEC02491E502BE242~000000000000000000000000000000~YAAQteQ1F/a1VnSDAQAAr/1OfBEAiXLNOeA+xDuv41R9Y67hiU0NyTSKmwq0L7elpMIBkhXzTHfqFJ48rnxRFwxITpcDdkcjX5tf1Da/icU+1p2yVT5njIOn6ao+Bi7Jckxb4BlfQkPyuMT8bFA3IKg9/HjUxu4jy3DLxqF++vpFpAJtGkiIovOAoGc4lxHs4tq383t5c9dku6y69zjyufIBwOSjglXPp+3K7bI0F4zY0ARcm6CrEeZPoYgEts0iPjKlMP5zQpk0PlR3EVFS3xRQdZFuyvzWvNTTJLTK0IxB5zA/1BpCP9PBcGkSPLsApl/beVjTge/eW3snJAzuPbjKvhfFWmlSDZV9zglNuWsZF/XfN9f87y5UZmTw7BxVAQ2i/vPu99ivAnzCweXuoEoj9kB8Z4xsah3NKzkvm+vsXcJpFcFBFoVfSK4hoMyKRx/WNXNfXYoNRmB4Jcix5iGJo1+1BDU21ACZAGd6F0GV+XxXu11+x5Dn2TUWY0U1IFbE',
    'cto_bundle': 'OdzM218wSTBCNmtVdmVUT0RCc3Vlc09YVlcxQTVqRlVjVDJEZTdsMGtTJTJGYnJFek1tT0Z2V2QlMkJ6Wm05TnRUcm4xMW5JN3dramRhM2kwJTJCQVRvdjdKMXFESEFJSlFjbTNBWEt2MGxRNSUyQklNZUhKb3FHNVpWUEVkckZPM0J1RDEwSWxLcWRwNCUyQll0cndpcG5zenJWbEpqdlRQbmF3JTNEJTNE',
    'x-coupang-accept-language': 'ko_KR',
    'bm_sv': '0C08F20D03A3F8598ADFDF58D27D76C2~YAAQteQ1F3pBV3SDAQAA491QfBEWrByZi4TGVNZy5z1wKR7MBewC+TYR4stKSKgXK811nf1Dncy+EgGHPK2neLVm2mwSMbU+/7l1IuNxQyhBPvVsvuvE8+3Pi/n+12t/xallfhUt0QAFTqCasxKZgv1rOXIcio/HuBIQtGr1WxAYi8s5wNXLZjYNEoGKNOHLo0ASgYv3xd1da2ruwK8AUSrtKRd5glOBOvjz0kG0HzCp11GVycNDw0e/Sn8tNhlWLpg=~1',
    'baby-isWide': 'small',
    'CLICKED_PRODUCT_ID': '1866720935',
}

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

def extract_product_info(product_html, category_id):
    product_id = product_html['data-product-id']
    vendor_item_id = product_html['data-vendor-item-id']
    item_id = product_html.select_one('a.baby-product-link')['data-item-id']
    product_name = product_html.select_one('div.name').get_text().strip()
    product_price = product_html.select_one('strong.price-value').get_text().strip()
    average_star = product_html.select_one('em.rating').get_text().strip()
    rating_count = product_html.select_one('span.rating-total-count').get_text().lstrip('(').rstrip(')')
    
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
    if int(review_dict['rating_count']) <= 500:
        return False # bad product
    else:
        return True # good product


def judge_crawl_to_stop(num_bad_product):
    if num_bad_product > 10:
        return False # time to stop
    else:
        return True # keep crawling


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
    num_product = 0
    page = 0
    
    while 1:
        page += 1
        product_list, num_bad_product = get_products_info_in_single_page(category_id, page)
        save_product_info(category_id, product_list)
        num_product += len(product_list)
        
        if judge_crawl_to_stop(num_bad_product) == True:
            break
        if num_product >= max_product_info:
            break
        
        # time.sleep(1)
        

# def get_save_products_info_in_given_categories(category_list):
#     for category_id in category_list:
#         get_save_products_info_in_single_category(category_id)
category_id = 486687        
get_save_products_info_in_single_category(category_id)