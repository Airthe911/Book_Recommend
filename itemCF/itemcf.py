import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

def item_base_CF(target_book_id, rating_data):
    """
    自己实现的基于物品相似度的协同过滤推荐，仅适用于规模不太大的数据集。输入目标书籍id，以及用户-书籍评分数据，返回用户推荐列表，可将这本书推荐给这些用户

    :param target_book_id:目标书籍的ISBN
    :param rating_data:用户-书籍评分数据
    :return:可将这本书推荐至的用户列表
    """
    # 构造User-book矩阵，随后构建稀疏矩阵，计算相似度
    user_book_matrix = rating_data.pivot(index="User-ID", columns="ISBN", values="Book-Rating").fillna(0)
    sparse_matrix = csr_matrix(user_book_matrix.values)
    book_similarity_matrix = pd.DataFrame(cosine_similarity(sparse_matrix.T), index=user_book_matrix.columns, columns=user_book_matrix.columns)
    target_book_avg_score = rating_data[rating_data["ISBN"] == target_book_id]["Book-Rating"].mean()
    agg_data = rating_data[["ISBN", "Book-Rating"]].groupby("ISBN").agg({"Book-Rating": "mean"}).reset_index() # 每个书籍的平均分
    avg_rating_dict = dict(zip(agg_data["ISBN"].tolist(), agg_data["Book-Rating"].tolist()))
    # 找出与该书籍最相关的几个书籍
    similar_dict = dict(zip(user_book_matrix.columns, book_similarity_matrix[target_book_id].tolist()))
    sorted_similar_dict = sorted(similar_dict.items(), key=lambda x: x[1], reverse=True)
    # 根据最相关的前20本书进行推荐
    selected_book_ids = [item[0] for item in sorted_similar_dict[:21]]
    selected_book_ids.remove(target_book_id)
    selected_book_df = pd.DataFrame({"ISBN": selected_book_ids, "cos_similarity": [similar_dict[book_id] for book_id in selected_book_ids],
                                    "avg_score": [avg_rating_dict[book_id] for book_id in selected_book_ids]})
    # 首先筛选出在这20本书上有购买记录的user做为备选
    sub_fixed_rating_data = pd.merge(rating_data, selected_book_df, how="inner", on="ISBN")
    # 预先计算好用户对书籍的评分-该书籍的平均分
    sub_fixed_rating_data["rating_diff"] = sub_fixed_rating_data["Book-Rating"] - sub_fixed_rating_data["avg_score"]
    user_recommended = []
    for user_id, group in sub_fixed_rating_data.groupby("User-ID"):
        # 计算该用户对目标书籍的预估得分
        score_pred = target_book_avg_score + ((group["cos_similarity"] * group["rating_diff"]).sum()) / group["cos_similarity"].sum()
        # 如果该用户对目标书籍的预估评分大于该用户以前给出的评分的平均值，则将该书籍推荐给这个用户
        user_avg_score = rating_data[rating_data["User-ID"] == user_id]["Book-Rating"].mean()
        if score_pred >= user_avg_score:
            user_recommended.append(user_id)
    # 修正结果，如果推荐列表中有人已经购买过该书籍，则去除这些人，以避免重复无效推荐
    buyer_list = rating_data[rating_data["ISBN"] == target_book_id]["User-ID"].tolist()
    for one_user in user_recommended:
        if one_user in buyer_list:
            user_recommended.remove(one_user)
    return user_recommended