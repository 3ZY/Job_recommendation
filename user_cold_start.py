#!usr/bin/env python
# -*- coding:utf-8 -*-
#用户冷启动
from __future__ import division
from DB import *
from filTer import *
from getData import *
import time
import math
import operator

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
	
	#sql="SELECT distinct Job_SN from [AnalysisData].[dbo].[JOB_OFFER] where Job_Publish_Date between "+lastmonth+" and "+nowtime

	sql="SELECT distinct Job_SN from [AnalysisData].[dbo].[JOB_OFFER] where Job_Publish_Date between '2014-4-01' and '2014-4-30'"
	allJob_SN=list()
	result=DBQuery(sql)
	for data in result:
		allJob_SN.append(data[0])

	return allJob_SN

#获得最新一个月内行为数不为0的N(i)，N(i)是对职位i发生过行为的用户数
def getNi(nowtime,lastmonth):
	
	# sql得出N(i)
	# sql="SELECT count(distinct [Jw_SN]) as num\
	# 			,[Job_SN]\
	# 	from \
	# 	(\
	# 	select [Jw_SN]\
	# 	      ,a.[Job_SN]\
	# 	from \
	# 	(\
	# 	SELECT [Jw_SN]\
	# 	      ,[Job_SN]\
	# 	  FROM [AnalysisData].[dbo].[JOB_FAV]\
	# 	union all\
	# 	SELECT [Jw_SN]\
	# 	      ,[Job_SN]\
	# 	  FROM [AnalysisData].[dbo].[JW_QUERY_LOG]\
	# 	union all\
	# 	SELECT [Jw_SN]\
	# 	      ,[Job_SN]\
	# 	  FROM [AnalysisData].[dbo].[JWAPPLYJOB]\
	# 	) a \
	# 	join \
	# 	(\
	# 	SELECT [Job_SN]\
	# 	      ,[Job_Publish_Date]\
	# 	  FROM [AnalysisData].[dbo].[JOB_OFFER]\
	# 	  where Job_Publish_Date between "+lastmonth+" and "+nowtime+" \
	# 	)b on b.[Job_SN]=a.Job_SN\
	# 	) tmp\
	# 	group by [Job_SN]"

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
		  where Job_Publish_Date between '2014-4-01' and '2014-4-30'\
		)b on b.[Job_SN]=a.Job_SN\
		) tmp\
		group by [Job_SN]"

	result=DBQuery(sql)
	Ni=dict()
	for data in result:
		Ni[data[1]]=data[0]
	return Ni

