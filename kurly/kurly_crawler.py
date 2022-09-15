import requests
from bs4 import BeautifulSoup

class NoMoreReviewError(Exception):
    pass

goodsno = 5156999

def extract_review_info(_goodsno, _page):
    url = "https://www.kurly.com/shop/goods/goods_review_list.php?goodsno={}&page={}".format(_goodsno, _page)

    response = requests.get(url)

    if response.status_code == 200:
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
            
            #print( "#", review_num, "#", review_title,  "#", review_user_grade,  "#", review_user_name,  "#", review_time,  "#", review_like_cnt, "#")
            #print("#", product_name, "#", review_text)
    else:
        print(response.status.code)

def extract_review_single_product(_goodsno):
    page = 1
    while 1:
        try:
            extract_review_info(_goodsno, page)
        except NoMoreReviewError:
            print("Every Review is Sorted in goodsno:{}".format(_goodsno))
            break
        page += 1
        
extract_review_single_product(goodsno)