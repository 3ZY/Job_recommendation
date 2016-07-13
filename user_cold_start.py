#!usr/bin/env python
# -*- coding:utf-8 -*-
#用户冷启动
from __future__ import division
from DB import *
from filTer import *
from getData import *
import math
import operator


#获得最新一个月内行为数不为0的N(i)，N(i)是对职位i发生过行为的用户数
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
		group by [Job_SN]" \
		% (lastmonth,nowtime)

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
			and	((Job_Workplace_Code/100=%s/100 or Job_Workplace_Code/100=%s/100 or Job_Workplace_Code/100=%s/100 ) or (%s=0 and %s=0 and %s=0 ) or \
				((Job_Workplace_Code%%10000=0 or %s%%10000=0) and (Job_Workplace_Code/10000=%s/10000) ) or \
				((Job_Workplace_Code%%10000=0 or %s%%10000=0) and (Job_Workplace_Code/10000=%s/10000) ) or \
				((Job_Workplace_Code%%10000=0 or %s%%10000=0) and (Job_Workplace_Code/10000=%s/10000) ) )\
			and ( (JobType=%s or JobType=%s or JobType=%s ) or (%s=0 and %s=0 and %s=0) or \
				((JobType%%1000=0 or %s%%1000=0) and (JobType/1000=%s/1000) ) or \
				((JobType%%1000=0 or %s%%1000=0) and (JobType/1000=%s/1000) ) or \
				((JobType%%1000=0 or %s%%1000=0) and (JobType/1000=%s/1000) ) )\
		)b on b.[Job_SN]=a.Job_SN\
		) tmp\
		group by [Job_SN]" \
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
		,JWINFO['Res_JobType3'])

	result=DBQuery(sql)
	if result==[]:
		return Recommend
	
	#计算p(f,i)，p(f,i)定义为喜欢职位i的求职者中具有特征f的比例
	for data in result:
		Recommend[data[1]]=data[0]/(Ni[data[1]]+100)
	
	return Recommend

#city_type_most_popular推荐结果
def city_type_most_popular_finallyRecommend(Jw_SN,nowtime,lastmonth):
	Ni=getNi(nowtime,lastmonth)
	finallyRecommend=dict()
	for u in Jw_SN:
		finallyRecommend[u]=dict()
		#JWINFO=getJWINFO(u)#获取求职者要求及资格
		uilist=getJW_cando(u,nowtime,lastmonth)#获取符合求职者的职位
		count=8 #推荐职位数
		u_recommend=city_type_most_popular_Recommend(u,Ni,nowtime,lastmonth)
		if u_recommend=={}:
			continue
		for i,pif in sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True):
			#规则过滤 性别不符、学历不符等
			#JOB_OFFER=getJOB_OFFER(i)#获取职位要求
			#是否符合要求
			#if jobIfEffect(JWINFO,JOB_OFFER)==1:
			if i in uilist:
				count-=1
				finallyRecommend[u][i]=pif
			if count==0:
				break
	return finallyRecommend

# most_popular推荐结果
def most_popular_finallyRecommend(Jw_SN,nowtime,lastmonth):
	Ni=getNi(nowtime,lastmonth)
	finallyRecommend=dict()
	for u in Jw_SN:
		finallyRecommend[u]=dict()
		#JWINFO=getJWINFO(u)#获取求职者要求及资格
		uilist=getJW_cando(u,nowtime,lastmonth)#获取符合求职者的职位
		count=8#推荐职位数
		for i,ni in sorted(Ni.items(),key=operator.itemgetter(1),reverse=True):
			#规则过滤 性别不符、学历不符等
			#JOB_OFFER=getJOB_OFFER(i)#获取职位要求
			#是否符合要求
			#if jobIfEffect(JWINFO,JOB_OFFER)==1:
			if i in uilist:
				count-=1
				finallyRecommend[u][i]=ni
			if count==0:
				break
	return finallyRecommend

#无算法推荐
def noal_finallyRecommend(Jw_SN,nowtime,lastmonth):
	finallyRecommend=dict()
	for u in Jw_SN:
		finallyRecommend[u]=dict()
		uilist=getJW_cando(u,nowtime,lastmonth)#获取符合求职者的职位
		count=8#推荐职位数
		for i in uilist:
			count-=1
			finallyRecommend[u][i]=0.001
			if count==0:
				break
	return finallyRecommend


