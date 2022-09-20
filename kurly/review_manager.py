import os
import pandas as pd
from csv import DictWriter

class NoMoreReviewError(Exception):
    pass

headersCSV = [
    'category_id',
    'product_id',
    'max',
    'min'
]

def init_review_manager(_category_id, _manager_loc):
    product_ids = os.listdir('{}/data/kurly/{}/reviews'.format(os.getcwd(), _category_id))
    product_ids = [id.replace(".csv", "") for id in product_ids]
    
    with open(_manager_loc, 'w', newline='', encoding="utf-8") as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        dictwriter_object.writeheader()
        for product_id in product_ids:
            
            data = pd.read_csv('{}/data/kurly/{}/reviews/{}.csv'.format(os.getcwd(), _category_id, product_id))
            data = [int(id) for id in data.review_num if id.isdigit()]
            _max = max(data)
            _min = min(data)
            
            temp_dict = {'category_id': _category_id, 'product_id': product_id, 'max': _max, 'min': _min}
            dictwriter_object.writerow(temp_dict)

class ReviewManager:
    def __init__(self, _category_id):
        
        self.category_id = _category_id
        now_loc = os.getcwd()
        category_loc = "{}/data/kurly/{}".format(now_loc, _category_id)
        
        category_exist = os.path.exists(category_loc)
        
        if not category_exist:
            print(category_loc)
            print("There is no category:{}, please crawl reviews first.".format(_category_id))
            raise NoMoreReviewError
        
        self.manager_loc = "{}/{}_review_manager.csv".format(category_loc, _category_id)
        
        manager_exist = os.path.exists(self.manager_loc)
        
        if not manager_exist:
            init_review_manager(_category_id, self.manager_loc)
        else:
            self.df = pd.read_csv(self.manager_loc)
            
    def info(self):
        product_num = 0
        review_num = 0
        for _, row in self.df.iterrows():
            product_num += 1
            temp = row[2] - row[3] + 1
            review_num += temp
        print("Category: {}, # of Product: {}, # of Review: {}".format(self.category_id, product_num, review_num))
    
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
            
    def get_max_min_of_product_id(self, _product_id):
        return self.df.loc[_product_id, "max"], self.df.loc[_product_id, "min"]