#!usr/bin/env python
# -*- coding:utf-8 -*-
#获得数据
from DB import *
import datetime

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
def getTrainData():
	train=dict()

	# #JW_QUERY_LOG
	# sql="SELECT [Jw_SN]\
	# 		,[Job_SN]\
	# 	FROM [AnalysisData].[dbo].[JW_QUERY_LOG]\
	# 	WHERE VDate between '2014-04-01' and '2014-05-01'\
	# 	and [Job_SN] in (select [Job_SN] from [AnalysisData].[dbo].[JOB_OFFER] where \
	#	[Job_Publish_Date] between '2014-04-01' and '2014-05-01')"
	

	# result=DBQuery(sql)
	# for data in result:
	# 	if data[0] not in train:
	# 		train[data[0]]=dict()
	# 	train[data[0]][data[1]]=0.1 #查看行为兴趣设定

	#JOB_FAV
	sql="SELECT [Jw_SN]\
			,[Job_SN]\
		FROM [AnalysisData].[dbo].[JOB_FAV]\
		WHERE Add_Date between '2014-04-01' and '2014-05-01' \
		and [Job_SN] in (select [Job_SN] from [AnalysisData].[dbo].[JOB_OFFER] where \
		[Job_Publish_Date] between '2014-04-01' and '2014-05-01')"

	result=DBQuery(sql)
	for data in result:
		if data[0] not in train:
			train[data[0]]=dict()
		train[data[0]][data[1]]=0.3 #收藏行为兴趣设定

	#JWAPPLYJOB
	sql="SELECT [Jw_SN]\
			,[Job_SN]\
		FROM [AnalysisData].[dbo].[JWAPPLYJOB]\
		WHERE Apply_Date between '2014-04-01' and '2014-05-01' \
		and [Job_SN] in (select [Job_SN] from [AnalysisData].[dbo].[JOB_OFFER] where \
		[Job_Publish_Date] between '2014-04-01' and '2014-05-01')"
	
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