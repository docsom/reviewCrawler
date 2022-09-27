from review_crawler_requests import *
from category_id_info import *
from product_crawler import *

#category_list = product_category_splited_section
#get_save_products_info_in_given_categories(category_list)

category_id = 225481
target_products = get_target_products_info_in_single_category(category_id)
print(len(target_products))

target_products = [a for a in target_products if (a[0] != 206820279 and a[0] != 4567751809 and a[0] != 290174474  and a[0] != 1577222388  and a[0] != 6079766075  and a[0] != 6079767106  and a[0] != 60386712105)]
print(len(target_products))
#get_save_reviews_in_given_products(category_id, target_products)