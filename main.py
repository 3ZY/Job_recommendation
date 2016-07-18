#!usr/bin/env python
# -*- coding:utf-8 -*-
#主函数
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
	nowtime='2014-5-1'
	lastmonth='2014-4-1'	
	R_Num=8 #推荐职位数
	#获取数据
	allJob_SN=getAllJob_SN(nowtime,lastmonth)#时间段内所有职位
	Jw_SN=getAllJw_SN()
	trainData=getTrainData(nowtime,lastmonth)
	
	#userCF_IIF推荐
	finallyRecommend=userCF_IIF_finallyRecommend(trainData,nowtime,lastmonth,R_Num)

	#itemCF_IUF推荐
	finallyRecommend=itemCF_IUF_finallyRecommend(trainData,nowtime,lastmonth,R_Num,finallyRecommend)

	#city_type_most_popular推荐
	finallyRecommend=city_type_most_popular_finallyRecommend(Jw_SN,nowtime,lastmonth,R_Num,finallyRecommend)

	#most_popular推荐
	finallyRecommend=most_popular_finallyRecommend(Jw_SN,nowtime,lastmonth,R_Num,finallyRecommend)

	#noal推荐
	finallyRecommend=noal_finallyRecommend(Jw_SN,nowtime,lastmonth,R_Num,finallyRecommend)
	
	# for u,u_recommend in finallyRecommend.items():
	# 	print u,sorted(u_recommend.items(),key=operator.itemgetter(1),reverse=True)
	
	#结果输出到文件
	outToFile('finallyRecommend.csv',finallyRecommend)
	
	end = time.clock()
	print u"耗时: %f s" % (end - start)
	
	#html显示结果
	#formatToHtml('finallyRecommend.csv')