import requests
import os
from bs4 import BeautifulSoup
from csv import DictWriter

headersCSV = [
    'review_num',
    'review_title',
    'review_user_grade',
    'review_user_name',
    'review_time',
    'review_like_cnt',
    "review_text",
    'product_name',
    'product_id',
]
class NoMoreReviewError(Exception):
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
            review_like_cnt = table_html[5].get_text().replace("\n", "").strip()
            
            inner_review_html = review_html.select_one("div.review_view > div.inner_review")
            product_name = inner_review_html.select_one("div.name_purchase > strong").get_text().replace("\n", "")
            review_text = inner_review_html.get_text().replace("\n", " ").replace(product_name, "").strip()
            
            review_dict = {"review_num":review_num, "review_title":review_title, "review_user_grade":review_user_grade, "review_user_name":review_user_name, "review_time":review_time, "review_like_cnt":review_like_cnt, "review_text":review_text, "product_name": product_name, "product_id": _goodsno}
            
            review_list.append(review_dict)
            
        print("{}, page:{} done".format(_goodsno, _page))
            
        return review_list
            #print( "#", review_num, "#", review_title,  "#", review_user_grade,  "#", review_user_name,  "#", review_time,  "#", review_like_cnt, "#")
            #print("#", product_name, "#", review_text)
    else:
        print(response.status.code)

def get_reviews_in_single_product(_goodsno):
    review_list = []
    
    page = 1
    while 1:
        try:
            review_list += get_reviews_in_single_page(_goodsno, page)
        except NoMoreReviewError:
            print("Every Review is Sorted in goodsno:{}".format(_goodsno))
            break
        page += 1
    
    return review_list

def get_save_reviews_in_single_product(_category_id, _goodsno):
    nowLoc = os.getcwd()
    dirLoc = "{}/data/kurly/{}/reviews".format(nowLoc, _category_id)

    try:
        dirExist = os.path.exists(dirLoc)
        if not dirExist :
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

def get_save_reviews_in_all_product_category():
    
    file_names = os.listdir('{}/data/kurly'.format(os.getcwd()))

    for category_id in file_names:
        goodsno_list = []
        with open('{}/data/kurly/{}/ids_{}.txt'.format(os.getcwd(), category_id, category_id), 'r', encoding='utf-8-sig') as f_object:
            for line in f_object:
                goodsno_list.append(line.strip())
        for goodsno in goodsno_list:
            get_save_reviews_in_single_product(category_id, goodsno)
            print("goodsno: {}'s review has been finished".format(goodsno))
            
        print("category: {}'s review has been finished".format(category_id))


    
# 상품목록을 불러오는 기능이 필요
# 리뷰 목록을 저장하는 코드 필요
# 상품 정보를 저장하는 기능도 필요할듯?