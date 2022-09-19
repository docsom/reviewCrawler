import os
import pandas as pd
from csv import DictWriter

class NoMoreReviewError(Exception):
    pass

headersCSV = [
    'category_id',
    'max',
    'num'
]

def init_review_manager(_category_id, _manager_loc):
    product_ids = os.listdir('{}/data/kurly/{}/reviews'.format(os.getcwd(), _category_id))
    product_ids = [id.replace(".csv", "") for id in product_ids]
    
    with open('_manager_loc', 'w', newline='', encoding="utf-8") as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        dictwriter_object.writeheader()
        for product_id in product_ids:
            
            data = pd.read_csv('{}/data/kurly/{}/reviews/{}.csv'.format(os.getcwd(), _category_id, product_id))
            data = data.review_num.apply(lambda _num: int(_num))
            _max = data.max()
            _min = data.min()
            
            temp_dict = {'category_id': _category_id, 'max': _max, 'min': _min}
            dictwriter_object.writerow(temp_dict)

class ReviewManager:
    def __init__(self, _category_id):
        now_loc = os.getcwd()
        category_loc = "{}/data/kurly/{}".format(now_loc, _category_id)
        
        category_exist = os.path.exists(category_loc)
        
        if not category_exist:
            print(category_loc)
            print("There is no category:{}, please crawl reviews first.".format(_category_id))
            raise NoMoreReviewError
        
        self.manager_loc = "{}/reviews/{}_manager.csv".format(category_loc, _category_id)
        
        manager_exist = os.path.exists(self.manager_loc)
        
        if not manager_exist:
            init_review_manager(_category_id, self.manager_loc)
        else:
            self.df = pd.read_csv(self.manager_loc)
    
    def save(self):
        self.df.to_csv(self.manager_loc, index=False, encoding="utf-8")
            
    def update_max_num(self, _product_id, max_num):
        try:
            if self.df.loc[_product_id, "max"] > max_num:
                self.df.loc[_product_id, "max"] = max_num
        except:
            print("There is no product_id:{} in ReviewManager.".format(_product_id))
            
    def update_min_num(self, _product_id, min_num):
        try:
            if self.df.loc[_product_id, "min"] < min_num:
                self.df.loc[_product_id, "min"] = min_num
        except:
            print("There is no product_id:{} in ReviewManager.".format(_product_id))