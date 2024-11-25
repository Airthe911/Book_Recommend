import pandas as pd
def process_rating_data(rating_data):
    """
    数据处理，处理原来数据中评分为0的数据。对于一条购买记录，如果该记录的评分为0，那么首先尝试用该书籍的平均得分来填充该记录；如果该书籍没有找到有效得分，则用所有书籍的平均得分来填充
    
    :param rating:需要处理的初始评分数据，至少需要包括'ISBN'(书籍编号)和'Book-Rating'(一个用户对书籍的评分)两个字段
    :return:处理过评分后的数据
    """
    rating_subdata_1 = rating_data[rating_data["Book-Rating"] != 0] # 代表原来数据中，评分已经不为0的部分数据
    rating_subdata_2 = rating_data[rating_data["Book-Rating"] == 0] # 代表原来数据中，评分为0的部分数据
    subdata_agg_1 = rating_subdata_1[["ISBN", "Book-Rating"]].groupby("ISBN").agg({"Book-Rating": "mean"}).reset_index() # 有评分书籍的平均分
    avg_rating_dict = dict(zip(subdata_agg_1["ISBN"].tolist(), subdata_agg_1["Book-Rating"].tolist()))
    rating_subdata_2["Book-Rating"] = rating_subdata_2["ISBN"].map(avg_rating_dict) # 有正常评分记录的书籍，用这本书的平均分填充
    rating_subdata_2["Book-Rating"].fillna(rating_subdata_1["Book-Rating"].mean(), inplace=True) # 否则用所有书的平均分填充
    fixed_rating_data = pd.concat([rating_subdata_1, rating_subdata_2])
    fixed_rating_data.sort_values(by="ISBN", inplace=True)
    fixed_rating_data.reset_index(drop=True, inplace=True)
    return rating_data