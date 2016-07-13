#!usr/bin/env python
# -*- coding:utf-8 -*-
#获得数据
from DB import *
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


#获得时间段
def getTimes():
	#2月最后一天当28号
	month={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
	localtime=time.localtime()
	nowtime=str(localtime[0])+'-'+str(localtime[1])+'-'+str(localtime[2])
	if localtime[1]-1==0:
		lastmonth=str(localtime[0]-1)+"-12-"+str(localtime[2])
	else :
		if localtime[2]>month[localtime[1]-1]:
			lastmonth=str(localtime[0])+'-'+str(localtime[1]-1)+'-'+str(month[localtime[1]-1])
		else:
			lastmonth=str(localtime[0])+'-'+str(localtime[1]-1)+'-'+str(localtime[2])
	return nowtime,lastmonth

#计算年龄
def CalculateAge(Birthday):
	if Birthday==None:#未填出生日期
		return -1
	Today=datetime.date.today()
	if (Today.month>Birthday.month):
		return Today.year-Birthday.year
	elif (Today.month<Birthday.month):
		return Today.year-Birthday.year-1
	else:
		if (Today.day>=Birthday.day):
			return Today.year-Birthday.year
		else:
			return Today.year-Birthday.year-1

#计算职位是否在有效期内,数据库中没有效期设定,这里设置成30天?
# def CalculateJobIfEffect(Job_Publish_Date):
# 	Today=datetime.datetime.today()
# 	days=(Today-Job_Publish_Date).days
# 	if days>30:
# 		return 0
# 	return 1


#获取训练数据
def getTrainData(nowtime,lastmonth):
	train=dict()

	# #JW_QUERY_LOG
	# sql="SELECT [Jw_SN]\
	# 		,[Job_SN]\
	# 	FROM [AnalysisData].[dbo].[JW_QUERY_LOG]\
	# 	WHERE VDate between '%s' and '%s'\
	# 	and [Job_SN] in (select [Job_SN] from [AnalysisData].[dbo].[JOB_OFFER] where \
	#	[Job_Publish_Date] between '%s' and '%s')" \
	#	% (lastmonth,nowtime,lastmonth,nowtime)
	

	# result=DBQuery(sql)
	# for data in result:
	# 	if data[0] not in train:
	# 		train[data[0]]=dict()
	# 	train[data[0]][data[1]]=0.1 #查看行为兴趣设定

	#JOB_FAV
	sql="SELECT [Jw_SN]\
			,[Job_SN]\
		FROM [AnalysisData].[dbo].[JOB_FAV]\
		WHERE Add_Date between '%s' and '%s' \
		and [Job_SN] in (select [Job_SN] from [AnalysisData].[dbo].[JOB_OFFER] where \
		[Job_Publish_Date] between '%s' and '%s')" \
		% (lastmonth,nowtime,lastmonth,nowtime)

	result=DBQuery(sql)
	for data in result:
		if data[0] not in train:
			train[data[0]]=dict()
		train[data[0]][data[1]]=0.3 #收藏行为兴趣设定

	#JWAPPLYJOB
	sql="SELECT [Jw_SN]\
			,[Job_SN]\
		FROM [AnalysisData].[dbo].[JWAPPLYJOB]\
		WHERE Apply_Date between '%s' and '%s' \
		and [Job_SN] in (select [Job_SN] from [AnalysisData].[dbo].[JOB_OFFER] where \
		[Job_Publish_Date] between '%s' and '%s')" \
		% (lastmonth,nowtime,lastmonth,nowtime)

	result=DBQuery(sql)
	for data in result:
		if data[0] not in train:
			train[data[0]]=dict()
		train[data[0]][data[1]]=0.6 #应聘行为兴趣设定

	return train

#获取求职者要求及资格
def getJWINFO(Jw_SN):
	
	JWINFO=dict()
	sql="SELECT [Jw_Type]\
		,[Res_Sex]\
		,[Res_birthday]\
		,[Res_Learn]\
		,[Res_Expr_Years]\
		,[Res_SN]\
		from [AnalysisData].[dbo].[JWINFO]\
		where [Jw_SN]="+str(Jw_SN)
	result=DBQuery(sql)

	#数据库不完整,缺失数据
	if result==[]:
		return JWINFO

	for data in result:
		JWINFO['Jw_Type']=data[0]
		JWINFO['Res_Sex']=data[1]
		JWINFO['Age']=CalculateAge(data[2])
		JWINFO['Res_Learn']=data[3]
		JWINFO['Res_Expr_Years']=data[4]
		JWINFO['Res_SN']=data[5]



	if JWINFO['Res_SN']==0:
		JWINFO['Res_Money']=0
		JWINFO['Res_JobType1']=0
		JWINFO['Res_JobType2']=0
		JWINFO['Res_JobType3']=0
		JWINFO['Res_Jobkind']=0
		JWINFO['Res_Workcity1']=0
		JWINFO['Res_Workcity2']=0
		JWINFO['Res_Workcity3']=0
	else:
		sql="SELECT [Res_Money]\
			,[Res_JobType1]\
			,[Res_JobType2]\
			,[Res_JobType3]\
			,[Res_Jobkind]\
			,[Res_Workcity1]\
			,[Res_Workcity2]\
			,[Res_Workcity3]\
			FROM [AnalysisData].[dbo].[RESUME]\
			where [Res_SN]="+str(JWINFO['Res_SN'])
		result=DBQuery(sql)
		for data in result:
			JWINFO['Res_Money']=data[0]
			JWINFO['Res_JobType1']=data[1]
			JWINFO['Res_JobType2']=data[2]
			JWINFO['Res_JobType3']=data[3]
			JWINFO['Res_Jobkind']=data[4]
			JWINFO['Res_Workcity1']=data[5]
			JWINFO['Res_Workcity2']=data[6]
			JWINFO['Res_Workcity3']=data[7]
	return JWINFO

#获取职位要求
def getJOB_OFFER(Job_SN):
	JOB_OFFER=dict()
	sql="SELECT [Job_Publish_Date]\
		,[JobType]\
		,[Job_Money]\
		,[Job_Learn_Limited]\
		,[Job_Sex]\
		,[Job_Kind]\
		,[Job_Agelowest]\
		,[Job_Agehighest]\
		,[Job_Expr_Years]\
		,[Job_Workplace_Code]\
		FROM [AnalysisData].[dbo].[JOB_OFFER]\
		where [Job_SN]="+str(Job_SN)
	result=DBQuery(sql)
	#数据库不完整,缺失数据
	if result==[]:
		return JOB_OFFER
	for data in result:
		# JOB_OFFER['Job_effect']=CalculateJobIfEffect(data[0])
		JOB_OFFER['JobType']=data[1]
		JOB_OFFER['Job_Money']=data[2]
		JOB_OFFER['Job_Learn_Limited']=data[3]
		JOB_OFFER['Job_Sex']=data[4]
		JOB_OFFER['Job_Kind']=data[5]
		JOB_OFFER['Job_Agelowest']=data[6]
		JOB_OFFER['Job_Agehighest']=data[7]
		JOB_OFFER['Job_Expr_Years']=data[8]
		JOB_OFFER['Job_Workplace_Code']=data[9]

	return JOB_OFFER

#获取符合用户u的职位
def getJW_cando(u,nowtime,lastmonth):
	JWINFO=getJWINFO(u)
	if 'Res_SN' not in JWINFO:
		return []
	sql="SELECT [Job_SN] \
	FROM [AnalysisData].[dbo].[JOB_OFFER] \
	where Job_Publish_Date between '%s' and '%s' \
	and ((Job_Workplace_Code/100=%s/100 or Job_Workplace_Code/100=%s/100 or Job_Workplace_Code/100=%s/100 ) or (%s=0 and %s=0 and %s=0 ) or \
		((Job_Workplace_Code%%10000=0 or %s%%10000=0) and (Job_Workplace_Code/10000=%s/10000) ) or \
		((Job_Workplace_Code%%10000=0 or %s%%10000=0) and (Job_Workplace_Code/10000=%s/10000) ) or \
		((Job_Workplace_Code%%10000=0 or %s%%10000=0) and (Job_Workplace_Code/10000=%s/10000) ) )\
	and ( (JobType=%s or JobType=%s or JobType=%s ) or (%s=0 and %s=0 and %s=0) or \
		((JobType%%1000=0 or %s%%1000=0) and (JobType/1000=%s/1000) ) or \
		((JobType%%1000=0 or %s%%1000=0) and (JobType/1000=%s/1000) ) or \
		((JobType%%1000=0 or %s%%1000=0) and (JobType/1000=%s/1000) ) )\
	and (Job_Money>=%s or %s=15) \
	and  (Job_Learn_Limited<=%s or %s=0) \
	and  (Job_Sex=%s or Job_Sex=0) \
	and  (Job_Kind='%s' or '%s'='0') \
	and  (Job_Agelowest<=%s or %s=-1) \
	and (Job_Agehighest=0 or Job_Agehighest>=%s) \
	and (Job_Expr_Years<=%s)"\
	% (lastmonth,nowtime,JWINFO['Res_Workcity1']\
		,JWINFO['Res_Workcity2'],JWINFO['Res_Workcity3']\
		,JWINFO['Res_Workcity1'],JWINFO['Res_Workcity2']\
		,JWINFO['Res_Workcity3'],JWINFO['Res_Workcity1']\
		,JWINFO['Res_Workcity1'],JWINFO['Res_Workcity2']\
		,JWINFO['Res_Workcity2'],JWINFO['Res_Workcity3']\
		,JWINFO['Res_Workcity3'],JWINFO['Res_JobType1']\
		,JWINFO['Res_JobType2'],JWINFO['Res_JobType3']\
		,JWINFO['Res_JobType1'],JWINFO['Res_JobType2']\
		,JWINFO['Res_JobType3'],JWINFO['Res_JobType1']\
		,JWINFO['Res_JobType1'],JWINFO['Res_JobType2']\
		,JWINFO['Res_JobType2'],JWINFO['Res_JobType3']\
		,JWINFO['Res_JobType3'],JWINFO['Res_Money']\
		,JWINFO['Res_Money'],JWINFO['Res_Learn']\
		,JWINFO['Res_Learn'],JWINFO['Res_Sex']\
		,JWINFO['Res_Jobkind'],JWINFO['Res_Jobkind']\
		,JWINFO['Age'],JWINFO['Age'],JWINFO['Age']\
		,JWINFO['Res_Expr_Years'])	
	result=DBQuery(sql)
	ilist=[ data[0] for data in result]
	return ilist

#获得所有Jw_SN
def getAllJw_SN():
	sql="SELECT [Jw_SN]\
 	 FROM [AnalysisData].[dbo].[JWINFO]"
 	result=DBQuery(sql)
 	Jw_SN=list()
 	for data in result:
 		Jw_SN.append(data[0])
 	return Jw_SN

#获得最新一个月内所有职位
def getAllJob_SN(nowtime,lastmonth):
	
	sql="SELECT distinct Job_SN \
	from [AnalysisData].[dbo].[JOB_OFFER] \
	where Job_Publish_Date between '%s' and '%s'"\
	% (lastmonth,nowtime)
	allJob_SN=list()
	result=DBQuery(sql)
	for data in result:
		allJob_SN.append(data[0])

	return allJob_SN