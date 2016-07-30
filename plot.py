#!usr/bin/env python
# -*- coding:utf-8 -*-
# 图表可视化
from __future__ import division
from filTer import *
from getData import *
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

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
    #数据读取
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

    # ----------- 职位分布 ----------------
    labels=u'完全匹配',u'性别城市职位类型匹配',u'性别城市匹配',u'性别匹配'
    sizes=[total_1/total_rec,total_2/total_rec,total_3/total_rec,total_4/total_rec]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.2f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.text(-1.4,1,u'职位分布')

    # ------------ 匹配性质中，各职位数下的用户比例 ------------------
    fig = plt.figure(figsize=(18,8))
    ax = fig.gca()
    X=[]
    Y=[]
    for i in range(R_Num+1):
        tmp=[]
        tmp.append(sum([1 for key,value in Jw_match.items() if value[0]==i])/total_Jw)
        tmp.append(sum([1 for key,value in Jw_match.items() if value[1]==i])/total_Jw)
        tmp.append(sum([1 for key,value in Jw_match.items() if value[2]==i])/total_Jw)
        tmp.append(sum([1 for key,value in Jw_match.items() if value[3]==i])/total_Jw)
        Y.append(tmp)
    X=np.arange(1,len(labels)+1)
    Y=np.array(Y)*100
    width=0.1
    rects=[]
    rect_colors= [np.random.rand(3) for _ in range(R_Num+1)] # 创建随机颜色
    for i in range(R_Num+1):
        rects.append(ax.bar(X+i*width,Y[i],width=width,color=rect_colors[i],edgecolor='white') )
        for x,y in zip(X,Y[i]):
            ax.text(x-0.05+(width)*(i+1),y+0.05,'%.1f' % y, ha='center', va='bottom')
    ax.set_ylabel(u'用户比例')
    ax.set_xlabel(u'匹配性质')
    ax.legend( [rect[0] for rect in rects], [u'职位数:'+str(i) for i in range(R_Num+1)] )
    ax.set_ylim(0,+110)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f%%'))
    ax.set_xticks( X+width*( (R_Num+1)/2 ) )
    ax.set_xticklabels(labels)

    # ------------ 用户分布 ------------------
    jw_type=[] #用户职位分布类型
    for value,match in Jw_match.items():
        if match not in jw_type:
            jw_type.append(match)
    for i in range(len(labels)):
        jw_type=sorted(jw_type,key=lambda x:x[len(labels)-i-1],reverse=True)

    percent=[]#用户比例
    for match in jw_type:
        percent.append(sum([1 for key,value in Jw_match.items() if value==match])/total_Jw*100)

    width=0.8
    Num=20 #每个窗口显示Num个
    count=int( (len(jw_type)+Num-1)/Num ) #窗口个数
    for v in range(count):
        fig = plt.figure(figsize=(18,8))
        ax = fig.gca()
        tmp=np.array(jw_type[Num*v:Num*(v+1)]).T
        x_num=len(tmp[0])
        X=np.arange(x_num)+0.1
        bottom=np.zeros(x_num)
        rects=[]
        for i in range(len(labels)):
            rects.append(ax.bar(X,tmp[i],width,color=colors[i],edgecolor='white',bottom=bottom) )
            bottom+=tmp[i]

        for i in range(x_num):
            ax.text(X[i]+width/2,R_Num+0.05,'%.2f' % percent[i+Num*v], ha='center', va='bottom')

        ax.set_title(u'用户分布')
        ax.set_ylabel(u'职位数')
        ax.set_xlabel(u'用户')
        ax.legend( [rect[0] for rect in rects],labels)
        ax.set_yticks([i for i in range(R_Num+2)])
        ax.set_ylim(0,R_Num+2)
        ax.set_xlim(0,Num+5)
        ax.set_xticks( X+width/2 )
        ax.set_xticklabels(X.astype(int)+Num*v)

    # ---- to html -----------
    i=0
    for match in jw_type:
        jws=[ key for key,value in Jw_match.items() if value==match]
        outFile=open('show/jw%s.html' % i,'w')
        outFile.write("<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />\n")
        outFile.write("完全匹配: %s  性别城市职位类型匹配: %s  性别城市匹配: %s  性别匹配 :%s</br>\n" \
                        % tuple(match) )
        for jw in jws:
            outstr="<a href='%s.html' target='_blank'>%s</a></br>\n" % (jw,jw)
            outFile.write(outstr)
        i+=1

    # -------- show -----------------
    plt.show()

show_plot('finallyRecommend.csv')
