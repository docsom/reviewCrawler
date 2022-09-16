import requests
import json

def get_auth_token():
    token_url = "https://www.kurly.com/nx/api/session"
    token_response = requests.get(token_url)
    
    return json.loads(token_response.text)['accessToken']


def collect_product_info_in_single_category(_category_id, _sort_type=4):
    '''
    return type: list[json]
    '''
    
    header = {
        "authorization" : "Bearer " + get_auth_token()
    }

    isNext = True
    page = 1
    product_list = []

    while isNext == True:
        
        print("Doing Page {}".format(page))
        
        url = "https://api.kurly.com/collection/v2/home/product-categories/{}/products?sort_type={}&page={}&per_page=99".format(_category_id, _sort_type, page)
        response = requests.get(url, headers=header)
        
        if response.status_code == 200:
            response_json = json.loads(response.text)
            data = response_json['data']
            
            for product in data:
                product_list.append(product)
        
            if response_json['meta']['pagination']['current_page'] == response_json['meta']['pagination']['total_pages']:
                print("All of products in category:{} is taken.".format(_category_id))
                break
            
            page += 1
            
        else:
            print(response.status.code)
            print("There is an error while making list of products")
    
    return product_list

print(collect_product_info_in_single_category(913008))