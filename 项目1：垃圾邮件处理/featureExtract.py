# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import re #正则
import jieba
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys


mpl.rcParams['font.sans-serif']=[u'simHei']
mpl.rcParams['axes.unicode_minus']=False

df = pd.read_csv('./data/result_process',sep = ',',header = None,names = ['From','To','date','content','label'])
#print(df.head())

##############特征工程1：提取邮件收发的服务器地址
def extract_email_server_address(str1):
    #定义正则匹配项
    reg = re.compile('@[A-Za-z0-9]*\.[A-Za-z0-9\.]*')
    it = reg.findall(str(str1)) #findall返回一个列表
    result = ''
    if len(it) >0:
        result = it[0]
    if not result:
        result = 'unknown'
    return result
      
#将‘From’，‘To’的值进行清洗
df['from_address'] = pd.Series(map(lambda str:extract_email_server_address(str),df['From']))       
df['to_address'] = pd.Series(map(lambda str:extract_email_server_address(str),df['To']))        

#统计邮件收发服务器的数量
print('================from===========')
print(df.from_address.value_counts().head())
#unique()返回一个列表，作用：将不重复的元素返回
print("总邮件发送服务器类别数量为:",str(df.from_address.unique().shape))

print('================to===========')
print(df.to_address.value_counts().head())
#unique()返回一个列表，作用：将不重复的元素返回
print("总邮件接收服务器类别数量为:",str(df.to_address.unique().shape))


#to_frame()作用：将Series转换为DataFrame
from_address_df = pd.DataFrame(df.from_address.value_counts())#.to_frame()
len_less_10_from_adderss_count = from_address_df[from_address_df.from_address<=10].shape
print("发送邮件数量小于10封的服务器数量为:",str(len_less_10_from_adderss_count))


#######特征工程2:时间处理
def extract_email_date(string):

    if not isinstance(string,str):
        string = str(string)
    str_len = len(string)
    
    
    week = ''
    hour = ''
    #0表示上午8-12，1表示13-18，2表示19-23，3表示0-7
    time_quantum = ''
    if str_len < 10:
        week = 'unknown'
        hour = 'unknowm'
        time_quantum = 'unknown'

    elif str_len == 16:
        # 2005-9-2 上午10:55
        rex = re.compile('\d{2}:\d{2}')
        it = rex.findall(string)
        if len(it) == 1:
            hour = it[0]
        else:
            hour = 'unknown'
        week = 'Fri'
        time_quantum = '0'
    elif str_len == 19:
        # Sep 23 2005 1:04 AM
        week = 'Sep'
        hour = '01'
        time_quantum = '3'
    elif str_len == 21:
        # August 24 2005 5:00pm
        week = "Wed"
        hour = "17"
        time_quantum = "1"
    else:
        rex = re.compile('([A-Za-z]+\d?[A-Za-z]*) .*?(\d{2}):\d{2}:\d{2}.*')
        it = rex.findall(string)
        
        if len(it) == 1 and len(it[0]) == 2:
            week = it[0][0][-3]
            hour = it[0][1]
            int_hour = int(hour)
            if int_hour < 8:
                time_quantum = "3"
            elif int_hour < 13:
                time_quantum = "0"
            elif int_hour < 19:
                time_quantum = "1"
            else:
                time_quantum = '2'
                
        else:
            week = "unknown"
            hour = "unknown"
            time_quantum = "unknown"
    week = week.lower()
    hour = hour.lower()
    time_quantum = time_quantum.lower()
    return (week,hour,time_quantum)
    
date_result = list(map(extract_email_date,df['date']))
df["date_week"] = pd.Series(map(lambda t:t[0],date_result))
df['date_hour'] = pd.Series(map(lambda t:t[1],date_result))
df['time_quantum'] = pd.Series(map(lambda t:t[2],date_result))

print("=======星期属性字段描述======")
#value_counts()作用：统计么一个元素出现的次数
print(df.date_week.value_counts().head())
#数据透视表
print(df.pivot_table(index = ['date_week','label'],aggfunc={'label':'count'}))

print("=======小时属性字段描述======")
#value_counts()作用：统计么一个元素出现的次数
print(df.date_hour.value_counts().head())
#数据透视表
print(df.pivot_table(index = ['date_hour','label'],aggfunc={'label':'count'}))

