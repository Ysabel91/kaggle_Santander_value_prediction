# coding: utf-8
"""
检查数据分布基本情况
"""

##==================== Package ====================##
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import seaborn as sns
from scipy import stats
import pickle  # to store temporary variable

##==================== File-Path (fp) ====================##
## raw data (for read)
fp_train = "../data/train.csv"
fp_test = "../data/test.csv"

## and setting rare categories' value to 'other' (feature filtering)
fp_train_f = "../data/train_f.csv"
fp_test_f = "../data/test_f.csv"

fp_config = "../data/config.txt"


##==================== pre-Processing ====================##

## data reading
df_train_ini = pd.read_csv(fp_train, nrows=10)
df_train_org = pd.read_csv(fp_train)
# df_test_org = pd.read_csv(fp_test)
# print("Train rows and columns : ", df_train_org.shape)
# print("Test rows and columns : ", df_test_org.shape)


# 检查缺失值情况(无缺失)
na_count = df_train_org.isnull().sum(axis=0).reset_index()
na_count.columns = ['feature', 'na_count']
na_count = na_count[na_count['na_count']>0]
na_count = na_count.sort_values(by='na_count')
print(na_count)

# 检查特征类型
feature_type = df_train_org.dtypes.reset_index()
feature_type.columns = ['feature_count', 'type']
feature_type = feature_type.groupby('type')
#groupby之后的数据并不是DataFrame格式的数据，而是特殊的groupby类型，此时，可以通过size()方法返回分组后的记录数目统计结果
print(feature_type.size())


# 检查特征是否唯一
unique_df = df_train_org.nunique().reset_index()
unique_df.columns = ["col_name", "unique_count"]
constant_df = unique_df[unique_df["unique_count"]==1]
print(constant_df.shape)
# 检测到变量唯一的特征，可从训练数据中剔除
constant_feature_dict = {"constant_feature": constant_df['col_name'].tolist()}
with open(fp_config, "a+") as file:
    file.write(str(constant_feature_dict))



# 查看目标分布（排序后查看是否有离群点）
plt.figure(figsize=(8,6))
plt.scatter(range(df_train_org.shape[0]), np.sort(df_train_org['target'].values))
plt.xlabel('index', fontsize=12)
plt.ylabel('Target', fontsize=12)
plt.title("Target Distribution", fontsize=14)
plt.show()

# 查看直方图，数据是否正态分布
plt.figure(figsize=(12,8))
sns.distplot(df_train_org["target"].values, bins=50, kde=False)
plt.xlabel('Target', fontsize=12)
plt.title("Target Histogram", fontsize=14)
plt.show()

# 发现数据右偏，对数据进行对数处理
plt.figure(figsize=(12,8))
sns.distplot(np.log1p(df_train_org["target"].values), bins=50, kde=False)
plt.xlabel('Target', fontsize=12)
plt.title("Log of Target Histogram", fontsize=14)
plt.show()

with open(fp_config, "r", encoding='utf-8') as file:
    import json
    content = json.load(file)
    drop_cols = content.get("constant_feature")
    print(u"drop content is {}".format(drop_cols))

