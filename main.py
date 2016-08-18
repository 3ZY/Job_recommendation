#!usr/bin/env python
# -*- coding:utf-8 -*-
#主函数
from __future__ import division
from getData import *
from userCF_IIF import userCF_IIF_finallyRecommend
from evaluate import *
from user_cold_start import *
from outData import *
import math
import operator
import time
import traceback
import ConfigParser

if __name__ == '__main__':

	conf = ConfigParser.ConfigParser()
	conf.read("conf.ini")

	outStr={'getData':u'——','evaluate':u'——','userCF_IIF':u'——', \
			'most_popular':u'——','CB_fill':u'——', \
			'outToDB':u'——','total':u'——','JW_QUERY_LOG':u'——',\
			'JWAPPLYJOB':u'——','JOB_FAV':u'——','RESUME':u'——',\
			'JWINFO':u'——','JOB_OFFER':u'——'}#日志输出部分
	errStr="none" #出错信息
	try:
		start = time.clock()
		nowtime,lastime=getTimes( int(conf.get('base','days')) )#前n天
		nowtime='2016-7-28'
		lastime='2016-6-1'
		R_Num=int(conf.get('base','R_Num')) #推荐职位数
		#获取数据
		Job_Rec=getJob_Rec()
		Job_SN=getAllJob_SN(nowtime,lastime)#时间段内所有职位
		# Jw_SN=getAllJw_SN()#获得所有求职者
		JWINFO,JOB_OFFER=getJWJOBINFO(nowtime,lastime,outStr)#获得求职者信息及职位信息
		Ni=getNi(nowtime,lastime)
		trainData=getTrainData(nowtime,lastime,outStr)#行为数据
		Jw_SN=set(JWINFO.keys())

		getData_time=time.clock()
		outStr['getData']=u"耗时: %f s" % (getData_time - start)
		print u"getData耗时: %f s" % (getData_time - start)

		#生成评估表
		evaluate(Job_Rec,conf.get('base','outScoreToFile'))
		evaluate_time=time.clock()
		outStr['evaluate']=u"耗时: %f s" % (evaluate_time - getData_time)
		print u"evaluate耗时: %f s" % (evaluate_time - getData_time)
		del Job_Rec#历史推荐数据释放

		#userCF_IIF推荐
		finallyRecommend=userCF_IIF_finallyRecommend(trainData,JWINFO,JOB_OFFER,R_Num,conf.get('base','K'))
		userCF_IIF_time=time.clock()
		outStr['userCF_IIF']=u"耗时: %f s" % (userCF_IIF_time - evaluate_time)
		print u"userCF_IIF耗时: %f s" % (userCF_IIF_time - evaluate_time)

		#most_popular推荐
		finallyRecommend=most_popular_finallyRecommend(trainData,Jw_SN,nowtime,lastime,JWINFO,JOB_OFFER,Ni,R_Num,finallyRecommend)
		most_popular_time=time.clock()
		outStr['most_popular']=u"耗时: %f s" % (most_popular_time - userCF_IIF_time)
		print u"most_popular耗时: %f s" % (most_popular_time - userCF_IIF_time)

		del trainData#训练数据释放

		#CB_fill推荐
		finallyRecommend=CB_fill_finallyRecommend(Jw_SN,Job_SN,nowtime,lastime,JWINFO,JOB_OFFER,Ni,R_Num,finallyRecommend)
		CB_fill_time=time.clock()
		outStr['CB_fill']=u"耗时: %f s" % (CB_fill_time - most_popular_time)
		print u"CB_fill耗时: %f s" % (CB_fill_time - most_popular_time)

		if conf.get('base','outToFile')=="y":
			#结果输出到文件
			outToFile('finallyRecommend.csv',finallyRecommend)

		#结果输出到数据库
		outToDB(finallyRecommend)
		outToDB_time=time.clock()
		outStr['outToDB']=u"耗时: %f s" % (outToDB_time - CB_fill_time)
		print u"outToDB耗时: %f s" % (outToDB_time - CB_fill_time)

		end = time.clock()
		outStr['total']=u"耗时: %f s" % (end - start)
		print u"耗时: %f s" % (end - start)

	except:
		errStr=traceback.format_exc()
		print errStr

	log_out(time.strftime("%Y-%m-%d %H:%M:%S"),errStr,outStr)
	# for key,value in outStr.items():
	# 	print key,value
