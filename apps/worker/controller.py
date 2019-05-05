#coding:utf-8
import time,json
from .models import Work_Order
from login.models import UserInfo
from django.db.models import Q

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

def get_allocation_data(msg):
    '''
    获取待分配数据,除去已分配的人员
    '''
    try:
        keyword = msg
        res = Work_Order.objects.filter(keyword=keyword).values()
        form_data = json.loads(res[0]['form_data'])
        
        #初始化form-data数据
        tempDict = {}
        tempDict['school'] = form_data['school']
        if  len(form_data['college']):
            tempDict['college'] = form_data['college']
        if  len(form_data['major']):
            tempDict['major'] = form_data['major']
        if  len(form_data['grade']):
            tempDict['grade'] = form_data['grade']
        if  len(form_data['classname']):
            tempDict['classname'] = form_data['classname']
        
        collegeQlist = []
        majorQlist = []
        gradeQlist = []
        classnameQlist = []
        schoolQ = ''
        
        # 将查询条件转换为Q对象
        for k,v in tempDict.items():
            if k == 'school':
                schoolQ = Q(school = v)
                continue
            elif k == 'college':
                for i in v:
                    tempQ = Q(college=i)
                    collegeQlist.append(tempQ)
            elif k == 'major':
                for i in v:
                    tempQ = Q(major=i)
                    majorQlist.append(tempQ)
            elif k == 'grade':
                for i in v:
                    tempQ = Q(grade=i)
                    gradeQlist.append(tempQ)
            elif k == 'classname':
                for i in v:
                    tempQ = Q(classname=i)
                    classnameQlist.append(tempQ)
        
        #  将Q对象进行聚合
        collegeQ = Q()
        for i in range(len(collegeQlist)):
            collegeQ = collegeQlist[i] | collegeQ
        
        majorQ = Q()
        for i in range(len(majorQlist)):
            majorQ = majorQlist[i] | majorQ

        gradeQ = Q()
        for i in range(len(gradeQlist)):
            gradeQ = gradeQlist[i] | gradeQ 
        
        classnameQ = Q()
        for i in range(len(classnameQlist)):
            classnameQ = classnameQlist[i] | classnameQ
        
        # 分配状态 : 0 待分配、1 分配中、2.已分配
        status = 0
        # 分配人员只能是学生权限级别的人员  token = 1
        token = 1
        
        # 获取符合该分配的人员信息(男，女 分别获取)
        try:
            res_man = UserInfo.objects.filter(schoolQ, collegeQ, majorQ, gradeQ, classnameQ, status=status, roles=token, sex="男").values()
            res_woman = UserInfo.objects.filter(schoolQ, collegeQ, majorQ, gradeQ, classnameQ, status=status, roles=token, sex="女").only('school').values()
        except Exception:
            res_man = []
            res_woman = []
        
        target_res_woman = []
        for i in res_woman:
            interests = json.loads(i['interests'])
            livinghabits = json.loads(i['livinghabits'])
            temp = {
                'u_id': i['u_id'],
                'name': i['name'],
                'esports': interests['esports'],
                'outdoorsports':  interests['outdoorsports'],
                'talent':  interests['talent'],
                'learnintent': livinghabits['learnintent'],
                'time':  livinghabits['time'],
            }
            target_res_woman.append(temp)

        target_res_man = []
        for i in res_man:
            interests = json.loads(i['interests'])
            livinghabits = json.loads(i['livinghabits'])
            temp = {
                'u_id': i['u_id'],
                'name': i['name'],
                'esports': interests['esports'],
                'outdoorsports':  interests['outdoorsports'],
                'talent':  interests['talent'],
                'learnintent': livinghabits['learnintent'],
                'time':  livinghabits['time'],
            }
            target_res_man.append(temp)
        
        data = {
            'target_man': target_res_man,
            'target_woman': target_res_woman
        }
        data = json.dumps(data)
    except Exception:
        data = {}
    return data

def test():
    '''
    '''
    pass