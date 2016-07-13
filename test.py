#!usr/bin/env python
# -*- coding:utf-8 -*-
#test
from __future__ import division
from DB import *
from getData import *
import math
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#获取符合用户u的职位
def getJW_cando(u):

	JWINFO=getJWINFO(u)
	if 'Res_SN' not in JWINFO:
		return []
	sql="SELECT [Job_SN] \
	FROM [AnalysisData].[dbo].[JOB_OFFER] \
	where Job_Publish_Date between '%s' and '%s' \
	and ((Job_Workplace_Code/100=%s/100 or Job_Workplace_Code/100=%s/100 or Job_Workplace_Code/100=%s/100 ) or (%s=0 and %s=0 and %s=0 ) or \
		((Job_Workplace_Code%%10000=0 or %s%%10000=0) and (Job_Workplace_Code/10000=%s/10000) ) or \
		((Job_Workplace_Code%%10000=0 or %s%%10000=0) and (Job_Workplace_Code/10000=%s/10000) ) or \
		((Job_Workplace_Code%%10000=0 or %s%%10000=0) and (Job_Workplace_Code/10000=%s/10000) ) )\
	and ( (JobType=%s or JobType=%s or JobType=%s ) or (%s=0 and %s=0 and %s=0) or \
		((JobType%%1000=0 or %s%%1000=0) and (JobType/1000=%s/1000) ) or \
		((JobType%%1000=0 or %s%%1000=0) and (JobType/1000=%s/1000) ) or \
		((JobType%%1000=0 or %s%%1000=0) and (JobType/1000=%s/1000) ) )\
	and (Job_Money>=%s or %s=15) \
	and  (Job_Learn_Limited<=%s or %s=0) \
	and  (Job_Sex=%s or Job_Sex=0) \
	and  (Job_Kind='%s' or '%s'='0') \
	and  (Job_Agelowest<=%s or %s=-1) \
	and (Job_Agehighest=0 or Job_Agehighest>=%s) \
	and (Job_Expr_Years<=%s)"\
	% ('2014-4-01','2014-4-30',JWINFO['Res_Workcity1']\
		,JWINFO['Res_Workcity2'],JWINFO['Res_Workcity3']\
		,JWINFO['Res_Workcity1'],JWINFO['Res_Workcity2']\
		,JWINFO['Res_Workcity3'],JWINFO['Res_Workcity1']\
		,JWINFO['Res_Workcity1'],JWINFO['Res_Workcity2']\
		,JWINFO['Res_Workcity2'],JWINFO['Res_Workcity3']\
		,JWINFO['Res_Workcity3'],JWINFO['Res_JobType1']\
		,JWINFO['Res_JobType2'],JWINFO['Res_JobType3']\
		,JWINFO['Res_JobType1'],JWINFO['Res_JobType2']\
		,JWINFO['Res_JobType3'],JWINFO['Res_JobType1']\
		,JWINFO['Res_JobType1'],JWINFO['Res_JobType2']\
		,JWINFO['Res_JobType2'],JWINFO['Res_JobType3']\
		,JWINFO['Res_JobType3'],JWINFO['Res_Money']\
		,JWINFO['Res_Money'],JWINFO['Res_Learn']\
		,JWINFO['Res_Learn'],JWINFO['Res_Sex']\
		,JWINFO['Res_Jobkind'],JWINFO['Res_Jobkind']\
		,JWINFO['Age'],JWINFO['Age'],JWINFO['Age']\
		,JWINFO['Res_Expr_Years'])	
	result=DBQuery(sql)
	ilist=[ data[0] for data in result]
	return ilist
