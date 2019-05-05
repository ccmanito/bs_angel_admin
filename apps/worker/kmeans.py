#coding:utf-8
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
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
def run_kemans(min_cluster_center,max_cluster_center,allocation_data,keyword):
    '''
    接口调用函数，kemans聚类分析
    '''

    #  dict数据过滤及处理
    allocation_data = json.loads(allocation_data)
    manlist = allocation_data["target_man"]
    womanlist = allocation_data["target_woman"]
    
    target_man_list = []
    target_woman_list = []
    
    for i in manlist:
        target_man_list.append(formal_data(i))
    
    for j in womanlist:
        target_woman_list.append(formal_data(j))
    
    # 将dict数据转为csv格式
    df = pd.DataFrame(target_man_list)
    print(df)