#!usr/bin/env python
# -*- coding:utf-8 -*-
#主函数
from __future__ import division
from getData import getTrainData
from itemCF_IUF import itemCF_IUF_finallyRecommend
from userCF_IIF import userCF_IIF_finallyRecommend
import math
import operator
import time

if __name__ == '__main__':
	start = time.clock()

	#获取数据
	trainData=getTrainData()
	
	#itemCF_IUF推荐结果
	# itemCF_IUF_finallyRecommend=itemCF_IUF_finallyRecommend(trainData)
	# for u,u_recommend in itemCF_IUF_finallyRecommend.items():
	# 	if u_recommend!={}:
	# 		print u,sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True)
	
	#userCF_IIF推荐结果	
	# userCF_IIF_finallyRecommend=userCF_IIF_finallyRecommend(trainData)
	# for u,u_recommend in userCF_IIF_finallyRecommend.items():
	# 	if u_recommend!={}:
	# 		print u,sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True)
	
	end = time.clock()
	print u"耗时: %f s" % (end - start)