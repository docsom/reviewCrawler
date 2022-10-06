import os
import pandas as pd

now_loc = os.getcwd()
coup_loc = '{}/data/coupang'.format(now_loc)

class NoSuchFileError(Exception):
    pass

def remove_duplicated_reviews_in_single_product(category_id, product_id):
    review_loc = '{}/{}/reviews/{}'.format(coup_loc, category_id, product_id)
    reviewExist = os.path.exists(review_loc)
    if reviewExist == False:
        raise NoSuchFileError
    try:
        reviews = pd.read_csv(review_loc)
        print(len(reviews))
        reviews = reviews.drop_duplicates('review_id').reset_index(drop=True)
        print(len(reviews))
    except:
        pass