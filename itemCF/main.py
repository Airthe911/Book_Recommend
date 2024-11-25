import pandas as pd
from data_processer import process_rating_data
from itemcf import item_base_CF

rating_data = pd.read_csv("../minidata/Ratings.csv") # 读取初始评分数据
fixed_rating_data = process_rating_data(rating_data) # 处理评分数据
recommend_result = item_base_CF(target_book_id="000649840X", rating_data=fixed_rating_data)
print(recommend_result)