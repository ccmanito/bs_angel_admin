#! /usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import datetime
from datetime import date
from .models import Work_Order
from apscheduler.schedulers.background import BackgroundScheduler
from .controller import get_allocation_data
def job_func(args):
    '''
    定时任务工作函数，具体操作实现
    '''
    print('...... 开始执行keyword= ' + args + ' 数据采集任务')
    print('...... 初始化待分配数据')
    allocation_data = get_allocation_data(args)
    if allocation_data:
        print('...... 待分配数据初始化完成')
        try:
            Work_Order.objects.filter(keyword=args).update(allocation_data=allocation_data)
        except Exception:
            print('...... 待分配数据存入失败')

def regularly(timestr, args):
    '''
    定时执行任务，每个job只执行一次
    通过 scheduler.get_jobs() 方法能够获取当前调度器中的所有 job 的列表
    '''
    print('......已新增定时调度任务')
    scheduler = BackgroundScheduler()
    scheduler.add_job(job_func, 'date', run_date=timestr, args=args)
    scheduler.start()