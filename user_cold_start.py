#!usr/bin/env python
# -*- coding:utf-8 -*-
#用户冷启动
from __future__ import division
from filTer import *
import math
import operator

# most_popular推荐结果
def most_popular_finallyRecommend(Jw_SN,nowtime,lastmonth,JWINFO,JOB_OFFER,Ni,R_Num=10,finallyRecommend={}):
	for u in Jw_SN:
		finallyRecommend.setdefault(u,{})
		#完全匹配的职位
		alreadyRecommendNum=len(finallyRecommend[u])#已经推荐数
		if alreadyRecommendNum>=R_Num*3:
			continue
		count=R_Num*3-alreadyRecommendNum#推荐职位数
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

def CB_fill_finallyRecommend(Jw_SN,Job_SN,nowtime,lastmonth,JWINFO,JOB_OFFER,Ni,R_Num=10,finallyRecommend={}):
	for u in Jw_SN:
		finallyRecommend.setdefault(u,{})
		#基于简历内容推荐
		alreadyRecommendNum=len(finallyRecommend[u])#已经推荐数
		if alreadyRecommendNum>=R_Num*3:
			continue
		count=R_Num*3-alreadyRecommendNum#推荐职位数
		for i in Job_SN:
			if i in finallyRecommend[u]:#已推荐过
				continue
			if jobIfEffect(JWINFO[u],JOB_OFFER[i])==1:
				count-=1
				finallyRecommend[u][i]=0.006
			if count==0:
				break

		#推荐补全
		alreadyRecommendNum=len(finallyRecommend[u])#已经推荐数
		if alreadyRecommendNum>=R_Num:
			continue
		count=R_Num-alreadyRecommendNum#推荐职位数
		for i in Job_SN:
			if i in finallyRecommend[u]:#已推荐过
				continue
			if city_tpye_IfEffect(JWINFO[u],JOB_OFFER[i])==1:
				count-=1
				finallyRecommend[u][i]=0.004
			if count==0:
				break

		alreadyRecommendNum=len(finallyRecommend[u])#已经推荐数
		if alreadyRecommendNum>=R_Num:
			continue
		count=R_Num-alreadyRecommendNum#推荐职位数
		for i in Job_SN:
			if i in finallyRecommend[u]:#已推荐过
				continue
			if sex_city_IfEffect(JWINFO[u],JOB_OFFER[i])==1:
				count-=1
				finallyRecommend[u][i]=0.002
			if count==0:
				break

		alreadyRecommendNum=len(finallyRecommend[u])#已经推荐数
		if alreadyRecommendNum>=R_Num:
			continue
		count=R_Num-alreadyRecommendNum#推荐职位数
		for i,ni in sorted(Ni.items(),key=operator.itemgetter(1),reverse=True):
			if i in finallyRecommend[u]:#已推荐过
				continue
			if sex_IfEffect(JWINFO[u],JOB_OFFER[i])==1:
				count-=1
				finallyRecommend[u][i]=0.001
			if count==0:
				break

	return finallyRecommend
