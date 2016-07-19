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
def city_type_most_popular_Recommend(u,Ni,item_users,JWINFO,JOB_OFFER):
	
	Recommend=dict()
	result=[]
	# 得出n(i)&u(f)
	for i,users in item_users.items():
		if i not in JOB_OFFER:
			continue
		u_num =0
		for u in users:
			if u not in JWINFO:
				continue
			if city_tpye_IfEffect(JWINFO[u],JOB_OFFER[i])==1:
				u_num+=1
		if u_num>0:
			result.append([u_num,i])

	if result==[]:
		return Recommend
	
	#计算p(f,i)，p(f,i)定义为喜欢职位i的求职者中具有特征f的比例
	for data in result:
		Recommend[data[1]]=data[0]/(Ni[data[1]]+100)
	
	return Recommend

#city_type_most_popular推荐结果
def city_type_most_popular_finallyRecommend(Jw_SN,nowtime,lastmonth,train,JWINFO,JOB_OFFER,R_Num=8,finallyRecommend={}):
	#建立职位到求职者的倒序表
	item_users=dict()
	for u, items in train.items():
		for i in items.keys():
			if i not in item_users:
				item_users[i]=set()
			item_users[i].add(u)
	Ni=getNi(nowtime,lastmonth)

	for u in Jw_SN:
		finallyRecommend.setdefault(u,{})
		alreadyRecommendNum=len(finallyRecommend[u])#已经推荐数
		if alreadyRecommendNum>=R_Num:
			continue
		count=R_Num-alreadyRecommendNum #推荐职位数
		u_recommend=city_type_most_popular_Recommend(u,Ni,item_users,JWINFO,JOB_OFFER)
		if u_recommend=={}:
			continue
		for i,pif in sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True):
			if i in finallyRecommend[u]:#已推荐过
				continue
			#规则过滤 性别不符、学历不符等
			if jobIfEffect(JWINFO[u],JOB_OFFER[i])==1:
				count-=1
				finallyRecommend[u][i]=pif
			if count==0:
				break
	return finallyRecommend

# most_popular推荐结果
def most_popular_finallyRecommend(Jw_SN,nowtime,lastmonth,JWINFO,JOB_OFFER,R_Num=8,finallyRecommend={}):
	Ni=getNi(nowtime,lastmonth)
	for u in Jw_SN:
		finallyRecommend.setdefault(u,{})
		alreadyRecommendNum=len(finallyRecommend[u])#已经推荐数
		if alreadyRecommendNum>=R_Num:
			continue
		count=R_Num-alreadyRecommendNum#推荐职位数
		for i,ni in sorted(Ni.items(),key=operator.itemgetter(1),reverse=True):
			if i in finallyRecommend[u]:#已推荐过
				continue
			#规则过滤 性别不符、学历不符等			
			if jobIfEffect(JWINFO[u],JOB_OFFER[i])==1:
				count-=1
				finallyRecommend[u][i]=0.01
			if count==0:
				break
	return finallyRecommend

#无算法推荐
def noal_finallyRecommend(Jw_SN,JWINFO,JOB_OFFER,allJob_SN,R_Num=8,finallyRecommend={}):
	for u in Jw_SN:
		finallyRecommend.setdefault(u,{})
		alreadyRecommendNum=len(finallyRecommend[u])#已经推荐数
		if alreadyRecommendNum>=R_Num:
			continue
		count=R_Num-alreadyRecommendNum#推荐职位数
		for i in allJob_SN:
			if i in finallyRecommend[u]:#已推荐过
				continue
			#规则过滤			
			if city_tpye_IfEffect(JWINFO[u],JOB_OFFER[i])==1:
				count-=1
				finallyRecommend[u][i]=0.001
			if count==0:
				break
	return finallyRecommend

#推荐补全
def fill_finallyRecommend(Jw_SN,nowtime,lastmonth,JWINFO,JOB_OFFER,R_Num=8,finallyRecommend={}):
	Ni=getNi(nowtime,lastmonth)
	for u in Jw_SN:
		finallyRecommend.setdefault(u,{})
		alreadyRecommendNum=len(finallyRecommend[u])#已经推荐数
		if alreadyRecommendNum>=R_Num:
			continue
		count=R_Num-alreadyRecommendNum#推荐职位数
		for i,ni in sorted(Ni.items(),key=operator.itemgetter(1),reverse=True):
			if i in finallyRecommend[u]:#已推荐过
				continue
			count-=1
			finallyRecommend[u][i]=0.005
			if count==0:
				break
	return finallyRecommend
