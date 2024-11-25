# 由于正常的数据量过大，学习时可以采用小数据集。为了使得数据相对更稠密，选择采样出原数据中销量最高的5000本书，及其对应的用户在这些书上的购买记录
import pandas as pd
book_data = pd.read_csv("../data/Books.csv")
rating_data = pd.read_csv("../data/Ratings.csv")
user_data = pd.read_csv("../data/Users.csv")
# 找出书籍销量前5000名的书
book_cnt_data = rating_data[["ISBN", "Book-Rating"]].groupby("ISBN").agg({"Book-Rating": "count"}).rename(columns={"Book-Rating": "Book-Count"}).sort_values(by="Book-Count", ascending=False).reset_index()
mini_book_cnt = book_cnt_data.loc[:5000-1, :]
# 利用这5000本书来对rating_data和book_data进行采样
mini_rating_data = pd.merge(rating_data, mini_book_cnt, how="inner", on="ISBN")
mini_book_data = pd.merge(book_data, mini_book_cnt, how="inner", on="ISBN")
# 寻找这5000个书的所有买家，并利用这些买家对user_data进行采用
mini_user_cnt = mini_rating_data[["User-ID", "Book-Rating"]].groupby("User-ID").agg({"Book-Rating": "count"}).rename(columns={"Book-Rating": "User-Count"}).sort_values(by="User-Count", ascending=False).reset_index()
mini_user_data = pd.merge(user_data, mini_user_cnt, how="inner", on="User-ID")
mini_rating_data.reset_index(drop=True, inplace=True)
mini_book_data.reset_index(drop=True, inplace=True)
mini_user_data.reset_index(drop=True, inplace=True)
mini_book_data = mini_book_data.drop(['Book-Count'], axis=1, inplace=False)
mini_rating_data = mini_rating_data.drop(['Book-Count'], axis=1, inplace=False)
mini_user_data = mini_user_data.drop(['User-Count'], axis=1, inplace=False)
mini_book_data.to_csv("../minidata/Books.csv", index=False)
mini_rating_data.to_csv("../minidata/Ratings.csv", index=False)
mini_user_data.to_csv("../minidata/Users.csv", index=False)
print("采样前，共有{}条评分记录，采样后有{}条评分记录".format(rating_data.shape[0], mini_rating_data.shape[0]))
print("采样前，共有{}本书，采样后有{}本书".format(book_data.shape[0], mini_book_data.shape[0]))
print("采样前，共有{}个用户，采样后有{}个用户".format(user_data.shape[0], mini_user_data.shape[0]))