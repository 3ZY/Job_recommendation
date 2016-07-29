#!usr/bin/env python
# -*- coding:utf-8 -*-
# 图表可视化
from __future__ import division
from filTer import *
from getData import *
import matplotlib.pyplot as plt

#判断职位匹配性
def job_match(JWINFO,JOB_OFFER):
    if jobIfEffect(JWINFO,JOB_OFFER)==1:#性别、年龄、城市、职位类型及种类、工资、工作经验、学历
        return 1
    elif city_tpye_IfEffect(JWINFO,JOB_OFFER)==1:#性别、城市、职位类型
        return 2
    elif sex_city_IfEffect(JWINFO,JOB_OFFER)==1:#符合性别及城市
        return 3
    else:#符合性别
        return 4

#绘制图表
def show_plot(fileName,R_Num=8):
    inPath="result/"
    nowtime,lastmonth=getTimes()
    nowtime='2016-7-28'
    lastmonth='2016-6-1'
    JWINFOS,JOB_OFFERS=getJWJOBINFO(nowtime,lastmonth)
    total_rec=0#总推荐数
    total_1=0 #job_match =1
    total_2=0 #job_match =2
    total_3=0 #job_match =3
    total_4=0 #job_match =4
    total_Jw=len(JWINFOS)
    Jw_match={}
    inFile=open(inPath+fileName,'r')
    inFile.readline()
    for line in inFile.readlines():
        values=line[:-1].split(',')
        total_rec+=R_Num
        match_1=len( [x for x in values[1:] if job_match(JWINFOS[int(values[0])],JOB_OFFERS[int(x)])==1 ])
        match_2=len( [x for x in values[1:] if job_match(JWINFOS[int(values[0])],JOB_OFFERS[int(x)])==2 ])
        match_3=len( [x for x in values[1:] if job_match(JWINFOS[int(values[0])],JOB_OFFERS[int(x)])==3 ])
        match_4=len( [x for x in values[1:] if job_match(JWINFOS[int(values[0])],JOB_OFFERS[int(x)])==4 ])
        total_1+=match_1
        total_2+=match_2
        total_3+=match_3
        total_4+=match_4
        Jw_match[values[0]]=[match_1,match_2,match_3,match_4]
    print total_1/total_rec,total_2/total_rec,total_3/total_rec,total_4/total_rec
    labels=u'完全匹配',u'性别城市职位类型匹配',u'性别城市匹配',u'性别匹配'
    sizes=[total_1/total_rec,total_2/total_rec,total_3/total_rec,total_4/total_rec]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.2f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.text(-1.4,1,u'match')
    plt.show()

show_plot('finallyRecommend.csv')
