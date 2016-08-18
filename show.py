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
def getJWINFO():

	lx_ICode_IName={}
	sql="SELECT [IName]\
      ,[ICode]\
      ,[lx]\
  FROM [dbo].[List_Down]"
	result=DBQuery(sql)
	for data in result:
		lx_ICode_IName.setdefault(data[2],{})
		lx_ICode_IName[data[2]][data[1]]=data[0]

	Jobtype={}
	sql="SELECT [name] \
	,[uid]\
 FROM [dbo].[Jobtype]"
 	result=DBQuery(sql)
	for data in result:
		Jobtype.setdefault(data[1],data[0])

	RESUME=dict()
	sql="SELECT * \
  FROM [dbo].[RESUME]"
	result=DBQuery(sql)
	for data in result:
		RESUME[data[15]]={}
		RESUME[data[15]]['Res_Publish_Date']=data[1]
		RESUME[data[15]]['Res_Edu_Trade']=data[2]
		RESUME[data[15]]['Res_Ability']=data[3]
		RESUME[data[15]]['Res_Dir']=data[4]
		RESUME[data[15]]['Res_Job_Want']=data[5]
		RESUME[data[15]]['Res_Self_Intro']=data[6]
		RESUME[data[15]]['Res_Money']=str(data[7])
		RESUME[data[15]]['Res_JobType1']=data[8]
		RESUME[data[15]]['Res_JobType2']=data[9]
		RESUME[data[15]]['Res_JobType3']=data[10]
		RESUME[data[15]]['Res_Jobkind']=data[11]
		RESUME[data[15]]['Res_Workcity1']=data[12]
		RESUME[data[15]]['Res_Workcity2']=data[13]
		RESUME[data[15]]['Res_Workcity3']=data[14]

	JWINFO=dict()
	sql="SELECT * \
	FROM [dbo].[JWINFO]"
	result=DBQuery(sql)
	for data in result:
		JWINFO[data[0]]={}
		JWINFO[data[0]]['Jw_Name']=data[1]
		JWINFO[data[0]]['Jw_Type']= u'社会人士' if data[2]==0 else u'应届毕业生'
		JWINFO[data[0]]['Jw_Action']=data[3]
		JWINFO[data[0]]['Jw_IndustryJob']=data[4]
		JWINFO[data[0]]['Res_Sex']=u'男' if data[5]==1 else u'女'
		JWINFO[data[0]]['Res_birthday']=data[6].strftime('%Y-%m-%d') if data[6] !=None else u'——'
		JWINFO[data[0]]['Age']=CalculateAge(data[6])
		JWINFO[data[0]]['Res_Height']=data[7]
		JWINFO[data[0]]['Res_Marry']= u'未婚' if data[8]==0 else u'已婚'
		JWINFO[data[0]]['Res_Learn']=str(data[9])
		JWINFO[data[0]]['Res_GSchool']=data[10]
		JWINFO[data[0]]['Res_Major']=data[11]
		JWINFO[data[0]]['Res_English']=data[12] if data[12]!=None else u'——'
		JWINFO[data[0]]['Res_Hukou']=data[13]
		JWINFO[data[0]]['Res_Livin']=data[14]
		JWINFO[data[0]]['Res_Comp_Ability']=data[15]
		JWINFO[data[0]]['Res_Expr_Years']=str(data[16]) if data[16]!=-1 else '0'
		JWINFO[data[0]]['Res_Has_Picture']=data[17]
		JWINFO[data[0]]['Res_SN']=data[18]
		JWINFO[data[0]]['Jw_CreditPoint']=data[19]

		if JWINFO[data[0]]['Res_Learn']=='0':
			JWINFO[data[0]]['Res_Learn']=u'无'
		else:
			JWINFO[data[0]]['Res_Learn']=lx_ICode_IName[15][ JWINFO[data[0]]['Res_Learn'] ]

		JWINFO[data[0]]['Res_Expr_Years']=lx_ICode_IName[14][ JWINFO[data[0]]['Res_Expr_Years'] ]

		if JWINFO[data[0]]['Res_SN']==0:
			JWINFO[data[0]]['Res_Publish_Date']=u'——'
			JWINFO[data[0]]['Res_Edu_Trade']=u'——'
			JWINFO[data[0]]['Res_Ability']=u'——'
			JWINFO[data[0]]['Res_Dir']=u'——'
			JWINFO[data[0]]['Res_Job_Want']=u'——'
			JWINFO[data[0]]['Res_Self_Intro']=u'——'
			JWINFO[data[0]]['Res_Money']=u'——'
			JWINFO[data[0]]['Res_JobType1']=u'——'
			JWINFO[data[0]]['Res_JobType2']=u'——'
			JWINFO[data[0]]['Res_JobType3']=u'——'
			JWINFO[data[0]]['Res_Jobkind']=u'——'
			JWINFO[data[0]]['Res_Workcity1']=u'——'
			JWINFO[data[0]]['Res_Workcity2']=u'——'
			JWINFO[data[0]]['Res_Workcity3']=u'——'
		else:
			JWINFO[data[0]]['Res_Publish_Date']=RESUME[ JWINFO[data[0]]['Res_SN'] ]['Res_Publish_Date']
			JWINFO[data[0]]['Res_Edu_Trade']=RESUME[JWINFO[data[0]]['Res_SN']]['Res_Edu_Trade']
			JWINFO[data[0]]['Res_Ability']=RESUME[JWINFO[data[0]]['Res_SN']]['Res_Ability']
			JWINFO[data[0]]['Res_Dir']=RESUME[JWINFO[data[0]]['Res_SN']]['Res_Dir']
			JWINFO[data[0]]['Res_Job_Want']=RESUME[JWINFO[data[0]]['Res_SN']]['Res_Job_Want']
			JWINFO[data[0]]['Res_Self_Intro']=RESUME[JWINFO[data[0]]['Res_SN']]['Res_Self_Intro']
			JWINFO[data[0]]['Res_Money']=RESUME[JWINFO[data[0]]['Res_SN']]['Res_Money']
			JWINFO[data[0]]['Res_JobType1']=RESUME[JWINFO[data[0]]['Res_SN']]['Res_JobType1']
			JWINFO[data[0]]['Res_JobType2']=RESUME[JWINFO[data[0]]['Res_SN']]['Res_JobType2']
			JWINFO[data[0]]['Res_JobType3']=RESUME[JWINFO[data[0]]['Res_SN']]['Res_JobType3']
			JWINFO[data[0]]['Res_Jobkind']=RESUME[JWINFO[data[0]]['Res_SN']]['Res_Jobkind']
			JWINFO[data[0]]['Res_Workcity1']=RESUME[JWINFO[data[0]]['Res_SN']]['Res_Workcity1']
			JWINFO[data[0]]['Res_Workcity2']=RESUME[JWINFO[data[0]]['Res_SN']]['Res_Workcity2']
			JWINFO[data[0]]['Res_Workcity3']=RESUME[JWINFO[data[0]]['Res_SN']]['Res_Workcity3']

			if JWINFO[data[0]]['Res_JobType1']!=0:
				JWINFO[data[0]]['Res_JobType1']=Jobtype[ JWINFO[data[0]]['Res_JobType1'] ]

			if JWINFO[data[0]]['Res_JobType2']!=0:
				JWINFO[data[0]]['Res_JobType2']=Jobtype[ JWINFO[data[0]]['Res_JobType2'] ]

			if JWINFO[data[0]]['Res_JobType3']!=0:
				JWINFO[data[0]]['Res_JobType3']=Jobtype[ JWINFO[data[0]]['Res_JobType3'] ]

			if JWINFO[data[0]]['Res_Money']=='0':
				JWINFO[data[0]]['Res_Money']=u'——'
			else:
				JWINFO[data[0]]['Res_Money']=lx_ICode_IName[6][ JWINFO[data[0]]['Res_Money'] ]

	return JWINFO

