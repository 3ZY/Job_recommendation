#!usr/bin/env python
# -*- coding:utf-8 -*-
#结果输出
from __future__ import division
from DB import *
from datetime import date
import operator

#输出推荐结果到文件
def outToFile(fileName,recommend):
	path='result/'
	outFile=open(path+fileName,'w')
	outFile.write('Jw_SN,Job_SN...\n')
	for u,u_recommend in recommend.items():
		if u_recommend!={}:
			outFile.write(str(u))
			for i,p in sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True):
				outFile.write(','+str(i))
			outFile.write("\n")
#输出运行日志
def log_out(nowtime,errStr,outStr):
	sql="insert into [dbo].[Rec_log] \
      	([log_time],[JW_QUERY_LOG] ,[JWAPPLYJOB] ,[JOB_FAV] ,[RESUME] \
		,[JWINFO] ,[JOB_OFFER] ,[getData] ,[evaluate] \
		,[userCF_IIF] ,[most_popular] \
		,[CB_fill] ,[outToDB] ,[total] ,[err]) \
	  	values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
	  	% (nowtime,outStr['JW_QUERY_LOG'], outStr['JWAPPLYJOB'], outStr['JOB_FAV'], \
			outStr['RESUME'], outStr['JWINFO'], outStr['JOB_OFFER'], outStr['getData'], \
			outStr['evaluate'], outStr['userCF_IIF'], \
			outStr['most_popular'], outStr['CB_fill'], outStr['outToDB'], \
			outStr['total'], errStr.replace("'",u"''"))
	DBInsert(sql)

#输出推荐结果到数据库
def outToDB(recommend):
	sql="truncate table [dbo].[Job_Rec]"
	DBInsert(sql)
	sql="insert into [dbo].[Job_Rec] ([Jw_SN],[Job_Rec],[Push]) values "
	flag=False
	num=0
	for u,u_recommend in recommend.items():
		if u_recommend!={}:
			num+=1
			ifPush=0
			if sum([p for i,p in sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True)[:6] ] )>=0.012:
				ifPush=1#推送
			content="('%s','%s','%s')," % \
			(str(u),(",").join([str(i) for i,p in sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True)]),str(ifPush))
			sql+=content
			flag=True
			if num==1000:
				num=0
				DBInsert(sql[:-1])
				sql="insert into [dbo].[Job_Rec] ([Jw_SN],[Job_Rec],[Push]) values "
				flag=False
	if flag:
		DBInsert(sql[:-1])

#输出F1到数据库
def outScore(jw_score):
	sql="truncate table [dbo].[Rec_F1]"
	DBInsert(sql)
	sql="insert into [dbo].[Rec_F1] ([Jw_SN],[Precision],[Recall],[F1]) values "
	flag=False
	num=0
	for jw,score in jw_score.items():
		num+=1
		content="('%s','%s','%s','%s')," % (str(jw),str(score[0]),str(score[1]),str(score[2]))
		sql+=content
		flag=True
		if num==1000:
			num=0
			DBInsert(sql[:-1])
			sql="insert into [dbo].[Rec_F1] ([Jw_SN],[Precision],[Recall],[F1]) values "
			flag=False
	if flag:
		DBInsert(sql[:-1])

#输出F1到文件
def outScoreToFile(jw_score):
	nowday=str(date.today())
	outFile=open('evaluate/%s.csv' % nowday,'w')
	outFile.write('Jw_SN,Precision,Recall,F1\n')
	for jw,score in jw_score.items():
		outFile.write("%s,%s,%s,%s\n" % (str(jw),str(score[0]),str(score[1]),str(score[2])) )
