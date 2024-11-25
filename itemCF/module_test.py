import pandas as pd
from data_processer import process_rating_data
from itemcf import item_base_CF
from sklearn.model_selection import train_test_split

rating_data = pd.read_csv("../minidata/Ratings.csv") # 读取初始评分数据
fixed_rating_data = process_rating_data(rating_data) # 处理评分数据
train_rating_data, test_rating_data = train_test_split(fixed_rating_data, test_size=0.2, random_state=42)
pred_recommend_result = item_base_CF(target_book_id="000649840X", rating_data=train_rating_data)
# 处理一下推荐数据，如果某个用户只在test_rating_data里面有，而train_rating_data里面没有，则不考虑这部分用户的购买行为。
test_rating_data = test_rating_data[test_rating_data["User-ID"].isin(set(train_rating_data['User-ID']))]
real_target_buyers = test_rating_data[test_rating_data["ISBN"] == "000649840X"]["User-ID"].unique()
# 类似的，如果推荐结果的用户在test_rating_data里面没有，则去掉这个结果
test_user_set = set(test_rating_data["User-ID"])
for pred_user in pred_recommend_result:
    if pred_user not in test_user_set:
        pred_recommend_result.remove(pred_user)
hit_cnt = 0
for one_real_buyer in real_target_buyers:
    if one_real_buyer in pred_recommend_result:
        hit_cnt += 1
print("算法尝试向{}个用户推荐目标书籍。在测试集上，共有{}个人购买该书籍，其中{}个人得到了算法的推荐".format(len(pred_recommend_result), len(real_target_buyers), hit_cnt))
print("推荐精确率(P)为{:2%}, 推荐召回率(R)为{:2%}".format(hit_cnt / len(pred_recommend_result), hit_cnt / len(real_target_buyers)))