#获取职位信息
def getJOBINFO():

	lx_ICode_IName={}
	sql="SELECT [IName]\
      ,[ICode]\
      ,[lx]\
  FROM [dbo].[List_Down]"
	result=DBQuery(sql)
	for data in result:
		lx_ICode_IName.setdefault(data[2],{})
		lx_ICode_IName[data[2]][data[1]]=data[0]

	Jobtype={}
	sql="SELECT [name] \
	,[uid]\
 FROM [dbo].[Jobtype]"
 	result=DBQuery(sql)
	for data in result:
		Jobtype.setdefault(data[1],data[0])

	ENT_INFO={}
	sql="SELECT [Ent_SN]\
	  ,[Ent_Name] \
      ,[Ent_Industry] \
      ,[Ent_Property] \
	FROM [dbo].[ENT_INFO_FORM]"
	result=DBQuery(sql)
	for data in result:
		ENT_INFO[data[0]]=[data[1],data[2],data[3]]

	JOBINFO=dict()
	sql="SELECT * \
	FROM [dbo].[JOB_OFFER]"
	result=DBQuery(sql)
	for data in result:
		JOBINFO[data[0]]={}
		JOBINFO[data[0]]['Job_Name']=data[1]
		JOBINFO[data[0]]['Job_Publish_Date']=data[2].strftime('%Y-%m-%d')
		JOBINFO[data[0]]['Job_People_Count']=data[3]
		JOBINFO[data[0]]['Job_Workplace']=data[4]
		JOBINFO[data[0]]['Job_Requirement']=data[5]
		JOBINFO[data[0]]['Ent_SN']=data[6]
		JOBINFO[data[0]]['JobType']=data[7]
		JOBINFO[data[0]]['Job_Money']=str(data[8])
		JOBINFO[data[0]]['Job_Learn_Limited']=str(data[9])
		if data[10]==0:
			JOBINFO[data[0]]['Job_Sex']=u'不限'
		else:
			JOBINFO[data[0]]['Job_Sex']=u'男' if data[10]==1 else u'女'

		JOBINFO[data[0]]['Job_ProvideHouse']=data[11]
		JOBINFO[data[0]]['Job_Kind']=data[12]
		JOBINFO[data[0]]['Job_Agelowest']=data[13]
		JOBINFO[data[0]]['Job_Agehighest']=data[14]
		JOBINFO[data[0]]['Job_Expr_Years']=str(data[15])
		JOBINFO[data[0]]['Job_Workplace_Code']=data[16]
		JOBINFO[data[0]]['Job_Keyword']=data[17]
		JOBINFO[data[0]]['Resumepipei']=data[18]
		JOBINFO[data[0]]['BUSWAY']=data[19]
		JOBINFO[data[0]]['discuss']=data[20]
		JOBINFO[data[0]]['Job_Medals']=data[21]


		JOBINFO[data[0]]['Ent_Name']=ENT_INFO[JOBINFO[data[0]]['Ent_SN']][0]
		JOBINFO[data[0]]['Ent_Industry']=ENT_INFO[JOBINFO[data[0]]['Ent_SN']][1]
		JOBINFO[data[0]]['Ent_Property']=ENT_INFO[JOBINFO[data[0]]['Ent_SN']][2]

		JOBINFO[data[0]]['JobType']=Jobtype[JOBINFO[data[0]]['JobType']]

		if JOBINFO[data[0]]['Job_Money']=='0':
			JOBINFO[data[0]]['Job_Money']='面议'
		else:
			JOBINFO[data[0]]['Job_Money']=lx_ICode_IName[6][ JOBINFO[data[0]]['Job_Money'] ]

		JOBINFO[data[0]]['Job_Learn_Limited']=lx_ICode_IName[9][ JOBINFO[data[0]]['Job_Learn_Limited'] ]
		JOBINFO[data[0]]['Job_Expr_Years']=lx_ICode_IName[10][ JOBINFO[data[0]]['Job_Expr_Years'] ]

	return JOBINFO

#输出到html
def formatToHtml(fileName):
	JOBINFOS=getJOBINFO()
	JWINFOS=getJWINFO()
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
		JWINFO=JWINFOS[int(value[0])]
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
			JOBINFO=JOBINFOS[int(i)]
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
