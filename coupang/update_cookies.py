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
import json

subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver=webdriver.Chrome('./chromedriver.exe', options=options)

url = 'https://www.coupang.com/'

driver.get(url)

all_cookies = driver.get_cookies()
print(all_cookies)

cookies_dict = {}
for cookie in all_cookies:
    cookies_dict[cookie['name']] = cookie['value']

now_loc = os.getcwd()
cookies_loc = '{}/coupang/cookies.json'.format(now_loc)

with open(cookies_loc, 'w') as f : 
	json.dump(cookies_dict, f, indent=4)

driver.close()