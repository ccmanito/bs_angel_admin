#! /usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import datetime
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler

def job_func(args):
    '''
    定时任务工作函数，具体操作实现
    '''
    print(args)


def regularly(timestr, args):
    '''
    定时执行任务，每个job只执行一次
    通过 scheduler.get_jobs() 方法能够获取当前调度器中的所有 job 的列表
    '''
    scheduler = BackgroundScheduler()
    # 在 2017-12-13 时刻运行一次 job_func 方法
    # scheduler.add_job(job_func, 'date', run_date=date(2017, 12, 13), args=['text'])
    # 在 2017-12-13 14:00:00 时刻运行一次 job_func 方法
    # scheduler.add_job(job_func, 'date', run_date=datetime(2017, 12, 13, 14, 0, 0), args=['text'])
    # 在 2017-12-13 14:00:01 时刻运行一次 job_func 方法
    scheduler.add_job(job_func, 'date', run_date=timestr, args=args)
    
    scheduler.start()