from review_crawler import *

from product_crawler import *

from category_id_info import product_category_splited_section

from review_manager import ReviewManager

a = product_category_splited_section
a.remove(911004)
a.remove(911006)

get_save_reviews_in_certain_category(a)