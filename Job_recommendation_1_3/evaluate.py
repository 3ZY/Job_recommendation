#!usr/bin/env python
# -*- coding:utf-8 -*-
# 评估函数
from __future__ import division
from DB import *
from getData import *
from outData import outScore

#得出各用户的Score
def evaluate(Job_Rec):
    if Job_Rec=={}:
        return 0
    nowday,lastday=getTimes(1)
    # nowday='2016-7-28'
    # lastday='2016-7-27'
    actionData=getTrainData(nowday,lastday)
    if actionData=={}:
        return 0
    Jw_click={}#求职者产生行为的职位
    for jw,jobs in actionData.items():
        Jw_click[jw]=set(jobs.keys())
    del actionData

    jw_score={}#评分
    for jw,rec_push in Job_Rec.items():
        if jw not in Jw_click:
            continue
        rec=set(rec_push[0].split(','))
        click=Jw_click[jw]
        common=rec&click
        rec_num=len(rec)+0.0000000001
        click_num=len(click)+0.0000000001
        common_num=len(common)
        Precision=common_num/rec_num
        Recall=common_num/click_num
        F1=(2*Precision*Recall)/(Precision+Recall+0.0000000001)
        jw_score[jw]=[Precision,Recall,F1]

    if jw_score!={}:
        jw_score['-1']=[ sum([ values[0] for values in jw_score.values() ]) / len(jw_score),\
                            sum([ values[1] for values in jw_score.values() ]) / len(jw_score),\
                            sum([ values[2] for values in jw_score.values() ]) / len(jw_score)]
    outScore(jw_score)
