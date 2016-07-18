#!usr/bin/env python
# -*- coding:utf-8 -*-
#简单可视化
from DB import *
import datetime
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#计算年龄
def CalculateAge(Birthday):
	if Birthday==None:#未填出生日期
		return -1
	Today=datetime.date.today()
	if (Today.month>Birthday.month):
		return Today.year-Birthday.year
	elif (Today.month<Birthday.month):
		return Today.year-Birthday.year-1
	else:
		if (Today.day>=Birthday.day):
			return Today.year-Birthday.year
		else:
			return Today.year-Birthday.year-1

#获得求职者信息
def getJWINFO(u):
	
	JWINFO=dict()

	sql="SELECT * \
	FROM [AnalysisData].[dbo].[JWINFO]  \
	where Jw_SN='%s'" % (u)
	result=DBQuery(sql)
	data=result[0]

	JWINFO['Jw_SN']=data[0]
	JWINFO['Jw_Name']=data[1]
	JWINFO['Jw_Type']= u'社会人士' if data[2]==0 else u'应届毕业生'
	JWINFO['Jw_Action']=data[3]
	JWINFO['Jw_IndustryJob']=data[4]
	JWINFO['Res_Sex']=u'男' if data[5]==1 else u'女'
	JWINFO['Res_birthday']=data[6].strftime('%Y-%m-%d')
	JWINFO['Age']=CalculateAge(data[6])
	JWINFO['Res_Height']=data[7]
	JWINFO['Res_Marry']= u'未婚' if data[8]==0 else u'已婚'
	JWINFO['Res_Learn']=data[9]
	JWINFO['Res_GSchool']=data[10]
	JWINFO['Res_Major']=data[11]
	JWINFO['Res_English']=data[12] if data[12]!=None else u'——'
	JWINFO['Res_Hukou']=data[13]
	JWINFO['Res_Livin']=data[14]
	JWINFO['Res_Comp_Ability']=data[15]
	JWINFO['Res_Expr_Years']=data[16]
	JWINFO['Res_Has_Picture']=data[17]
	JWINFO['Res_SN']=data[18]
	JWINFO['Jw_CreditPoint']=data[19]

	sql="SELECT [IName]     \
  FROM [AnalysisData].[dbo].[List_Down] \
  where ICode='%s' and lx='15'" % (JWINFO['Res_Learn'])
	result=DBQuery(sql)
	data=result[0]
	JWINFO['Res_Learn']=data[0]

	sql="SELECT [IName]     \
  FROM [AnalysisData].[dbo].[List_Down] \
  where ICode='%s' and lx='14'" % (JWINFO['Res_Expr_Years'])
	result=DBQuery(sql)
	data=result[0]
	JWINFO['Res_Expr_Years']=data[0]

	if JWINFO['Res_SN']==0:
		JWINFO['Res_Publish_Date']=u'——'
		JWINFO['Res_Edu_Trade']=u'——'
		JWINFO['Res_Ability']=u'——'
		JWINFO['Res_Dir']=u'——'
		JWINFO['Res_Job_Want']=u'——'
		JWINFO['Res_Self_Intro']=u'——'
		JWINFO['Res_Money']=u'——'
		JWINFO['Res_JobType1']=u'——'
		JWINFO['Res_JobType2']=u'——'
		JWINFO['Res_JobType3']=u'——'
		JWINFO['Res_Jobkind']=u'——'
		JWINFO['Res_Workcity1']=u'——'
		JWINFO['Res_Workcity2']=u'——'
		JWINFO['Res_Workcity3']=u'——'
		
	sql="SELECT * \
  FROM [AnalysisData].[dbo].[RESUME] \
  where res_sn='%s'" % (JWINFO['Res_SN'])
	result=DBQuery(sql)
	data=result[0]
	JWINFO['Res_Publish_Date']=data[1]
	JWINFO['Res_Edu_Trade']=data[2]
	JWINFO['Res_Ability']=data[3]
	JWINFO['Res_Dir']=data[4]
	JWINFO['Res_Job_Want']=data[5]
	JWINFO['Res_Self_Intro']=data[6]
	JWINFO['Res_Money']=data[7]
	JWINFO['Res_JobType1']=data[8]
	JWINFO['Res_JobType2']=data[9]
	JWINFO['Res_JobType3']=data[10]
	JWINFO['Res_Jobkind']=data[11]
	JWINFO['Res_Workcity1']=data[12]
	JWINFO['Res_Workcity2']=data[13]
	JWINFO['Res_Workcity3']=data[14]

	if JWINFO['Res_JobType1']!=0:
		sql="SELECT [name] \
	 FROM [AnalysisData].[dbo].[Jobtype] \
	 where [uid]='%s'" % (JWINFO['Res_JobType1'])
		result=DBQuery(sql)
		data=result[0]
		JWINFO['Res_JobType1']=data[0]

	if JWINFO['Res_JobType2']!=0:
		sql="SELECT [name] \
	 FROM [AnalysisData].[dbo].[Jobtype] \
	 where [uid]='%s'" % (JWINFO['Res_JobType2'])
		result=DBQuery(sql)
		data=result[0]
		JWINFO['Res_JobType2']=data[0]

	if JWINFO['Res_JobType3']!=0:
		sql="SELECT [name] \
	 FROM [AnalysisData].[dbo].[Jobtype] \
	 where [uid]='%s'" % (JWINFO['Res_JobType3'])
		result=DBQuery(sql)
		data=result[0]
		JWINFO['Res_JobType3']=data[0]
	
	sql="SELECT [IName]    \
	FROM [AnalysisData].[dbo].[List_Down] \
	where ICode='%s' and lx='6'" % (JWINFO['Res_Money'])
	result=DBQuery(sql)
	data=result[0]
	JWINFO['Res_Money']=data[0]

	return JWINFO

