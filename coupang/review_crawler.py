#https://waytothem.com/blog/163/

#from multiprocessing import Pool

#pepp8 해보기 control k f

#https://www.coupang.com/vp/products/1717552921/items/2923167957/vendoritems/70911802261
import json
from bs4 import BeautifulSoup
import requests
import os

nowLoc = os.getcwd()
with open("{}/Coupang/Headers.json".format(nowLoc), 'r') as f_object:
    headers = json.load(f_object)
class Coupang:
    def get_product_code(self, url):
        prod_code = url.split('products/')[-1].split('?')[0]
        return prod_code
    
    def __init__(self):
        self.__headers = headers['headers']
        
    def main(self):
        
        #URL = self.input_review_url()
        URL = "https://www.coupang.com/vp/products/6638786505?itemId=15167378523&vendorItemId=82388756551&sourceType=cmgoms&isAddedCart="
        
        prod_code = self.get_product_code(url=URL)
    
        URLS = [f'https://www.coupang.com/vp/product/reviews?productId={prod_code}&amp;page={page}&amp;size=5&amp;sortBy=ORDER_SCORE_ASC&amp;ratings=&amp;q=&amp;viRoleCode=3&amp;ratingSummary=true' for page in range(1,1 + 1)]

        
        self.__headers['referer'] = URL

        print(self.__headers)

        with requests.Session() as session:
            [self.fetch(url=url,session=session) for url in URLS]

        print("hi")
        return None
        
    def fetch(self,url,session):
        print("fetch")
        with session.get(url=url,headers=self.__headers) as response:
            print("response")
            html = response.text
            soup = BeautifulSoup(html,'html.parser')
            print(soup.prettify())
            
coupang = Coupang()
coupang.main()

