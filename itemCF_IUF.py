#!usr/bin/env python
# -*- coding:utf-8 -*-
#itemCF-IUF
from __future__ import division
from filTer import *
import math
import operator

#获取职位间的相似度
def ItemSimilarity(train):

	#计算职位协同率
	N=dict()
	C=dict()
	for u, items in train.items():
		for i in items.keys():
			if i not in N:
				N[i]=0
			N[i]+=1
			for j in items.keys():
				if i==j:
					continue
				if i not in C:
					C[i]=dict()
				if j not in C[i]:
					C[i][j]=0
				C[i][j] += 1 / math.log(1+len(items))

	W=dict()
	#计算职位最终相似度
	for i, related_items in C.items():
		for j,cij in related_items.items():
			if i not in W:
				W[i]=dict()
			W[i][j]=cij / math.sqrt(N[i]*N[j])

	return W

#对user推荐item rank
def itemCF_IUF_Recommend(user,train,W):
	K=100 #最相似的K个职位
	rank=dict()
	interacted_items = train[user]
	for i,pi in interacted_items.items():
		if i not in W:
			continue
		for j,wj in sorted(W[i].items(),key=operator.itemgetter(1),reverse=True)[0:K]:
			if j in interacted_items:
				#过滤求职者浏览、应聘、收藏过的职位
				continue
			if j not in rank:
				rank[j]=0
			rank[j]+=pi*wj

	return rank

#itemCF-IUF推荐结果
def itemCF_IUF_finallyRecommend(train,JWINFO,JOB_OFFER,R_Num=10,finallyRecommend={}):
	W=ItemSimilarity(train)
	for u in train.keys():
		if u not in JWINFO:
			continue
		finallyRecommend.setdefault(u,{})
		alreadyRecommendNum=len(finallyRecommend[u])#已经推荐数
		if alreadyRecommendNum>=R_Num*3:
			continue
		u_recommend=itemCF_IUF_Recommend(u,train,W) #求职者u的推荐集合
		count=R_Num*3-alreadyRecommendNum#推荐职位数
		for i,pui in sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True):
			if i in finallyRecommend[u]:#已推荐过
				continue
			if i not in JOB_OFFER:
				continue
			#规则过滤 性别不符、学历不符等
			if jobIfEffect(JWINFO[u],JOB_OFFER[i])==1:
				count-=1
				finallyRecommend[u][i]=pui
			if count==0:
				break

	return finallyRecommend
