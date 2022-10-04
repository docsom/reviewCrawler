from selenium import webdriver

import os
import subprocess
import json

nowLoc = os.getcwd()

def update_cookie():
    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver=webdriver.Chrome('./chromedriver.exe', options=options)

    url = 'https://www.coupang.com/'

    driver.get(url)

    all_cookies = driver.get_cookies()

    cookies_dict = {}
    for cookie in all_cookies:
        cookies_dict[cookie['name']] = cookie['value']

    now_loc = os.getcwd()
    cookies_loc = '{}/coupang/cookies.json'.format(now_loc)

    with open(cookies_loc, 'w') as f : 
        json.dump(cookies_dict, f, indent=4)

    driver.close()
    
def get_cookie():
    cookies_loc = '{}/coupang/cookies.json'.format(nowLoc)
    with open(cookies_loc, 'r') as f:
        cookies = json.load(f)
        return cookies