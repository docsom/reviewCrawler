# log에서 정보를 뽑아내서 뭐 done으로 표시된 애들은 싹 다 타겟에서 지우는 뭐 그런거 해봐
# log에서 error가 떴을 경우에 해당 카테고리를 지우는 프로그램도 좀 만들어봐 이거 하나하나 지우기 힘드니까

# 도커에서 안돌아가는거 방안 좀 생각해봐
# 마켓컬리 데이터 집어넣고 컨플에 정리해
import os
import pandas as pd
#hi
now_loc = os.getcwd()
coup_loc = '{}/data/coupang'.format(now_loc)
    
def extract_info_in_reviews_csv(category_id, product_id):
    product_loc = '{}/{}/reviews/{}.csv'.format(coup_loc, category_id, product_id)
    try:
        reviews = pd.read_csv(product_loc)
        orig_num_reviews = len(reviews)
        reviews.drop_duplicates('review_id', inplace = True)
        num_total_reviews = len(reviews)
        num_by_rating = [0]
        for i in range(1, 6):
            num_by_rating.append(len(reviews.loc[reviews.review_user_grade == i]))

        info_dict = {
            'category_id' : category_id,
            'product_id' : product_id,
            'total_review_num' : num_total_reviews,
            'duplicated_num' : orig_num_reviews - num_total_reviews,
            'num_by_rating' : num_by_rating
        }
        return info_dict
    
    except FileNotFoundError:
        info_dict = {
            'category_id' : category_id,
            'product_id' : product_id,
            'total_review_num' : 0,
            'duplicated_num' : 0,
            'num_by_rating' : [0, 0, 0, 0, 0, 0]
        }
        return info_dict
        

def extract_info_in_single_category(category_id):
    std_products_loc = '{}/{}/{}.csv'.format(coup_loc, category_id, category_id)
    if os.path.isfile(std_products_loc) == False:
        print('No Product_List of Single Category: {}'.format(category_id))
        raise FileNotFoundError
    
    std_products = pd.read_csv(std_products_loc).product_id.drop_duplicates().reset_index(drop=True)
    now_reviews_loc = '{}/{}/reviews'.format(coup_loc, category_id)
    if os.path.isdir(now_reviews_loc):
        now_products =[id.rstrip('.csv') for id in os.listdir(now_reviews_loc)]
        ratings_num = [0, 0, 0, 0, 0, 0]
        total_review_num = 0
        each_product_info = []
        for product_id in now_products:
            product_info = extract_info_in_reviews_csv(category_id, product_id)
            each_product_info.append(product_info)
            total_review_num += product_info['total_review_num']
            for i in range(1, 6):
                ratings_num[i] += product_info['num_by_rating'][i]
            
        info_dict = {
            'category_id' : category_id,
            'target_num_of_products' : len(std_products),
            'got_num_of_products' : len(now_products),
            'total_review_num' : total_review_num,
            'num_by_rating' : ratings_num,
            'each_product_info' : each_product_info
        }
        return info_dict
    
    else:
        info_dict = {
            'category_id' : category_id,
            'target_num_of_products' : len(std_products),
            'got_num_of_products' : 0,
            'total_review_num' : 0,
            'num_by_rating' : [0,0,0,0,0,0],
            'each_product_info' : []
        }
        return info_dict
        
def extract_info_in_all_category():
    categories = os.listdir(coup_loc)
    categories.remove('log.csv')
    ratings_num = [0, 0, 0, 0, 0, 0]
    target_num_of_products = 0
    got_num_of_products = 0
    total_review_num = 0
    each_category_info = []
    for category_id in categories:
        category_info = extract_info_in_single_category(category_id)
        target_num_of_products += category_info['target_num_of_products']
        got_num_of_products += category_info['got_num_of_products']
        total_review_num += category_info['total_review_num']
        for i in range(1, 6):
            ratings_num[i] += category_info['num_by_rating'][i]
        
        each_category_info.append(category_info)
    
    info_dict = {
        'target_num_of_products': target_num_of_products,
        'got_num_of_products': got_num_of_products,
        'total_review_num' : total_review_num,
        'num_by_rating' : ratings_num,
        'each_category_info' : each_category_info
    }
    return info_dict

print(extract_info_in_all_category()['got_num_of_products'])

print(extract_info_in_all_category()['total_review_num'])

print(extract_info_in_all_category()['num_by_rating'])