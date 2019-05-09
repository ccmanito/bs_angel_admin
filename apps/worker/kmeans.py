#coding:utf-8
from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt
# import matplotlib matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.cluster import KMeans, MiniBatchKMeans #导入K均值聚类算法
from sklearn.decomposition import PCA #进行降维处理
import os
import time,json
import pandas as pd
import numpy as np

INTEREST_MAP = {
        "非常感兴趣": 0.08,
        "感兴趣": 0.07,
        "一般": 0.06,
        "不感兴趣": 0.05
    }
INTENT_MAP = {
    "考研": 0.5,
    "就业": 0.4,
    "出国": 0.3,
    "无要求": 0.2
}
TIME_MAP = {
    "早睡早起": 1,
    "晚睡早起": 2,
    "晚睡晚起": 3,
    "早睡晚起": 4
}
def formal_data(msg):
    '''
    数据处理并充填, 
    
    数据释义：
        esports：对电子竞技、桌游等。 指标：（不感兴趣，感兴趣，一般， 非常感兴趣）
        learnintent：学习意向   指标： 考研、就业、出国、无要求
        outdoorsports：对户外运动、体育运动、健身、徒步等活动。指标：（不感兴趣，感兴趣，一般， 非常感兴趣）
        talent：对艺术（唱歌、跳舞、演奏、绘画、园艺、摄影、创作）  指标（不感兴趣，感兴趣，一般， 非常感兴趣）
        time：作息时间  指标： 早睡早起、晚睡早起、晚睡晚起、早睡晚起
     
    '''
    
    target_dict = {}
    for k,v in msg.items():
        if v == '':
            target_dict[k] = 0
        elif k in ['esports','outdoorsports','talent']:
            target_dict[k] = INTEREST_MAP[v]
        elif k == 'time':
            target_dict[k] = TIME_MAP[v]
        elif k == 'learnintent':
            target_dict[k] = INTENT_MAP[v]
        else:
            pass
    # print(target_dict)
    return target_dict

#数据归一化(线性归一化)
def nomalization(df,columns):
    for listName in columns:
        if df[listName].max() != df[listName].min():
            df[listName] = (df[listName]-df[listName].min())/(df[listName].max()-df[listName].min())

#对于聚类需要计算距离，且字段是离散化的，需要进行one-hot编码
def onehot(df,columns):
    print('开始进行onehot编码')
    for l in columns:
        df_dummies2 = pd.get_dummies(df[l], prefix=l) #选定要进行onehot编码的列，增名为scomb_____1
        df = df.drop(l, axis=1) #删除原有的列
        df = pd.concat([df,df_dummies2],axis=1) #重新拼接
    print('onehot编码结束')

#进行降维处理
def draw(Data,centers,index=None):
    """
            降维展示分类效果，
            不代表实际数据的分布
    """
    fig,axes = plt.subplots(1,1)#fig为幕布对像 axes为子图对象
    pca = PCA(n_components=2)#设置维度
    new_data = pca.fit_transform(Data) #进行绘图
    # print (new_data)
    axes.scatter(new_data[:,0], new_data[:,1],c='b',marker='o',alpha=0.5)#在子图0上绘制二维分布图像
    # print('-------------------------')
    # print(centers)
    # for center_index,center in enumerate(centers):#绘制分类中心点
    axes.scatter(centers[:,0], centers[:,1],c='r',marker='*',alpha=0.5)
    plt.show()

#进行kmeans聚类
def kmeans(df,k,drawplt = True, max_iter=300,return_n_iter=True):
    data_set = df.as_matrix()
    kmeans = KMeans(n_clusters=k).fit(data_set) # fit（X [，y，sample_weight]）	计算k均值聚类。
    centers = kmeans.cluster_centers_#获取中心点
    pca = PCA(n_components=2)  # 设置维度
    centers_d = pca.fit_transform(centers)
    labels = kmeans.labels_ #获取聚类标签
    inertia = kmeans.inertia_ #获取聚类准则的总和
    num = kmeans.n_iter_
    # if drawplt:
    #     draw(data_set,centers_d)
    return inertia,labels,num

