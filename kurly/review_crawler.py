import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
from csv import DictWriter
from review_manager import ReviewManager

headersCSV = [
    'review_num',
    'review_title',
    'review_user_grade',
    'review_user_name',
    'review_time',
    'review_like_cnt',
    "review_text",
    'product_name',
    'product_name_before',
    'product_id',
]

nowLoc = os.getcwd()

class NoMoreReviewError(Exception):
    pass

class NoSuchFileError(Exception):
    pass

def get_reviews_in_single_page(_goodsno, _page):
    url = "https://www.kurly.com/shop/goods/goods_review_list.php?goodsno={}&page={}".format(_goodsno, _page)

    response = requests.get(url)
    
    #필요하다면 여기에 시간을 넣는 코드를 삽입

    if response.status_code == 200:
        
        review_list = []
        
        html = response.text
        bsObject = BeautifulSoup(html, "lxml")
        
        no_data_html = bsObject.select_one('p.no_data')
        
        if no_data_html != None:
            raise NoMoreReviewError
        
        reviews_html = bsObject.select('div.tr_line')

        for review_html in reviews_html:
            table_html = review_html.select('table > tr > td')
            
            review_num = table_html[0].get_text().replace("\n", "").strip()
            review_title = table_html[1].select_one('div').get_text().replace("\n", " ").strip()
            review_user_grade = table_html[2].get_text().replace("\n", "").strip()
            review_user_name = table_html[3].get_text().replace("\n", "").strip()
            review_time = table_html[4].get_text().replace("\n", "").strip()
            review_like_cnt = table_html[5].get_text().replace("\n", " ").strip()
            
            inner_review_html = review_html.select_one("div.review_view > div.inner_review")
            product_name = inner_review_html.select_one("div.name_purchase > strong").get_text().replace("\n", "")
            product_name_2 = inner_review_html.select_one("div.name_purchase > p").get_text().replace("\n", "")
            
            def getText(parent):
                return ''.join(parent.find_all(text=True, recursive=False)).strip()
            
            review_text = getText(inner_review_html).replace("\n", " ").replace("\r", " ")
            review_text = " ".join(review_text.split())
            
            review_dict = {
                "review_num":review_num, 
                "review_title":review_title, 
                "review_user_grade":review_user_grade, 
                "review_user_name":review_user_name, 
                "review_time":review_time, 
                "review_like_cnt":review_like_cnt, 
                "review_text":review_text, 
                "product_name": product_name, 
                "product_name_before" : product_name_2,
                "product_id": _goodsno
            }
            
            if review_num != "공지":
                review_list.append(review_dict)
            
        print("{}, page:{} done".format(_goodsno, _page))
            
        return review_list
    
    else:
        print(response.status.code)

def get_reviews_in_single_product(_goodsno, _limit=5000):
    '''
    특정 카테고리 안의, 특정 상품에 대해 리뷰를 가져옴
    return list(dict, dict, ....)
    '''
    
    review_list = []
    
    page = 1
    while 1:
        try:
            review_list += get_reviews_in_single_page(_goodsno, page)
            if len(review_list) >= _limit:
                print("More than {} Review is Taken in goodsno:{}".format(_limit, _goodsno))
                break
            
        except NoMoreReviewError:
            print("Every Review is Taken in goodsno:{}".format(_goodsno))
            break
        page += 1
    
    return review_list

def get_new_reviews_in_single_product(_category_id, _goodsno):
    review_list = []

    review_manager = ReviewManager(_category_id)
    _max, _min = review_manager.get_max_min_of_product_id(_category_id)
    
    page = 1
    while 1:
        try:
            temp_review_list = get_reviews_in_single_page(_goodsno, page)
            temp_num_list = []
            for temp_review in temp_review_list:
                if temp_review['review_num'].isdigit():
                    temp_num_list.append(int(temp_review['review_num']))
            if min(temp_num_list) <= _max:
                nobest_review_list = [review for review in temp_review_list if review['review_num'].isdigit() is True]
                best_review_list =  [review for review in temp_review_list if review['review_num'].isdigit() is False]
                nobest_review_list = [review for review in temp_review_list if int(review['review_num']) > _max]
                review_list += (nobest_review_list + best_review_list)
                break
            else:
                review_list += temp_review_list
                page += 1
            
        except NoMoreReviewError:
            print("Every New Review is Taken in goodsno:{}".format(_goodsno))
            
    return review_list

