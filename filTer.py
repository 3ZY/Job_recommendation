#!usr/bin/env python
# -*- coding:utf-8 -*-
#过滤器

#职位是否有效
def jobIfEffect(JWINFO,JOB_OFFER):
	
	#数据不完整,缺失数据
	if 'Job_effect' not in JOB_OFFER:
		return 0
	if 'Res_SN' not in JWINFO:
		return 0

	#有效期 先当做全在有效期
	if JOB_OFFER['Job_effect']==0:
		pass
		#return 0

	#职位类型
	if  JOB_OFFER['JobType']!=JWINFO['Res_JobType1'] and\
		JOB_OFFER['JobType']!=JWINFO['Res_JobType2'] and\
		JOB_OFFER['JobType']!=JWINFO['Res_JobType3'] and\
		not(JWINFO['Res_JobType3']==0 and JWINFO['Res_JobType2']==0 and JWINFO['Res_JobType1']==0) and\
		not( (JOB_OFFER['JobType']%1000==0 or JWINFO['Res_JobType1']%1000==0) and int(JOB_OFFER['JobType']/1000)==int(JWINFO['Res_JobType1']/1000) ) and\
		not( (JOB_OFFER['JobType']%1000==0 or JWINFO['Res_JobType2']%1000==0) and int(JOB_OFFER['JobType']/1000)==int(JWINFO['Res_JobType2']/1000) ) and\
		not( (JOB_OFFER['JobType']%1000==0 or JWINFO['Res_JobType3']%1000==0) and int(JOB_OFFER['JobType']/1000)==int(JWINFO['Res_JobType3']/1000) ):
		return 0

	#工资要求
	if JOB_OFFER['Job_Money']<JWINFO['Res_Money'] and JWINFO['Res_Money']!=15:
		return 0

	#学历限制
	if JOB_OFFER['Job_Learn_Limited']>JWINFO['Res_Learn'] and JWINFO['Res_Learn']!=0:
		return 0

	#性别限制
	if JOB_OFFER['Job_Sex']!=JWINFO['Res_Sex'] and JOB_OFFER['Job_Sex']!=0:
		return 0

	#职位类型
	if JOB_OFFER['Job_Kind']!=JWINFO['Res_Jobkind'] and JWINFO['Res_Jobkind']!=0:
		return 0

	#年龄要求
	if JOB_OFFER['Job_Agelowest']>JWINFO['Age'] and JWINFO['Age']!=-1:
		return 0
	if JOB_OFFER['Job_Agehighest']!=0 and JOB_OFFER['Job_Agehighest']<JWINFO['Age']:
		return 0

	#工作经验
	if JOB_OFFER['Job_Expr_Years']>JWINFO['Res_Expr_Years']:
		return 0

	#工作城市 数据库代码不清楚，目前不能判断
	if JOB_OFFER['Job_Workplace_Code']==0:
		pass

	return 1