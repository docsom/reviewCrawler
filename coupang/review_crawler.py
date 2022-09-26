#https://msgoel.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%81%AC%EB%A1%A4%EB%A7%81-%EC%BF%A0%ED%8C%A1-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%B0%A8%EB%8B%A8-%EC%A0%91%EC%86%8D-%EA%B1%B0%EB%B6%80-Access-Denied-%EB%AC%B8%EC%A0%9C-%ED%95%B4%EA%B2%B0-%EB%B0%A9%EB%B2%95

# this one is for Selenium
# If I find route only with requests, I'll move to it.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import os
import subprocess
import time
import random
import shutil
from csv import DictWriter
import pandas as pd

nowLoc = os.getcwd()

max_num_review = 60
min_text_len = 50

headersCSV = [
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

def rantime(_min = 0., _max = 1.):
    num = random.random()
    return _min + num * (_max - _min)


def judge_value_of_review(_text):
    '''
    input: str(review's text)
    output: boolean(if quality is good True else False)
    '''
    if _text == None:
        return False
    
    if len(_text) >= min_text_len:
        return True
    else:
        return False
    
    
def extract_review_info(_element, _product_id=None):
    '''
    input: html element
    output: python dictionary
    '''
    elementHTML = _element.get_attribute('outerHTML')
    review_html = BeautifulSoup(elementHTML, "lxml").select('html > body > article')
    
    reviewer_html = review_html[0].select('article > div > div')
    
    review_user_name = reviewer_html[1].get_text().strip()
    review_user_grade = reviewer_html[2].select('div > div > div > div')[0]['data-rating']
    review_time = reviewer_html[2].select('div > div > div')[2].get_text().strip()
    product_name = reviewer_html[4].get_text().strip()
    review_title = review_html[0].select_one('article > div.sdp-review__article__list__headline')
    review_title = review_title.get_text().strip() if review_title != None else None
    review_text = review_html[0].select_one('article > div.sdp-review__article__list__review')
    review_text = review_text.get_text().strip() if review_text != None else None
    review_survey = review_html[0].select_one('article > div.sdp-review__article__list__survey')
    review_survey = review_survey.get_text().strip() if review_survey != None else None
    review_help_cnt = review_html[0].select_one('article > div.sdp-review__article__list__help')
    review_help_cnt = review_help_cnt['data-count'] if review_help_cnt != None else None
    
    review_dict = {
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


def extract_review_info_in_single_page(_elements, _product_id = None):
    '''
    input: list[html element, html element...]
    output: list[dict, dict...], boolean
    '''
    should_stop = True
    reviews_info = []
    for review_html in _elements:
        review_info = extract_review_info(review_html, _product_id)
        if judge_value_of_review(review_info['review_text']) == True:
            reviews_info.append(review_info)
        else:
            should_stop = False
    
    return reviews_info, should_stop

def save_reviews(_category_id, _product_id, _review_list):
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
    
category_id = 502382
product_id = 1717552921
url = "https://www.coupang.com/vp/products/{}?itemId=2923167957&vendorItemId=70911802261&sourceType=CATEGORY&categoryId={}&isAddedCart=".format(product_id, category_id)

subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver=webdriver.Chrome('./chromedriver.exe', options=options)
#driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.implicitly_wait(3)

driver.get(url)
time.sleep(rantime(2.3, 2.7))

driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)

time.sleep(rantime(0.4, 0.6))

driver.find_element(By.XPATH, '//*[@id="btfTab"]/ul[1]/li[2]').click()

reviews_html = driver.find_elements(By.XPATH, '//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/article')


reviews_single_page, should_stop = extract_review_info_in_single_page(reviews_html)

driver.implicitly_wait(3)
time.sleep(rantime(1.1, 1.32))

#if should_stop == False:
#   break

buttons_xpath = '//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button'
num_buttons = len(driver.find_elements(By.XPATH, buttons_xpath))

save_reviews(category_id, product_id, reviews_single_page)

num_review = 5
flag = True

while(1):
    for aaa in range(3, num_buttons+1):
        time.sleep(rantime(1.5, 2.0))
        driver.find_element(By.XPATH, '{}[{}]'.format(buttons_xpath, aaa)).click()
        time.sleep(rantime(1.9, 2.35))
        reviews_html = driver.find_elements(By.XPATH, '//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/article')
        reviews_single_page, should_stop = extract_review_info_in_single_page(reviews_html)
        
        save_reviews(category_id, product_id, reviews_single_page)
        
        if should_stop == False:
            flag = False
            break
        
        if num_review >= max_num_review:
            flag = False
            break
        
        num_review += 5
    if flag == False:
        break
    

    
driver.close()