def SSE(df, max_cluster_center, key, keyword):
    '''
    选取K值：手肘法
    '''
    path = os.getcwd()
    picture_path = {}
    if key == 'woman':
        WOSSE = []  # 存放每次结果的误差平方和
        for k1 in range(2, max_cluster_center):
            res = kmeans(df,k1)
            WOSSE.append(res[0])

        X = range(2, max_cluster_center)
        plt.xlabel('k')
        plt.ylabel('SSE')
        plt.plot(X, WOSSE, 'o-')
        plt.title('female k')
        plt.savefig( 'E:\workdir\\bs\\bs_angel_fe\static\images\woman' + '\\'+ keyword + '.png')
        picture_path['woman_picture_path'] = 'E:\workdir\\bs\\bs_angel_fe\static\images\woman' + '\\'+ keyword + '.png'
        # plt.close()
        plt.clf()
    else:
        MANSSE = []  # 存放每次结果的误差平方和
        for k2 in range(2, max_cluster_center):
            res = kmeans(df,k2)
            MANSSE.append(res[0])
        Y = range(2, max_cluster_center)
        plt.xlabel('k')
        plt.ylabel('SSE')
        plt.plot(Y, MANSSE, 'o-')
        plt.title('male k')
        plt.savefig('E:\workdir\\bs\\bs_angel_fe\static\images\man' + '\\'+ keyword + '.png')
        picture_path['man_picture_path'] = 'E:\workdir\\bs\\bs_angel_fe\static\images\woman' + '\\'+ keyword + '.png'
        # plt.close()
        plt.clf()
    return picture_path

def get_data_list(allocation_data,keyword):
    '''
    最终可用数据函数
    '''
    #  dict数据过滤及处理
    allocation_data = json.loads(allocation_data)
    manlist = allocation_data["target_man"]
    womanlist = allocation_data["target_woman"]
    
    man_max_cluster_center = len(manlist)
    woman_max_cluster_center = len(womanlist)

    target_man_list = []
    target_woman_list = []
    
    #格式化数据
    for i in manlist:
        target_man_list.append(formal_data(i))
    
    for j in womanlist:
        target_woman_list.append(formal_data(j))
    
    # 将dict数据转为csv格式
    man_df = pd.DataFrame(target_man_list)
    woman_df = pd.DataFrame(target_woman_list)
    
    # titlelist =  ['esports','learnintent','outdoorsports','talent','time']
    # nomalization(df, titlelist)
    # onehot(df, titlelist)
    # kmeans(df,28)
    
    return man_df,woman_df,man_max_cluster_center,woman_max_cluster_center

def get_elbow_picture(allocation_data,keyword):
    '''
    获取拐点图地址
    '''
    res = get_data_list(allocation_data, keyword)
    
    sse_woman_path = SSE(res[1], res[3], 'woman', keyword)
    sse_man_path = SSE(res[0], res[2], 'man', keyword)

    return 0

def run_kemans(allocation_data,keyword, woman_k, man_k):
    '''
    通过最佳得K执行分配
    '''
    
    # 拿到处理好的待分配数据 
    res = get_data_list(allocation_data, keyword)
    man_df = res[0]
    woman_df = res[1]
    
    # kmeans() retuen  inertia,labels,num
    man_res = kmeans(man_df,man_k)
    woman_res = kmeans(woman_df,woman_k)
    
    # 拿到原始数据
    allocation_data = json.loads(allocation_data)
    manlist = allocation_data["target_man"]
    womanlist = allocation_data["target_woman"]
    
    
    # enumerate(man_res[1]) return  [(0, 0), (1, 0), (2, 0)]
    
    tag_man_dict = {
        'iterations': man_res[2],
        'inertia': str(man_res[0])[0: 8],
        'tag_man_list': []
    }
    tag_woman_dict = {
        'iterations': woman_res[2],
        'inertia': str(woman_res[0])[0: 8],
        'tag_woman_list': []
    }

    for i in range(man_k): 
        man_list = []
        index_man_list = [index for index,value in enumerate(man_res[1]) if value == i ]
        for k in index_man_list:
            man_value = [value1 for index1,value1 in enumerate(manlist) if index1 == k ]
            man_list.append(man_value[0])
        tag_man_dict['tag_man_list'].append(man_list)
    
    
    for j in range(woman_k): 
        woman_list = []
        index_woman_list = [index2 for index2,value2 in enumerate(woman_res[1]) if value2 == j ]
        for m in index_woman_list:
            woman_value = [value3 for index3,value3 in enumerate(womanlist) if index3 == m ]
            woman_list.append(woman_value[0])
        tag_woman_dict['tag_woman_list'].append(woman_list)
    
    result = []
    result.append(tag_man_dict)
    result.append(tag_woman_dict)
    
    return result