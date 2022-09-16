import requests
from bs4 import BeautifulSoup
import json

category_id = 914004
sort_type = 4
token_url = "https://www.kurly.com/nx/api/session"

token_response = requests.get(token_url)
header = {
    "authorization" : "Bearer " + json.loads(token_response.text)['accessToken']
}


url = "https://api.kurly.com/collection/v2/home/product-categories/{}/products?sort_type={}&page=1&per_page=99".format(category_id, sort_type)

# header={
#     'session_id' : "1098390459594528453",
#     'identity_id' : "1098390459603534135",
#     'identity' : "436a7271-0ae6-4015-a22a-e12f550d4158",
#     'link' : "https://we.kurly.com/a/key_live_meOgzIdffiVWvdquf7Orkacksxa2LneN?%24identity_id=1098390459603534135",
    
# }

response = requests.get(url, headers=header)

#https://www.kurly.com/nx/api/session

print(response.text)