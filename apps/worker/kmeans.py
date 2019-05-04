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
