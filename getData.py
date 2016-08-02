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

	#JW_QUERY_LOG
	sql="SELECT [Jw_SN]\
			,[Job_SN]\
		FROM [AnalysisData].[dbo].[JW_QUERY_LOG]\
		WHERE VDate between '%s' and '%s'\
		and [Job_SN] in (select [Job_SN] from [AnalysisData].[dbo].[JOB_OFFER] where \
		[Job_Publish_Date] between '%s' and '%s')" \
		% (lastmonth,nowtime,lastmonth,nowtime)


	result=DBQuery(sql)
	for data in result:
		if data[0] not in train:
			train[data[0]]=dict()
		train[data[0]][data[1]]=0.1 #查看行为兴趣设定

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
		train[data[0]][data[1]]=0.3 #应聘行为兴趣设定

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
		train[data[0]][data[1]]=0.6 #收藏行为兴趣设定

	return train

#获得时间段内行为数不为0的N(i)，N(i)是对职位i发生过行为的用户数
def getNi(nowtime,lastmonth):

	# sql得出N(i)
	sql="SELECT count(distinct [Jw_SN]) as num\
				,[Job_SN]\
		from \
		(\
		select [Jw_SN]\
		      ,a.[Job_SN]\
		from \
		(\
		SELECT [Jw_SN]\
		      ,[Job_SN]\
		  FROM [AnalysisData].[dbo].[JOB_FAV]\
		union all\
		SELECT [Jw_SN]\
		      ,[Job_SN]\
		  FROM [AnalysisData].[dbo].[JW_QUERY_LOG]\
		union all\
		SELECT [Jw_SN]\
		      ,[Job_SN]\
		  FROM [AnalysisData].[dbo].[JWAPPLYJOB]\
		) a \
		join \
		(\
		SELECT [Job_SN]\
		      ,[Job_Publish_Date]\
		  FROM [AnalysisData].[dbo].[JOB_OFFER]\
		  where Job_Publish_Date between '%s' and '%s' \
		)b on b.[Job_SN]=a.Job_SN\
		) tmp\
		group by [Job_SN] " \
		% (lastmonth,nowtime)

	result=DBQuery(sql)
	Ni=dict()
	for data in result:
		Ni[data[1]]=data[0]
	return Ni

#获得JWINFO及JOB_OFFER,求职者信息及职位信息
def getJWJOBINFO(nowtime,lastmonth):
	JWINFO=dict()
	RESUME=dict()
	JOB_OFFER=dict()
	sql="SELECT [Res_SN]\
			,[Res_Money]\
			,[Res_JobType1]\
			,[Res_JobType2]\
			,[Res_JobType3]\
			,[Res_Jobkind]\
			,[Res_Workcity1]\
			,[Res_Workcity2]\
			,[Res_Workcity3]\
			FROM [AnalysisData].[dbo].[RESUME]"
	result=DBQuery(sql)
	for data in result:
		RESUME[data[0]]=dict()
		RESUME[data[0]]['Res_Money']=data[1]
		RESUME[data[0]]['Res_JobType1']=data[2]
		RESUME[data[0]]['Res_JobType2']=data[3]
		RESUME[data[0]]['Res_JobType3']=data[4]
		RESUME[data[0]]['Res_Jobkind']=data[5]
		RESUME[data[0]]['Res_Workcity1']=data[6]
		RESUME[data[0]]['Res_Workcity2']=data[7]
		RESUME[data[0]]['Res_Workcity3']=data[8]

	sql="SELECT [Jw_SN]\
		,[Jw_Type]\
		,[Res_Sex]\
		,[Res_birthday]\
		,[Res_Learn]\
		,[Res_Expr_Years]\
		,[Res_SN]\
		from [AnalysisData].[dbo].[JWINFO]"
	result=DBQuery(sql)
	for data in result:
		JWINFO[data[0]]=dict()
		JWINFO[data[0]]['Jw_Type']=data[1]
		JWINFO[data[0]]['Res_Sex']=data[2]
		JWINFO[data[0]]['Age']=CalculateAge(data[3])
		JWINFO[data[0]]['Res_Learn']=data[4]
		JWINFO[data[0]]['Res_Expr_Years']=data[5]
		JWINFO[data[0]]['Res_SN']=data[6]
		if JWINFO[data[0]]['Res_SN']==0:
			JWINFO[data[0]]['Res_Money']=0
			JWINFO[data[0]]['Res_JobType1']=0
			JWINFO[data[0]]['Res_JobType2']=0
			JWINFO[data[0]]['Res_JobType3']=0
			JWINFO[data[0]]['Res_Jobkind']=0
			JWINFO[data[0]]['Res_Workcity1']=0
			JWINFO[data[0]]['Res_Workcity2']=0
			JWINFO[data[0]]['Res_Workcity3']=0
		else:
			JWINFO[data[0]]['Res_Money']=RESUME[data[6]]['Res_Money']
			JWINFO[data[0]]['Res_JobType1']=RESUME[data[6]]['Res_JobType1']
			JWINFO[data[0]]['Res_JobType2']=RESUME[data[6]]['Res_JobType2']
			JWINFO[data[0]]['Res_JobType3']=RESUME[data[6]]['Res_JobType3']
			JWINFO[data[0]]['Res_Jobkind']=RESUME[data[6]]['Res_Jobkind']
			JWINFO[data[0]]['Res_Workcity1']=RESUME[data[6]]['Res_Workcity1']
			JWINFO[data[0]]['Res_Workcity2']=RESUME[data[6]]['Res_Workcity2']
			JWINFO[data[0]]['Res_Workcity3']=RESUME[data[6]]['Res_Workcity3']
	del RESUME

	sql="SELECT [Job_SN]\
		,[Job_Publish_Date]\
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
		where Job_Publish_Date between '%s' and '%s'"\
		% (lastmonth,nowtime)
	result=DBQuery(sql)
	for data in result:
		JOB_OFFER[data[0]]=dict()
		JOB_OFFER[data[0]]['JobType']=data[2]
		JOB_OFFER[data[0]]['Job_Money']=data[3]
		JOB_OFFER[data[0]]['Job_Learn_Limited']=data[4]
		JOB_OFFER[data[0]]['Job_Sex']=data[5]
		JOB_OFFER[data[0]]['Job_Kind']=data[6]
		JOB_OFFER[data[0]]['Job_Agelowest']=data[7]
		JOB_OFFER[data[0]]['Job_Agehighest']=data[8]
		JOB_OFFER[data[0]]['Job_Expr_Years']=data[9]
		JOB_OFFER[data[0]]['Job_Workplace_Code']=data[10]
	return JWINFO,JOB_OFFER


#获得所有Jw_SN
def getAllJw_SN():
	sql="SELECT [Jw_SN]\
 	 FROM [AnalysisData].[dbo].[JWINFO]"
 	result=DBQuery(sql)
 	Jw_SN=list()
 	for data in result:
 		Jw_SN.append(data[0])
 	return Jw_SN

#获得时间段内所有职位
def getAllJob_SN(nowtime,lastmonth):

	sql="SELECT Job_SN \
	from [AnalysisData].[dbo].[JOB_OFFER] \
	where Job_Publish_Date between '%s' and '%s' \
	order by Job_Publish_Date desc"\
	% (lastmonth,nowtime)
	allJob_SN=list()
	result=DBQuery(sql)
	for data in result:
		allJob_SN.append(data[0])

	return allJob_SN
