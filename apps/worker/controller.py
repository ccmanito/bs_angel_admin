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
        timeStamp = msg
    timeArray = time.localtime(timeStamp)
    res = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return res