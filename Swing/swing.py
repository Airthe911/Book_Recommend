import pandas as pd
import numpy as np
from itertools import combinations

def swing_CF(target_book_id, data):
    """
    自己实现的基于Swing算法的协同过滤推荐，输入用户购物历史，返回用户推荐结果

    :param target_book_id:目标书籍的ISBN
    :param data:用户-书籍购买记录
    :return:推荐的结果
    """
    target_book_users = set(data[data["ISBN"] == target_book_id]["User-ID"].unique())
    similar_dict = {} # 用于保存结果
    alpha = 0.5
    # 2.遍历其他所有的物品
    for other_book_id, group in data.groupby("ISBN"):
        other_book_users = set(group["User-ID"].unique())
        # 3.a.找出同时点击过target物品和other物品的用户。在我们的数据里，即为找出所有购买过target和other的人
        common_users = target_book_users & other_book_users
        user_pair_list = list(combinations(common_users, 2))
        if len(user_pair_list) == 0:
            similar_dict[other_book_id] = 0
            continue
        # 找到每个用户的买过物品的集合
        user2books_dict = {}
        for one_user in common_users:
            user2books_dict[one_user] = set(data[data["User-ID"] == one_user]["ISBN"].unique())
        # 3.b.将找到的用户两两组合，按上述公式计算target和other的相似度
        swing_similarity = 0
        for user_pair in user_pair_list:
            user_1, user_2 = user_pair
            swing_similarity += (1 / np.sqrt(len(user2books_dict[user_1]))) * (1 / np.sqrt(len(user2books_dict[user_2]))) * (
                1 / (alpha + len(user2books_dict[user_1] & user2books_dict[user_2]))
            )
        similar_dict[other_book_id] = swing_similarity
    sorted_similar_books = [item[0] for item in sorted(similar_dict.items(), key=lambda x: x[1], reverse=True)]
    sorted_similar_books.remove(target_book_id)
    # 将与目标书籍相似度top20的书，推荐给购买过target的用户
    top_list = sorted_similar_books[:20]
    result_user_ls = []
    result_book_ls = []
    for one_user in target_book_users:
        result_user_ls.extend([one_user for _ in range(20)])
        result_book_ls.extend(top_list)
    recommend_result = pd.DataFrame({"User-ID": result_user_ls, "ISBN": result_book_ls})
    return recommend_result