drop_cols = ['d5308d8bc', 'c330f1a67', 'eeac16933', '7df8788e8', '5b91580ee', '6f29fbbc7', '46dafc868', 'ae41a98b6', 'f416800e9', '6d07828ca', '7ac332a1d', '70ee7950a', '833b35a7c', '2f9969eab', '8b1372217', '68322788b', '2288ac1a6', 'dc7f76962', '467044c26', '39ebfbfd9', '9a5ff8c23', 'f6fac27c8', '664e2800e', 'ae28689a2', 'd87dcac58', '4065efbb6', 'f944d9d43', 'c2c4491d5', 'a4346e2e2', '1af366d4f', 'cfff5b7c8', 'da215e99e', '5acd26139', '9be9c6cef', '1210d0271', '21b0a54cb', 'da35e792b', '754c502dd', '0b346adbd', '0f196b049', 'b603ed95d', '2a50e001c', '1e81432e7', '10350ea43', '3c7c7e24c', '7585fce2a', '64d036163', 'f25d9935c', 'd98484125', '95c85e227', '9a5273600', '746cdb817', '6377a6293', '7d944fb0c', '87eb21c50', '5ea313a8c', '0987a65a1', '2fb7c2443', 'f5dde409b', '1ae50d4c3', '2b21cd7d8', '0db8a9272', '804d8b55b', '76f135fa6', '7d7182143', 'f88e61ae6', '378ed28e0', 'ca4ba131e', '1352ddae5', '2b601ad67', '6e42ff7c7', '22196a84c', '0e410eb3d', '992e6d1d3', '90a742107', '08b9ec4ae', 'd95203ded', '58ad51def', '9f69ae59f', '863de8a31', 'be10df47c', 'f006d9618', 'a7e39d23d', '5ed0abe85', '6c578fe94', '7fa4fcee9', '5e0571f07', 'fd5659511', 'e06b9f40f', 'c506599c8', '99de8c2dc', 'b05f4b229', '5e0834175', 'eb1cc0d9c', 'b281a62b9', '00fcf67e4', 'e37b65992', '2308e2b29', 'c342e8709', '708471ebf', 'f614aac15', '15ecf7b68', '3bfe540f1', '7a0d98f3c', 'e642315a5', 'c16d456a7', '0c9b5bcfa', 'b778ab129', '2ace87cdd', '697a566f0', '97b1f84fc', '34eff114b', '5281333d7', 'c89f3ba7e', 'cd6d3c7e6', 'fc7c8f2e8', 'abbbf9f82', '24a233e8f', '8e26b560e', 'a28ac1049', '504502ce1', 'd9a8615f3', '4efd6d283', '34cc56e83', '93e98252a', '2b6cef19e', 'c7f70a49b', '0d29ab7eb', 'e4a0d39b7', 'a4d1a8409', 'bc694fc8f', '3a36fc3a2', '4ffba44d3', '9bfdec4bc', '66a866d2f', 'f941e9df7', 'e7af4dbf3', 'dc9a54a3e', '748168a04', 'bba8ce4bb', 'ff6f62aa4', 'b06fe66ba', 'ae87ebc42', 'f26589e57', '963bb53b1', 'a531a4bf0', '9fc79985d', '9350d55c1', 'de06e884c', 'fc10bdf18', 'e0907e883', 'c586d79a1', 'e15e1513d', 'a06067897', '643e42fcb', '217cd3838', '047ebc242', '9b6ce40cf', '3b2c972b3', '17a7bf25a', 'c9028d46b', '9e0473c91', '6b041d374', '783c50218', '19122191d', 'ce573744f', '1c4ea481e', 'fbd6e0a0b', '69831c049', 'b87e3036b', '54ba515ee', 'a09ba0b15', '90f77ec55', 'fb02ef0ea', '3b0cccd29', 'fe9ed417c', '589e8bd6f', '17b5a03fd', '80e16b49a', 'a3d5c2c2a', '1bd3a4e92', '611d81daa', '3d7780b1c', '113fd0206', '5e5894826', 'cb36204f9', 'bc4e3d600', 'c66e2deb0', 'c25851298', 'a7f6de992', '3f93a3272', 'c1b95c2ec', '6bda21fee', '4a64e56e7', '943743753', '20854f8bf', 'ac2e428a9', '5ee7de0be', '316423a21', '2e52b0c6a', '8bdf6bc7e', '8f523faf2', '4758340d5', '8411096ec', '9678b95b7', 'a185e35cc', 'fa980a778', 'c8d90f7d7', '080540c81', '32591c8b4', '5779da33c', 'bb425b41e', '01599af81', '1654ab770', 'd334a588e', 'b4353599c', '51b53eaec', '2cc0fbc52', '45ffef194', 'c15ac04ee', '5b055c8ea', 'd0466eb58', 'a80633823', 'a117a5409', '7ddac276f', '8c32df8b3', 'e5649663e', '6c16efbb8', '9118fd5ca', 'ca8d565f1', '16a5bb8d2', 'fd6347461', 'f5179fb9c', '97428b646', 'f684b0a96', 'e4b2caa9f', '2c2d9f267', '96eb14eaf', 'cb2cb460c', '86f843927', 'ecd16fc60', '801c6dc8e', 'f859a25b8', 'ae846f332', '2252c7403', 'fb9e07326', 'd196ca1fd', 'a8e562e8e', 'eb6bb7ce1', '5beff147e', '52b347cdc', '4600aadcf', '6fa0b9dab', '43d70cc4d', '408021ef8', 'e29d22b59']
print(df_train_org.shape)
df_train_org = df_train_org.drop(drop_cols, axis=1)
print(df_train_org.shape)

from scipy.stats import spearmanr
import warnings
warnings.filterwarnings("ignore")

# 查看特征与目标之间的斯皮尔曼相关系数
labels = []
values = []
for col in df_train_org.columns:
    if col not in ["ID", "target"]:
        labels.append(col)
        values.append(spearmanr(df_train_org[col].values, df_train_org["target"].values)[0])
corr_df = pd.DataFrame({'col_labels': labels, 'corr_values': values})
corr_df = corr_df.sort_values(by='corr_values')
print(corr_df)

corr_df = corr_df[(corr_df['corr_values'] > 0.1) | (corr_df['corr_values'] < -0.1)]
ind = np.arange(corr_df.shape[0])
width = 0.9
fig, ax = plt.subplots(figsize=(12, 30))
rects = ax.barh(ind, np.array(corr_df.corr_values.values), color='b')
ax.set_yticks(ind)
ax.set_yticklabels(corr_df.col_labels.values, rotation='horizontal')
ax.set_xlabel("Correlation coefficient")
ax.set_title("Correlation coefficient of the variables")
plt.show()



cols_to_use = corr_df[(corr_df['corr_values']>0.11) | (corr_df['corr_values']<-0.11)].col_labels.tolist()
print(cols_to_use)
print(len(cols_to_use))

cols_to_drop = corr_df[(corr_df['corr_values']<0.02) & (corr_df['corr_values']>-0.02)].col_labels.tolist()
print(cols_to_drop)
print(len(cols_to_drop))

temp_df = df_train_org[cols_to_use]
corrmat = temp_df.corr(method='spearman')
f, ax = plt.subplots(figsize=(20, 20))

# Draw the heatmap using seaborn
sns.heatmap(corrmat, vmax=1., square=True, cmap="YlGnBu", annot=True)
plt.title("Important variables correlation map", fontsize=15)
plt.show()

### Get the X and y variables for building model ###
train_X = df_train_org.drop(df_train_org.col_name.tolist() + ["ID", "target"], axis=1)
test_X = df_train_org.drop(df_train_org.col_name.tolist() + ["ID"], axis=1)
train_y = np.log1p(df_train_org["target"].values)

print(' - finish - ')