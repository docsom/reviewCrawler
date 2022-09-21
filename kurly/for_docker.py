from review_crawler import get_save_reviews_in_single_category

from product_crawler import get_save_product_info_in_all_category



from review_manager import ReviewManager

category_id = 911006

reviewManager = ReviewManager(category_id)
reviewManager.info()

get_save_reviews_in_single_category(category_id)