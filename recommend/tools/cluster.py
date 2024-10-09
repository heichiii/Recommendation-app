import os

# import
import pandas as pd
import random
from sklearn.decomposition import PCA
import  numpy as np
from sklearn.cluster import AgglomerativeClustering
import warnings
import sys
if not sys.warnoptions:
    warnings.simplefilter("ignore")
np.random.seed(42)

# load file
module_dir=os.path.dirname(__file__)
file_path=os.path.join(module_dir,'shopping_behavior_updated.csv')
data = pd.read_csv(file_path)
existing_df = pd.read_csv(file_path)

# Get list of categorical variables
objs = (data.dtypes == 'object')
object_cols = list(objs[objs].index)


# Drop some columns
to_drop = ['Promo Code Used', 'Customer ID', 'Location']
data.drop(to_drop, axis=1, inplace=True)
object_cols.remove('Promo Code Used')
object_cols.remove('Location')

# with level,ordinal encoding
ord_map1 = {'No':0, 'Yes':1}
ord_map2 = {'Store Pickup':0, 'Free Shipping':0, 'Standard':1,'2-Day Shipping':2,'Express':3,'Next Day Air':4}
ord_map3 = {'No':1, 'Yes':0}
ord_map4 = {'Debit Card':0,'Credit Card':0, 'PayPal':1, 'Bank Transfer':2, 'Cash':2,'Venmo':2}
ord_map5 = {'Annually':1, 'Quarterly':2,'Every 3 Months':3,'Monthly':4,'Fortnightly':5,'Bi-Weekly':5,'Weekly':6}
ord_map6 = {'S':1,'M':2,'L':3,'XL':4}

data['Subscription Status'] = data['Subscription Status'].map(ord_map1)
data['Shipping Type'] = data['Shipping Type'].map(ord_map2)
data['Discount Applied'] = data['Discount Applied'].map(ord_map3)
data['Payment Method'] = data['Payment Method'].map(ord_map4)
data['Frequency of Purchases'] = data['Frequency of Purchases'].map(ord_map5)
data['Size'] = data['Size'].map(ord_map6)
data.head()

# without level, one-hot encoding

object_cols.remove('Subscription Status')
object_cols.remove('Shipping Type')
object_cols.remove('Discount Applied')
object_cols.remove('Payment Method')
object_cols.remove('Frequency of Purchases')
object_cols.remove('Size')

for i in object_cols:
    data = pd.concat([data,pd.get_dummies(data[i],prefix=i,dtype=int)],axis=1)
    data.drop(i,axis=1,inplace=True)



#Initiating PCA to reduce dimentions aka features to 3
pca = PCA(n_components=3)
pca.fit(data)
PCA_ds = pd.DataFrame(pca.transform(data), columns=(["col1","col2", "col3"]))
#PCA_ds.head()
PCA_ds.describe().T

#Initiating the Agglomerative Clustering model
AC = AgglomerativeClustering(n_clusters=4)
# fit model and predict clusters
yhat_AC = AC.fit_predict(PCA_ds)

PCA_ds_copy = PCA_ds.copy()


PCA_ds["Clusters"] = yhat_AC
#Adding the Clusters feature to the orignal dataframe.
data["Clusters"]= yhat_AC


# 接下来给每个人推荐他所属类别中最畅销的3个商品
data['ID'] = data.index + 1
data.to_csv(os.path.join(module_dir,'out.csv'), index=False)


existing_df['Clusters'] = data['Clusters'].values
existing_df.to_csv(os.path.join(module_dir,'final.csv'), index=False)


df = pd.read_csv(os.path.join(module_dir,'final.csv'))

# 统计每个簇（Cluster）中最受欢迎的商品类别
top_categories = (
    df.groupby(['Clusters', 'Item Purchased'])
    .size()  # 计算每个类别的数量
    .reset_index(name='Count')  # 重置索引
)

# 获取每个簇中最受欢迎的三个商品类别
top_3_categories = (
    top_categories
    .sort_values(['Clusters', 'Count'], ascending=[True, False])  # 按簇和数量排序
    .groupby('Clusters')
    .head(3)  # 取每个簇的前三个
)

def predict(data):
# Age,Genderf,genferm,size,pp,pm,fp
# single record prediction
    test = [data[0],random.randint(30,150),data[3],random.randint(1,5),random.randint(0,1),random.randint(0,4),random.randint(0,1),data[4],data[5],data[6],data[1],data[2],0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    test_transformed=pca.transform([test])


    test_transformed = np.array(test_transformed).reshape(1,-1)
    distances = np.linalg.norm(PCA_ds_copy - test_transformed, axis=1)
    nearest_index = np.argmin(distances)
    predicted_label = PCA_ds['Clusters'][nearest_index]
    if predicted_label == 0:
        return ['T恤', '裤子', '背包']
    elif predicted_label == 1:
        return ['短裤', '夹克', '首饰']
    elif predicted_label == 2:
        return ['裙子','墨镜','围巾']
    elif predicted_label == 3:
        return ['外套','手提包','夹克']

#predict ([60, 1,0, 2, 15,3,3])
