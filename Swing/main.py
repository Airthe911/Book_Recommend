import pandas as pd
from swing import swing_CF

rating_data = pd.read_csv("../minidata/Ratings.csv") # 读取初始评分数据
recommend_result = swing_CF(target_book_id="000649840X", data=rating_data[["User-ID", "ISBN"]])
print(recommend_result)