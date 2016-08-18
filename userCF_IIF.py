#!usr/bin/env python
# -*- coding:utf-8 -*-
#userCF-IIF
from __future__ import division
from filTer import *
import math
import operator

#获取求职者间的相似度
def UserSimilarity(item_users,goal_users,N):
	#计算求职者协同率
	C=dict()
	for i, users in item_users.items():
		for u in users:
			if u not in goal_users:
				continue
			for v in users:
				if u==v:
					continue
				C.setdefault(u,{})
				C[u].setdefault(v,0)
				C[u][v]+= 1 / math.log(1+len(users))
	W=dict()
	#计算求职者最终相似度
	for u, related_users in C.items():
		for v,cuv in related_users.items():
			W.setdefault(u,{})
			W[u][v]=cuv / math.sqrt(N[u]*N[v])
	return W

#对user推荐item rank
def userCF_IIF_Recommend(user,train,W,JOB_OFFER):
	K=50 #兴趣最接近的K个求职者
	rank=dict()
	interacted_items = train[user]
	for v, wuv in sorted(W[user].items(),key=operator.itemgetter(1),reverse=True)[0:K]:
		for i, rvi in train[v].items():
			if i in interacted_items:#过滤求职者浏览、应聘、收藏过的职位
				continue
			if i not in JOB_OFFER:#非目标职位
				continue
			if i not in rank:
				rank[i]=0
			rank[i]+=wuv*rvi
	return rank

#userCF-IIF推荐结果
def userCF_IIF_finallyRecommend(train,JWINFO,JOB_OFFER,R_Num=10,K=1000):
	finallyRecommend={}
	#建立职位到求职者的倒序表及求职者喜欢的职位数
	item_users=dict()
	N=dict()
	for u, items in train.items():
		N[u]=len(items.keys())
		for i in items.keys():
			if i not in item_users:
				item_users[i]=set()
			item_users[i].add(u)

	K=int(K) #分批推荐
	iter_n=int( (len(train.keys())+K-1)/K ) #循环次数
	for j in xrange(iter_n):
		goal_users=train.keys()[K*j:K*(j+1)]
		W=UserSimilarity(item_users,goal_users,N)
		for u in goal_users:
			if (u not in W) or (u not in JWINFO):
				continue
			finallyRecommend.setdefault(u,{})
			u_recommend=userCF_IIF_Recommend(u,train,W,JOB_OFFER) #求职者u的推荐集合
			count=R_Num*3#推荐职位数
			for i,pui in sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True):
				if i in finallyRecommend[u]:#已推荐过
					continue
				#规则过滤 性别不符、学历不符等
				if jobIfEffect(JWINFO[u],JOB_OFFER[i])==1:
					count-=1
					finallyRecommend[u][i]=pui
				if count==0:
					break
		del W
	return finallyRecommend
