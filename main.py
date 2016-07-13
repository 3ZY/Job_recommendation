#!usr/bin/env python
# -*- coding:utf-8 -*-
#主函数
from __future__ import division
from getData import getTrainData
from itemCF_IUF import itemCF_IUF_finallyRecommend
from userCF_IIF import userCF_IIF_finallyRecommend
from user_cold_start import *
import math
import operator
import time

if __name__ == '__main__':
	start = time.clock()
	nowtime,lastmonth=getTimes()
	nowtime='2014-5-1'
	lastmonth='2014-4-1'	

	#获取数据
	allJob_SN=getAllJob_SN(nowtime,lastmonth)#时间段内所有职位
	Jw_SN=getAllJw_SN()
	trainData=getTrainData(nowtime,lastmonth)
	
	#itemCF_IUF推荐结果
	# itemCF_IUF_finallyRecommend=itemCF_IUF_finallyRecommend(trainData,nowtime,lastmonth)
	# for u,u_recommend in itemCF_IUF_finallyRecommend.items():
	# 	if u_recommend!={}:
	# 		print u,sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True)
	
	#userCF_IIF推荐结果	
	# userCF_IIF_finallyRecommend=userCF_IIF_finallyRecommend(trainData,nowtime,lastmonth)
	# for u,u_recommend in userCF_IIF_finallyRecommend.items():
	# 	if u_recommend!={}:
	# 		print u,sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True)
	
	#city_type_most_popular推荐结果
	#city_type_most_popular_finallyRecommend=city_type_most_popular_finallyRecommend(Jw_SN,nowtime,lastmonth)
	# for u,u_recommend in city_type_most_popular_finallyRecommend.items():
	# 	if u_recommend!={}:
	# 		print u,sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True)

	#most_popular推荐结果
	#most_popular_finallyRecommend=most_popular_finallyRecommend(Jw_SN,nowtime,lastmonth)
	# for u,u_recommend in most_popular_finallyRecommend.items():
	# 	if u_recommend!={}:
	# 		print u,sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True)

	#noal推荐结果
	#noal_finallyRecommend=noal_finallyRecommend(Jw_SN,nowtime,lastmonth)
	# for u,u_recommend in noal_finallyRecommend.items():
	# 	if u_recommend!={}:
	# 		print u,sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True)

	end = time.clock()
	print u"耗时: %f s" % (end - start)