print("=======时间段属性字段描述======")
#value_counts()作用：统计么一个元素出现的次数
print(df.time_quantum.value_counts().head())
#数据透视表pivot_table() 与  groupby()
print(df.pivot_table(index = ['time_quantum','label'],aggfunc={'label':'count'}))

#添加是否有‘date_week’，标记为0和1
df['has_date'] = df.apply(lambda c: 0 if c['date_week'] == 'unknown' else 1, axis = 1)
         
#特征工程3：content分词
'''
jieba 第三方包是处理中文的一个重要分词工具
1.分词方法cut()有三种三种方式一般选择 精准模式（默认）
2.自定义分词字典，通过jieba.load_userdict('字典名.txt')加载
3.导入jieba 的posseg包可以查看分词后的词性
'''
df['content'] = df['content'].astype('str')
df['jieba_cut_content'] = list(map(lambda st: '/'.join(jieba.cut(st)),df['content']))


#特征工程3：邮件长度
def process_content_length(lg):
    if lg < 10:
        return 0
    elif lg <= 100:
        return 1
    elif lg <= 500:
        return 2
    elif lg <= 1000:
        return 3
    elif lg <= 1500:
        return 4
    elif lg <= 2000:
        return 5
    elif lg <= 2500:
        return 6
    elif lg <= 3000:
        return 7
    elif lg <= 4000:
        return 8
    elif lg <= 5000:
        return 9
    elif lg <= 10000:
        return 10
    elif lg <= 20000:
        return 11
    elif lg <= 30000:
        return 12
    elif lg <= 50000:
        return 13
    else:
        return 14
#判断内容长度
df['content_length'] = list(map(lambda st:len(st),df['content']))
df['content_lg_type'] = list(map(lambda st :process_content_length(st),df['content_length']))

df2 = df.groupby(["content_lg_type","label"])["label"].agg(['count']).reset_index()
df3 = df2[df2.label == 1][['content_lg_type','count']].rename(columns = {'count':'c1'})
df4 = df2[df2.label == 0][['content_lg_type','count']].rename(columns = {'count':'c2'})

df5 = pd.merge(df3,df4)

df5['c1_rage'] = df5.apply(lambda r:r["c1"]/(r["c1"]+r["c2"]),axis=1) 
df5["c2_rage"] = df5.apply(lambda r:r["c2"]/(r["c1"]+r["c2"]),axis=1)

plt.plot(df5['content_lg_type'],df5['c1_rage'],label = u'正常邮件比例')
plt.plot(df5['content_lg_type'],df5['c2_rage'],label = u'垃圾邮件比例')


plt.xlabel(u"邮件长度标记")
plt.ylabel(u"邮件比例")
plt.grid(True)
plt.legend(loc='best')
plt.show()

#特征工程4：添加信号量
def precess_content_sema(x):
    if x > 10000:
        return 0.5/np.exp(np.log10(500)) + np.log(abs(x-500) + 1) - np.log(abs(x-10000)) +1
    else:
        return 0.5/np.exp(np.log10(x)-np.log10(500))+np.log(abs(x-500)+1)+1

a = np.arange(1,20000)
plt.plot(a,list(map(lambda t:precess_content_sema(t),a)),label=u"信息量")
plt.grid(True)
plt.legend(loc=0)
plt.savefig("信息量.png")

df['content_sema'] = list(map(lambda st :precess_content_sema(st),df['content_length']))
print(df['content_sema'])
print(df.head())
print(df.dtypes)

#得到最终模型训练需要的数据
#drop()方法可以得到一个新的dataframe，不改变原始数据，其中inplace参数 可以 决定是否改变原始数组，默认 否
# 收发地址，时间，内容长短 都与是否为垃圾邮件贡献度不高，将这些列删除
#drop() 列表参数中为要删除的内容
df.drop(["From","To","date","content","to_address","from_address",
         "date_week","date_hour","time_quantum","content_length",
         "content_lg_type"],axis = 1,inplace = True)
#print(df.dtypes)
#print(df.head())
df.to_csv('./results',encoding = 'utf-8',index = False)






























       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