#获取职位信息
def getJOBINFO(i):
	JOBINFO=dict()
	
	sql="SELECT * \
	FROM [AnalysisData].[dbo].[JOB_OFFER] \
	where Job_SN='%s'" %(i)
	result=DBQuery(sql)
	data=result[0]

	JOBINFO['Job_SN']=data[0]
	JOBINFO['Job_Name']=data[1]
	JOBINFO['Job_Publish_Date']=data[2].strftime('%Y-%m-%d')
	JOBINFO['Job_People_Count']=data[3]
	JOBINFO['Job_Workplace']=data[4]
	JOBINFO['Job_Requirement']=data[5]
	JOBINFO['Ent_SN']=data[6]
	JOBINFO['JobType']=data[7]
	JOBINFO['Job_Money']=data[8]
	JOBINFO['Job_Learn_Limited']=data[9]
	if data[10]==0:
		JOBINFO['Job_Sex']=u'不限'
	else:
		JOBINFO['Job_Sex']=u'男' if data[10]==1 else u'女'

	JOBINFO['Job_ProvideHouse']=data[11]
	JOBINFO['Job_Kind']=data[12]
	JOBINFO['Job_Agelowest']=data[13]
	JOBINFO['Job_Agehighest']=data[14]
	JOBINFO['Job_Expr_Years']=data[15]
	JOBINFO['Job_Workplace_Code']=data[16]
	JOBINFO['Job_Keyword']=data[17]
	JOBINFO['Resumepipei']=data[18]
	JOBINFO['BUSWAY']=data[19]
	JOBINFO['discuss']=data[20]
	JOBINFO['Job_Medals']=data[21]

	sql="SELECT [Ent_Name] \
      ,[Ent_Industry] \
      ,[Ent_Property] \
	FROM [AnalysisData].[dbo].[ENT_INFO_FORM] \
	where Ent_SN='%s'" % (JOBINFO['Ent_SN'])
	result=DBQuery(sql)
	data=result[0]
	JOBINFO['Ent_Name']=data[0]
	JOBINFO['Ent_Industry']=data[1]
	JOBINFO['Ent_Property']=data[2]

	sql="SELECT [name] \
	 FROM [AnalysisData].[dbo].[Jobtype] \
	 where [uid]='%s'" % (JOBINFO['JobType'])
	result=DBQuery(sql)
	data=result[0]
	JOBINFO['JobType']=data[0]

	sql="SELECT [IName]    \
	FROM [AnalysisData].[dbo].[List_Down] \
	where ICode='%s' and lx='6'" % (JOBINFO['Job_Money'])
	result=DBQuery(sql)
	data=result[0]
	JOBINFO['Job_Money']=data[0]

	sql="SELECT [IName]    \
	FROM [AnalysisData].[dbo].[List_Down] \
	where ICode='%s' and lx='9'" % (JOBINFO['Job_Learn_Limited'])
	result=DBQuery(sql)
	data=result[0]
	JOBINFO['Job_Learn_Limited']=data[0]

	sql="SELECT [IName]     \
	FROM [AnalysisData].[dbo].[List_Down] \
	where ICode='%s' and lx='10'" % (JOBINFO['Job_Expr_Years'])
	result=DBQuery(sql)
	data=result[0]
	JOBINFO['Job_Expr_Years']=data[0]

	return JOBINFO

