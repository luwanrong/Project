# -*- coding: utf-8 -*-

import jieba
from jieba import posseg

#构建词典
jieba.load_userdict('./word.txt')
str = '这半年发生的许多事，但是没啥好消息，不开心！北风网'
#jieba分词的cut()接口，分为三种模式：精准模式，全模式，关闭隐马尔科夫模型
cut1 = jieba.cut(str)#精准模式
print(' '.join(cut1))

#cut2 = jieba.cut(str,cut_all = True)#全模式
#print('/'.join(cut2))

#cut3 = jieba.cut(str,HMM = False)#关闭HMM
#print('/'.join(cut3))
cut4 = posseg.cut(str)
for i in cut4:
    print(i.word,end = '')
    print(i.flag)#返回词性