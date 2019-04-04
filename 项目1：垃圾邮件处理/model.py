# -*- coding: utf-8 -*-
import time 
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import f1_score,precision_score,recall_score


mpl.rcParams['font.sans-serif']=[u'simHei']
mpl.rcParams['axes.unicode_minus']=False

df = pd.read_csv('./results',sep = ',')

df.dropna(axis = 0,how = 'any',inplace = True)
x = df[['has_date','jieba_cut_content','content_sema']]
y = df['label']
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 6)
print('训练集，测试集大小%d,%d' % (x_train.shape[0],x_test.shape[0]))

#对文本数据进行数值化处理
#CountVectorizer会将文本中的词语转换为词频矩阵，通过fit_transform计算各个词出现的次数、
#TfidfTransformer用于统计vectorizer中每个词的tf-idf值

#TfidfVectorizer 就是相当于完成了上面两个加起来的功能,将文本转换为tf-idf特征矩阵，从而进行文本相似度计算
tfid = TfidfVectorizer(norm = 'l2',use_idf=True)
svd = TruncatedSVD(n_components=20)
jieba_cut_content = list(x_train['jieba_cut_content'].astype('str'))
df1 = tfid.fit_transform(jieba_cut_content)#建模转换
print(df1)
print(df1.shape)
jieba_cut_content_test = list(x_test['jieba_cut_content'].astype('str'))
df2 = tfid.transform(jieba_cut_content_test)
df3 = svd.fit_transform(df1)
print(df3)
print(df3.shape)
df4 = svd.fit_transform(df2)
#训练集最终数据
data = pd.DataFrame(df3)
data['has_date'] = list(x_train['has_date'])
data['content_sema'] = list(x_train['content_sema'])
#测试集
data_test = pd.DataFrame(df4)
data_test['has_date'] = list(x_test['has_date'])
data_test['content_sema'] = list(x_test['content_sema'])


#进行训练

t1 = time.time()
bn = BernoulliNB(alpha=1.0,binarize=0.0005)
bn_model = bn.fit(data,y_train)
t2 = time.time()-t1
print('构建时间%.3fms'% (t2*1000))

y_pre = bn_model.predict(data_test)

print('准确率：%.5f' % precision_score(y_test,y_pre))
print('召回率：%.5f' % recall_score(y_test,y_pre))
print('F1值：%.5f' % f1_score(y_test,y_pre))


#随机森林
from sklearn.ensemble import RandomForestClassifier
t3 = time.time()
forest = RandomForestClassifier(n_estimators=100,criterion='gini',max_depth=3,random_state=6)
forest_model = forest.fit(data,y_train)
t4 = time.time()-t3
print('构建时间%.3fms'% (t4*1000))

y_pre1 = forest_model.predict(data_test)

print('准确率：%.5f' % precision_score(y_test,y_pre1))
print('召回率：%.5f' % recall_score(y_test,y_pre1))
print('F1值：%.5f' % f1_score(y_test,y_pre1))