def get_target_products_list_in_single_product(_category_id):
    manager_loc = "{}/data/kurly/{}/{}_review_manager.csv".format(nowLoc, _category_id, _category_id)
    ids_loc = "{}/data/kurly/{}/ids_{}.txt".format(nowLoc, _category_id, _category_id)
    
    manager_exist = os.path.exists(manager_loc)
    ids_exist = os.path.exists(ids_loc)
    
    if not manager_exist:
        print("You should make {}_review_manager.csv first.".format(_category_id))
        raise NoSuchFileError
    if not ids_exist:
        print("You should make ids_{}.txt first.".format(_category_id))
        raise NoSuchFileError
    
    manager_list = [id for id in pd.read_csv(manager_loc).product_id]
    
    ids_list = []
    with open(ids_loc, 'r', encoding="utf-8-sig") as f_object:
        while True:
            line = f_object.readline().strip()
            if not line: break
            ids_list.append(int(line))
    
    target_ids = [id for id in ids_list if id not in manager_list]
    
    return target_ids

def get_save_reviews_in_single_product(_category_id, _goodsno):
    '''
    특정 카테고리 안의, 특정 상품에 대해 리뷰를 가져오고 저장함
    return None
    '''
    
    dirLoc = "{}/data/kurly/{}/reviews".format(nowLoc, _category_id)

    try:
        dirExist = os.path.exists(dirLoc)
        if not dirExist:
            os.makedirs(dirLoc)
    except OSError:
            print("Error: Creating Dir {}".format(dirLoc))
            
    review_list = get_reviews_in_single_product(_goodsno)
    
    reviewListLoc = "{}/{}".format(dirLoc, _goodsno)
    
    with open('{}.csv'.format(reviewListLoc), 'a', newline='', encoding="utf-8-sig") as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        dictwriter_object.writeheader()
        for i in review_list:
            dictwriter_object.writerow(i)
            
# category_id = 911001
# goodsno = 5057076
# get_save_reviews_in_single_product(category_id, goodsno)

def get_save_reviews_in_certain_category(_category_ids):

    for category_id in _category_ids:
        goodsno_list = []
        with open('{}/data/kurly/{}/ids_{}.txt'.format(nowLoc, category_id, category_id), 'r', encoding='utf-8-sig') as f_object:
            for line in f_object:
                goodsno_list.append(line.strip())
        for goodsno in goodsno_list:
            get_save_reviews_in_single_product(category_id, goodsno)
            print("goodsno: {}'s review has been finished".format(goodsno))
            
        print("category: {}'s review has been finished".format(category_id))
        
        try:
            with open('{}/data/kurly_info.txt'.format(nowLoc), 'a', encoding='utf-8-sig') as f_object:
                f_object.write(category_id)
        except:
            pass

def get_save_reviews_in_all_category():
    '''
    ids_(category_id).txt 안에 있는 product List를 읽어서 돌림
    
    이 과정을 data/kurly 안에 들어있는 모든 카테고리 이름을 불러와서 진행함
    '''
    
    category_ids = os.listdir('{}/data/kurly'.format(nowLoc))

    for category_id in category_ids:
        goodsno_list = []
        with open('{}/data/kurly/{}/ids_{}.txt'.format(nowLoc, category_id, category_id), 'r', encoding='utf-8-sig') as f_object:
            for line in f_object:
                goodsno_list.append(line.strip())
        for goodsno in goodsno_list:
            get_save_reviews_in_single_product(category_id, goodsno)
            print("goodsno: {}'s review has been finished".format(goodsno))
            
        print("category: {}'s review has been finished".format(category_id))

def get_save_reviews_in_single_category(category_id):
    
    goodsno_list = []
    
    with open('{}/data/kurly/{}/ids_{}.txt'.format(os.getcwd(), category_id, category_id), 'r', encoding='utf-8-sig') as f_object:
        for line in f_object:
            goodsno_list.append(line.strip())
    for goodsno in goodsno_list:
        get_save_reviews_in_single_product(category_id, goodsno)
        print("goodsno: {}'s review has been finished".format(goodsno))
        
    print("category: {}'s review has been finished".format(category_id))
    
    with open('{}.data/kurly/log.txt', 'a') as f_object:
        f_object.write(category_id)

def get_save_reviews_in_left_products_in_single_category(_category_id):
    target_product_ids = get_target_products_list_in_single_product(_category_id)
    for goodsno in target_product_ids:
        get_save_reviews_in_single_product(_category_id, goodsno)