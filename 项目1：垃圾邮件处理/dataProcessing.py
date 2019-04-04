
# -*- coding: utf-8 -*-
'''  '''
import os 
import time

def 制作标签字典(file_path):
    type_dict = {'spam':'1','ham':'0'}
    #打开文件
    index_file = open(file_path)
    index_dict = {}
    try:
        for line in index_file:
            arr = line.split(' ')
            if len(arr) == 2:
                key ,value = arr
            #将字典的值'../data/000/000'的../data删除 也删除 最后的换行符
            value = value.replace('../data','').replace('\n','')
            index_dict[value] = type_dict[key.lower()]
    finally:
        index_file.close()
    return index_dict
def 读取邮件内容(file_path):
    #以只读的形式打开邮件
    file = open(file_path, 'r',encoding = 'gb2312', errors = 'ignore')
    content_dict = {}
    
    try:
        is_content = False#定义一个开关
        for line in file:#遍历每一行
            line = line.strip()#将所有的空格切掉
            if line.startswith('From:'):
                #将其内容添加到支点
                content_dict['From'] = line[5:] 
            elif line.startswith('To:'):
                content_dict['To'] = line[3:]
            elif line.startswith('Date:'):
                content_dict['Date'] = line[5:]
            elif not line:#如果是空行
                is_content = True
            
            if is_content:
                if 'content' in content_dict:#判断字典中有没有 key：content
                    content_dict['content'] += line
                else:
                    content_dict['content'] = line
    finally:
        file.close()
            
        return content_dict
def 字典转文本(file_path):#将每一份 邮件都转换为一行，各内容用‘，’隔开
    content_dict = 读取邮件内容(file_path)
    
    result_str = content_dict.get('From','unkonwn').replace(',','').strip() + ','                
    result_str += content_dict.get('To','unkonwn').replace(',','').strip() + ','                
    result_str += content_dict.get('Date','unkonwn').replace(',','').strip() + ','                
    result_str += content_dict.get('content','unkonwn').replace(',','').strip()               
    
    return result_str
start = time.time()    
index_dict = 制作标签字典('./full/index')
#将文件夹下的文件或文件夹的名称列表返回  
#就是说在/data路径下的000文件夹到215文件夹的名称返回，以便后边遍历所有的文件

list0 = os.listdir('./data')
#开始遍历每一个文件夹[000-215]
for dir1 in list0:
    #得到处理的路径 ./data/000 
    current_path = './data/' + dir1
    
    print('正在处理的文件夹是：',current_path)
    #000文件夹路径，在该路径下还有300左右各文件
    dir_path = os.listdir(current_path)
    #dir_path 就是000文件夹下所有文件的列表
    #将每一个文件夹中的所有文件的内容都写到一个文件，eg：将./data/000文件家中的000文件-299文件的内容写到./data/process_000中
    write_file_path = './data/process_' + dir1
    #print(write_file_path)
    with open(write_file_path,'w',encoding = 'utf-8') as file:   
        for dir2 in dir_path:
            #得到要处理文件的路径 current_path + '/' +dir2 = ./data/000/000
            dir2_path = current_path + '/' +dir2
            #开始写内容
            index_key = '/' + dir1 + '/' +dir2
            #print(index_dict[index_key])
            
            if index_key in index_dict:
                content_str = 字典转文本(dir2_path)
                # 给数据添加分类
                content_str += ',' + index_dict[index_key] + '\n'
                #写入文件
                file.writelines(content_str)
                
#将每个文件中的内容合并到一个文件
with open('./data/result_process','w',encoding = 'utf-8') as writer:
    for l1 in list0:
        file_path = './data/process_' + l1
        print('开始合并文件：',file_path)
        
        with open(file_path,encoding = 'utf-8') as file:
            for line in file:
                writer.writelines(line)
end = time.time()
print('总共耗时%.3fs'% (end - start))               
            
    
    
    
    

