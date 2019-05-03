#coding:utf-8
from sklearn.cluster import KMeans
# import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.cluster import KMeans, MiniBatchKMeans #导入K均值聚类算法
from sklearn.decomposition import PCA #进行降维处理
import time

def format_time(msg):
    '''
    时间戳转换
    '''
    
    if len(str(msg)) == 13:
        timeStamp  = int(msg) / 1000
    else:
        timeStamp = int(msg)
    timeArray = time.localtime(timeStamp)
    res = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return res

def countdown(msg):
    '''
    距离该时间计算函数
    '''
    now = int(time.time())
    endtime = int( int(msg) / 1000)
    countdown = (endtime - now)
    if countdown < 3600  and countdown > 0:
        temp  = str(float( '%.2f' % (countdown / 60)))
        res = temp + '分钟'
    elif countdown > 86400:
        temp  = str(float( '%.2f' % (countdown / 60 / 60 /24)))
        res = temp + '天'
    elif countdown < 0:
        res = '已关闭'
    else:
        temp  = str(float( '%.2f' % (countdown / 60 / 60)))
        res = temp + '小时'
    return res 