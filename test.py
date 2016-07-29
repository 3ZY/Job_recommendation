#!usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import division
from getData import getTrainData
from itemCF_IUF import itemCF_IUF_finallyRecommend
from userCF_IIF import userCF_IIF_finallyRecommend
from user_cold_start import *
from show import formatToHtml
import math
import operator
import time

def outToFile(fileName,recommend):
	path='result/'
	outFile=open(path+fileName,'w')
	outFile.write('Jw_SN,Job_SN...\n')
	for u,u_recommend in recommend.items():
		if u_recommend!={}:
			outFile.write(str(u))
			for i,p in sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True):
				outFile.write(','+str(i))
			outFile.write("\n")

if __name__ == '__main__':
	start = time.clock()
	nowtime,lastmonth=getTimes()
	nowtime='2016-7-28'
	lastmonth='2016-6-1'
	R_Num=8 #推荐职位数
	Job_SN=getAllJob_SN(nowtime,lastmonth)#时间段内所有职位
	Jw_SN=getAllJw_SN()#获得所有求职者
	JWINFO,JOB_OFFER=getJWJOBINFO(nowtime,lastmonth)#获得求职者信息及职位信息
	trainData=getTrainData(nowtime,lastmonth)


	# #userCF_IIF推荐
	# finallyRecommend=userCF_IIF_finallyRecommend(trainData,JWINFO,JOB_OFFER,R_Num)
	# outToFile('userCF_IIF_Recommend.csv',finallyRecommend)
	#
	# #itemCF_IUF推荐
	# finallyRecommend=itemCF_IUF_finallyRecommend(trainData,JWINFO,JOB_OFFER,R_Num)
	# outToFile('itemCF_IUF_Recommend.csv',finallyRecommend)

	# #most_popular推荐
	# finallyRecommend=most_popular_finallyRecommend(Jw_SN,nowtime,lastmonth,JWINFO,JOB_OFFER,R_Num)
	# outToFile('most_popular_Recommend.csv',finallyRecommend)

	#CB_fill推荐
	# finallyRecommend=CB_fill_finallyRecommend(Jw_SN,Job_SN,nowtime,lastmonth,JWINFO,JOB_OFFER,R_Num)
	# outToFile('CB_fill_Recommend.csv',finallyRecommend)

	formatToHtml('finallyRecommend.csv')

	end = time.clock()
	print u"耗时: %f s" % (end - start)

	#####
