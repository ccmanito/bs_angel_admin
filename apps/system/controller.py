#coding:utf-8
import time,json

def format_time(msg):
    '''
    时间戳转换
    '''
    if msg == None:
        return '--'
    if len(str(msg)) == 13:
        timeStamp  = int(msg) / 1000
    else:
        timeStamp = int(msg)
    timeArray = time.localtime(timeStamp)
    res = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return res