#输出到html
def formatToHtml(fileName):
	inPath="result/"
	outPath="show/"
	inFile=open(inPath+fileName,'r')
	inFile.readline()
	for line in inFile.readlines():
		content="<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>\
		<html xmlns='http://www.w3.org/1999/xhtml'>\
	    <head>\
	        <meta http-equiv='Content-Type' content='text/html; charset=utf-8' />\
	        <title>example</title>\
	    </head>\
	    <body>\
	    <div style='margin-left:20px'>"
		value=line[:-1].split(',')
		outFile=open(outPath+str(value[0])+'.html','w')
		JWINFO=getJWINFO(value[0])
		content+="<h3>基本资料</h3>\
	    	<table border='1px' cellspacing='0' width='600' >\
	    		<tr height='30'>\
	    			<td>&nbsp;姓&nbsp;&nbsp;名：%s</td>\
	    			<td>&nbsp;性&nbsp;&nbsp;别：%s</td>\
	    		</tr>\
	    		<tr height='30'>\
	    			<td>&nbsp;年&nbsp;&nbsp;龄：%s</td>\
	    			<td>&nbsp;身&nbsp;&nbsp;高：%scm</td>\
	    		</tr>\
	    		<tr height='30'>\
	    			<td>&nbsp;学&nbsp;&nbsp;历：%s</td>\
	    			<td>&nbsp;类&nbsp;&nbsp;型：%s</td>\
	    		</tr>\
	    		<tr height='30'>\
	    			<td>&nbsp;院&nbsp;&nbsp;校：%s</td>\
	    			<td>&nbsp;专&nbsp;&nbsp;业：%s</td>\
	    		</tr>\
	    		<tr height='30'>\
	    			<td>&nbsp;期望待遇：%s</td>\
	    			<td>&nbsp;期望工作：%s,%s,%s</td>\
	    		</tr>\
	    		<tr height='30'>\
	    			<td>&nbsp;英语水平：%s</td>\
	    			<td>&nbsp;期望地点：%s,%s,%s</td>\
	    		</tr>\
	    		<tr height='30'>\
	    			<td>&nbsp;求职类型：%s</td>\
	    			<td>&nbsp;工作经验：%s</td>\
	    		</tr>	\
	    	</table>\
	    	<h3>技能</h3>\
		    	<span>\
		    		%s\
		    	</span>\
	    	<h3>自我介绍</h3>\
	    		<span>\
	    			%s\
	    		</span>\
	    	<h3>-------------------</h3>" \
			% (JWINFO['Jw_Name'],JWINFO['Res_Sex'],JWINFO['Age']\
				,JWINFO['Res_Height'],JWINFO['Res_Learn'],JWINFO['Jw_Type']\
				,JWINFO['Res_GSchool'],JWINFO['Res_Major'],JWINFO['Res_Money']\
				,JWINFO['Res_JobType1'],JWINFO['Res_JobType2'],JWINFO['Res_JobType3']\
				,JWINFO['Res_English'],JWINFO['Res_Workcity1'],JWINFO['Res_Workcity2']\
				,JWINFO['Res_Workcity3'],JWINFO['Res_Jobkind'],JWINFO['Res_Expr_Years']\
				,JWINFO['Res_Ability'],JWINFO['Res_Self_Intro'])
		for i in value[1:]:
			JOBINFO=getJOBINFO(i)
			content+="<h3>推荐职位</h3>\
			<table border='1px' cellspacing='0' width='600' >\
	    		<tr height='30'>\
	    			<td>&nbsp;公&nbsp;&nbsp;司：%s</td>\
	    			<td>&nbsp;性&nbsp;&nbsp;质：%s</td>\
	    		</tr>\
	    		<tr height='30'>\
	    			<td>&nbsp;职位名称：%s</td>\
	    			<td>&nbsp;职位类型：%s</td>\
	    		</tr>\
	    		<tr height='30'>\
	    			<td>&nbsp;提供待遇：%s</td>\
	    			<td>&nbsp;年龄限制：%s-%s</td>\
	    		</tr>\
	    		<tr height='30'>\
	    			<td>&nbsp;工作类型：%s</td>\
	    			<td>&nbsp;工作经验：%s</td>\
	    		</tr>\
	    		<tr height='30'>\
	    			<td>&nbsp;性别限制：%s</td>\
	    			<td>&nbsp;学历限制：%s</td>\
	    		</tr>\
	    		<tr height='30'>\
	    			<td>&nbsp;工作地点：%s</td>\
	    			<td>&nbsp;发布时间：%s</td>\
	    		</tr>\
	    	</table>\
			<h3>职位要求</h3>\
		    	<span>\
		    		%s\
		    	</span>\
		    <h3>-------------------</h3>"\
			% (JOBINFO['Ent_Name'],JOBINFO['Ent_Property'],JOBINFO['Job_Name']\
				,JOBINFO['JobType'],JOBINFO['Job_Money'],JOBINFO['Job_Agelowest']\
				,JOBINFO['Job_Agehighest'],JOBINFO['Job_Kind'],JOBINFO['Job_Expr_Years']\
				,JOBINFO['Job_Sex'],JOBINFO['Job_Learn_Limited']\
				,JOBINFO['Job_Workplace'],JOBINFO['Job_Publish_Date']\
				,JOBINFO['Job_Requirement'])
		outFile.write(content)