#给用户推荐对于和他同一个期望工作地点类型的用户当中最热门的职位
def city_type_most_popular_Recommend(u,Ni,nowtime,lastmonth):
	JWINFO=getJWINFO(u)
	Recommend=dict()
	if 'Res_SN' not in JWINFO:
		return Recommend

	# sql得出n(i)&u(f)
	# sql="SELECT count(distinct [Jw_SN]) as num\
	# 			,[Job_SN]\
	# 	from \
	# 	(\
	# 	select [Jw_SN]\
	# 	      ,a.[Job_SN]\
	# 	from \
	# 	(\
	# 	SELECT [Jw_SN]\
	# 	      ,[Job_SN]\
	# 	  FROM [AnalysisData].[dbo].[JOB_FAV]\
	# 	union all\
	# 	SELECT [Jw_SN]\
	# 	      ,[Job_SN]\
	# 	  FROM [AnalysisData].[dbo].[JW_QUERY_LOG]\
	# 	union all\
	# 	SELECT [Jw_SN]\
	# 	      ,[Job_SN]\
	# 	  FROM [AnalysisData].[dbo].[JWAPPLYJOB]\
	# 	) a \
	# 	join \
	# 	(\
	# 	SELECT [Job_SN]\
	# 	      ,[Job_Publish_Date]\
	# 	  FROM [AnalysisData].[dbo].[JOB_OFFER]\
	# 	  where Job_Publish_Date between "+lastmonth+" and "+nowtime+" and \
	# 			 ((Job_Workplace_Code="+str(JWINFO['Res_Workcity1'])+" or \
	# 			 Job_Workplace_Code="+str(JWINFO['Res_Workcity2'])+" or \
	# 			 Job_Workplace_Code="+str(JWINFO['Res_Workcity3'])+" ) or \
	# 			 ("+str(JWINFO['Res_Workcity1'])+"=0 and \
	# 			 	"+str(JWINFO['Res_Workcity2'])+"=0 and \
	# 			 	"+str(JWINFO['Res_Workcity2'])+"=0 ) ) and \
	# 			 ( (JobType="+str(JWINFO['Res_JobType1'])+" or \
	# 			 	JobType="+str(JWINFO['Res_JobType2'])+" or \
	# 			 	JobType="+str(JWINFO['Res_JobType3'])+" ) or \
	# 			 	("+str(JWINFO['Res_JobType1'])+"=0 and \
	# 			 	 "+str(JWINFO['Res_JobType2'])+"=0 and \
	# 			 	 "+str(JWINFO['Res_JobType3'])+"=0) )\
	# 	)b on b.[Job_SN]=a.Job_SN\
	# 	) tmp\
	# 	group by [Job_SN]"

	# sql得出n(i)&u(f)
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
		  where Job_Publish_Date between '2014-4-01' and '2014-4-30' and \
				 ((Job_Workplace_Code="+str(JWINFO['Res_Workcity1'])+" or \
				 Job_Workplace_Code="+str(JWINFO['Res_Workcity2'])+" or \
				 Job_Workplace_Code="+str(JWINFO['Res_Workcity3'])+" ) or \
				 ("+str(JWINFO['Res_Workcity1'])+"=0 and \
				 	"+str(JWINFO['Res_Workcity2'])+"=0 and \
				 	"+str(JWINFO['Res_Workcity2'])+"=0 ) ) and \
				 ( (JobType="+str(JWINFO['Res_JobType1'])+" or \
				 	JobType="+str(JWINFO['Res_JobType2'])+" or \
				 	JobType="+str(JWINFO['Res_JobType3'])+" ) or \
				 	("+str(JWINFO['Res_JobType1'])+"=0 and \
				 	 "+str(JWINFO['Res_JobType2'])+"=0 and \
				 	 "+str(JWINFO['Res_JobType3'])+"=0) )\
		)b on b.[Job_SN]=a.Job_SN\
		) tmp\
		group by [Job_SN]"
	result=DBQuery(sql)
	if result==[]:
		return Recommend
	
	#计算p(f,i)，p(f,i)定义为喜欢职位i的求职者中具有特征f的比例
	for data in result:
		Recommend[data[1]]=data[0]/(Ni[data[1]]+100)
	
	return Recommend

#city_type_most_popular推荐结果
def city_type_most_popular_finallyRecommend(Jw_SN):
	nowtime,lastmonth=getTimes()
	Ni=getNi(nowtime,lastmonth)
	finallyRecommend=dict()
	for u in Jw_SN:
		finallyRecommend[u]=dict()
		JWINFO=getJWINFO(u)#获取求职者要求及资格
		count=8 #推荐职位数
		u_recommend=city_type_most_popular_Recommend(u,Ni,nowtime,lastmonth)
		if u_recommend=={}:
			continue
		for i,pif in sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True):
			#规则过滤 性别不符、学历不符等
			JOB_OFFER=getJOB_OFFER(i)#获取职位要求
			#是否符合要求
			if jobIfEffect(JWINFO,JOB_OFFER)==1:
				count-=1
				finallyRecommend[u][i]=pif
			if count==0:
				break
	return finallyRecommend

# most_popular推荐结果
def most_popular_finallyRecommend(Jw_SN):
	nowtime,lastmonth=getTimes()
	Ni=getNi(nowtime,lastmonth)
	finallyRecommend=dict()
	for u in Jw_SN:
		finallyRecommend[u]=dict()
		JWINFO=getJWINFO(u)#获取求职者要求及资格
		count=8 #推荐职位数
		for i,ni in sorted(Ni.items(),key=operator.itemgetter(1),reverse=True):
			#规则过滤 性别不符、学历不符等
			JOB_OFFER=getJOB_OFFER(i)#获取职位要求
			#是否符合要求
			if jobIfEffect(JWINFO,JOB_OFFER)==1:
				count-=1
				finallyRecommend[u][i]=ni
			if count==0:
				break
	return finallyRecommend

nowtime,lastmonth=getTimes()
allJob_SN=getAllJob_SN(nowtime,lastmonth)
Jw_SN=getAllJw_SN()
finallyRecommend=city_type_most_popular_finallyRecommend(Jw_SN)
#finallyRecommend=most_popular_finallyRecommend(Jw_SN)
# for u,u_recommend in finallyRecommend.items():
# 	print u,len(u_recommend)