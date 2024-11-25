#import numpy as np
import pandas as pd

rate_data = pd.read_csv("../data/Ratings.csv")

#print(rate_data.head())#查看前5行数据
#print(rate_data.shape)#查看几行几列
#sub_data = rate_data[rate_data["Book-Rating"]==0]#选出评分为0的数据给sub_data
#sub_data.reset_index(drop=True, inplace=True)#重设sub_data索引
#print(sub_data)
#print(rate_data["User-ID"].value_counts())#统计rate_data中User_ID列的不同值的个数
#print(rate_data["ISBN"].value_counts())#统计rate_data中User_ID列的不同值的个数
book_avg_rate = rate_data[rate_data["Book-Rating"]!=0].groupby('ISBN')['Book-Rating'].mean().reset_index(name='ISBN_avg_rate')#计算每本书被给的的平均分
user_avg_rate = rate_data[rate_data["Book-Rating"]!=0].groupby('User-ID')['Book-Rating'].mean().reset_index(name='user_avg_rate')#计算每个用户给出的平均分
#print(book_avg_rate)
#print(user_avg_rate)
rate_data = rate_data.merge(book_avg_rate, on='ISBN',how="left")#增加书的平均分列
rate_data = rate_data.merge(user_avg_rate, on='User-ID',how="left")#增加用户的平均分列
rate_data = rate_data.fillna(0)
#print(rate_data)
rate_data.loc[rate_data["Book-Rating"] == 0, "Book-Rating"] = rate_data.loc[rate_data["Book-Rating"] == 0, "user_avg_rate"]#用用户的平均分替换0分
rate_data.loc[rate_data["Book-Rating"] == 0, "Book-Rating"] = rate_data.loc[rate_data["Book-Rating"] == 0, "ISBN_avg_rate"]#再用书的平均分替换用户全给的0分
#print(rate_data)
rate_data.drop(columns="user_avg_rate", inplace=True)#删除用户平均分列
rate_data.drop(columns="ISBN_avg_rate", inplace=True)#删除书平均分列
print(rate_data)
#print((rate_data["Book-Rating"] == '0').sum())#统计0个数


