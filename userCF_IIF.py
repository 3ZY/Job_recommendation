#!usr/bin/env python
# -*- coding:utf-8 -*-
#userCF-IIF
from __future__ import division
from filTer import *
from getData import *
import math
import operator


#获取求职者间的相似度
def UserSimilarity(train):

	#建立职位到求职者的倒序表
	item_users=dict()
	for u, items in train.items():
		for i in items.keys():
			if i not in item_users:
				item_users[i]=set()
			item_users[i].add(u)
	
	#计算求职者协同率
	N=dict()
	C=dict()
	for i, users in item_users.items():
		for u in users:
			if u not in N:
				N[u]=0
			N[u] += 1
			for v in users:
				if u==v:
					continue
				if u not in C:
					C[u]=dict()
				if v not in C[u]:
					C[u][v]=0
				C[u][v]+= 1 / math.log(1+len(users))
	W=dict()
	#计算求职者最终相似度
	for u, related_users in C.items():
		for v,cuv in related_users.items():
			if u not in W:
				W[u]=dict()
			W[u][v]=cuv / math.sqrt(N[u]*N[v])

	return W

#对user推荐item rank
def userCF_IIF_Recommend(user,train,W):
	K=40 #兴趣最接近的K个求职者
	rank=dict()
	interacted_items = train[user]
	for v, wuv in sorted(W[user].items(),key=operator.itemgetter(1),reverse=True)[0:K]:
		for i, rvi in train[v].items():
			if i in interacted_items:
				#过滤求职者浏览、应聘、收藏过的职位
				continue
			if i not in rank:
				rank[i]=0
			rank[i]+=wuv*rvi

	return rank

#userCF-IIF推荐结果
def userCF_IIF_finallyRecommend(train):
	W=UserSimilarity(train)
	finallyRecommend=dict()
	for u in train.keys():
		if u not in W:
			continue
		finallyRecommend[u]=dict()
		JWINFO=getJWINFO(u)#获取求职者要求及资格
		u_recommend=userCF_IIF_Recommend(u,train,W) #求职者u的推荐集合
		count=8 #推荐职位数
		for i,pui in sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True):
			#规则过滤 性别不符、学历不符等
			JOB_OFFER=getJOB_OFFER(i)#获取职位要求
			#是否符合要求
			if jobIfEffect(JWINFO,JOB_OFFER)==1:
				count-=1
				finallyRecommend[u][i]=pui
			if count==0:
				break
	return finallyRecommend
