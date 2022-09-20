import requests
import json
import os
from csv import DictWriter

headersCSV = [
    'no',
    'name',
    'short_description',
    'list_image_url',
    'sales_price',
    'discounted_price',
    'discount_rate',
    'is_buy_now',
    'is_purchase_status',
    'is_giftable',
    'is_only_adult',
    'is_sold_out',
    'sold_out_title',
    'sold_out_text',
    'can_restock_notify',
    'tags',
    'sticker',
    'is_multiple_price',
    'group_product',
    'product_view_status',
    'not_purchase_message',
    'delivery_type_names',    
]

def get_auth_token():
    token_url = "https://www.kurly.com/nx/api/session"
    token_response = requests.get(token_url)
    
    return json.loads(token_response.text)['accessToken']


def get_products_info_in_single_category(_category_id, _sort_type=4):
    '''
    return type: list[json]
    '''
    
    header = {
        "authorization" : "Bearer " + get_auth_token()
    }

    isNext = True
    page = 1
    product_id_list = []
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
                product_id_list.append(product['no'])
        
            if response_json['meta']['pagination']['current_page'] == response_json['meta']['pagination']['total_pages']:
                print("All of products in category:{} is taken.".format(_category_id))
                break
            
            page += 1
            
        else:
            print(response.status.code)
            print("There is an error while making list of products")
    
    return product_list, product_id_list


def get_save_products_info_in_single_category(_category_id, _sort_type=4):
    
    nowLoc = os.getcwd()
    dirLoc = "{}/data/kurly/{}".format(nowLoc, _category_id)

    try:
        dirExist = os.path.exists(dirLoc)
        if not dirExist :
            os.makedirs(dirLoc)
    except OSError:
            print("Error: Creating Dir {}".format(dirLoc))

    product_list, product_id_list = get_products_info_in_single_category(_category_id, _sort_type)

    proListLoc = "{}/info_{}".format(dirLoc, _category_id)
    proIdListLoc = "{}/ids_{}".format(dirLoc, _category_id)

    with open('{}.txt'.format(proIdListLoc), 'w', encoding='utf-8-sig') as f_object:
        for id in product_id_list:
            f_object.write(str(id)+'\n')

    with open('{}.csv'.format(proListLoc), 'a', newline='', encoding='utf-8-sig') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        dictwriter_object.writeheader()
        for i in product_list:
            dictwriter_object.writerow(i)
            
def get_save_product_info_in_all_category():

    from category_id_info import product_category_splited_section

    for goodsno in product_category_splited_section:
        get_save_products_info_in_single_category(goodsno)