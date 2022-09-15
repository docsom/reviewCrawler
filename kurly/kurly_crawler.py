import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen


first_page = 1
end_page = 10

goodsno = 5114889
page = 2
url = "https://www.kurly.com/shop/goods/goods_review_list.php?goodsno={}&page={}".format(goodsno, page)

response = requests.get(url)


if response.status_code == 200:
    html = response.text
    bsObject = BeautifulSoup(html, "lxml")
    
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
        
        
        #print( "#", review_num, "#", review_title,  "#", review_user_grade,  "#", review_user_name,  "#", review_time,  "#", review_like_cnt, "#")
        break
else:
    print(response.status.code)

