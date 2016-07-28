#!usr/bin/env python
# -*- coding:utf-8 -*-
#过滤器


#职位是否有效
def jobIfEffect(JWINFO,JOB_OFFER):

	#数据不完整,缺失数据
	# if 'JobType' not in JOB_OFFER:
	# 	return 0
	# if 'Res_SN' not in JWINFO:
	# 	return 0

	#数据库未设有效期
	# if JOB_OFFER['Job_effect']==0:
	# 	pass
	# 	#return 0

	#职位类型
	if  ((JOB_OFFER['JobType']==JWINFO['Res_JobType1'] or \
		JOB_OFFER['JobType']==JWINFO['Res_JobType2'] or \
		JOB_OFFER['JobType']==JWINFO['Res_JobType3']) or \
		(JWINFO['Res_JobType3']==0 and JWINFO['Res_JobType2']==0 and JWINFO['Res_JobType1']==0) or \
		( (JOB_OFFER['JobType']%1000==0 or JWINFO['Res_JobType1']%1000==0) and int(JOB_OFFER['JobType']/1000)==int(JWINFO['Res_JobType1']/1000) ) or \
		( (JOB_OFFER['JobType']%1000==0 or JWINFO['Res_JobType2']%1000==0) and int(JOB_OFFER['JobType']/1000)==int(JWINFO['Res_JobType2']/1000) ) or \
		( (JOB_OFFER['JobType']%1000==0 or JWINFO['Res_JobType3']%1000==0) and int(JOB_OFFER['JobType']/1000)==int(JWINFO['Res_JobType3']/1000) ) )==0:
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

	#工作城市
	if ((JOB_OFFER['Job_Workplace_Code']/100==JWINFO['Res_Workcity1']/100 or \
		JOB_OFFER['Job_Workplace_Code']/100==JWINFO['Res_Workcity2']/100 or \
		JOB_OFFER['Job_Workplace_Code']/100==JWINFO['Res_Workcity3']/100 ) or \
		( JWINFO['Res_Workcity1']==0 and JWINFO['Res_Workcity2']==0 and JWINFO['Res_Workcity3']==0 ) or \
		((JOB_OFFER['Job_Workplace_Code']%10000==0 or JWINFO['Res_Workcity1']%10000==0) and (JOB_OFFER['Job_Workplace_Code']/10000==JWINFO['Res_Workcity1']/10000) ) or \
		((JOB_OFFER['Job_Workplace_Code']%10000==0 or JWINFO['Res_Workcity2']%10000==0) and (JOB_OFFER['Job_Workplace_Code']/10000==JWINFO['Res_Workcity2']/10000) ) or \
		((JOB_OFFER['Job_Workplace_Code']%10000==0 or JWINFO['Res_Workcity3']%10000==0) and (JOB_OFFER['Job_Workplace_Code']/10000==JWINFO['Res_Workcity3']/10000) ) )==0:
		return 0

	return 1

#是否符合期望工作地点及工作类型特征
def city_tpye_IfEffect(JWINFO,JOB_OFFER):

	#数据库未设有效期
	# if JOB_OFFER['Job_effect']==0:
	# 	pass
	# 	#return 0

	#性别限制
	if JOB_OFFER['Job_Sex']!=JWINFO['Res_Sex'] and JOB_OFFER['Job_Sex']!=0:
		return 0

	#职位类型
	if  ((JOB_OFFER['JobType']==JWINFO['Res_JobType1'] or \
		JOB_OFFER['JobType']==JWINFO['Res_JobType2'] or \
		JOB_OFFER['JobType']==JWINFO['Res_JobType3']) or \
		(JWINFO['Res_JobType3']==0 and JWINFO['Res_JobType2']==0 and JWINFO['Res_JobType1']==0) or \
		( (JOB_OFFER['JobType']%1000==0 or JWINFO['Res_JobType1']%1000==0) and int(JOB_OFFER['JobType']/1000)==int(JWINFO['Res_JobType1']/1000) ) or \
		( (JOB_OFFER['JobType']%1000==0 or JWINFO['Res_JobType2']%1000==0) and int(JOB_OFFER['JobType']/1000)==int(JWINFO['Res_JobType2']/1000) ) or \
		( (JOB_OFFER['JobType']%1000==0 or JWINFO['Res_JobType3']%1000==0) and int(JOB_OFFER['JobType']/1000)==int(JWINFO['Res_JobType3']/1000) ) )==0:
		return 0

	#工作城市
	if ((JOB_OFFER['Job_Workplace_Code']/100==JWINFO['Res_Workcity1']/100 or \
		JOB_OFFER['Job_Workplace_Code']/100==JWINFO['Res_Workcity2']/100 or \
		JOB_OFFER['Job_Workplace_Code']/100==JWINFO['Res_Workcity3']/100 ) or \
		( JWINFO['Res_Workcity1']==0 and JWINFO['Res_Workcity2']==0 and JWINFO['Res_Workcity3']==0 ) or \
		((JOB_OFFER['Job_Workplace_Code']%10000==0 or JWINFO['Res_Workcity1']%10000==0) and (JOB_OFFER['Job_Workplace_Code']/10000==JWINFO['Res_Workcity1']/10000) ) or \
		((JOB_OFFER['Job_Workplace_Code']%10000==0 or JWINFO['Res_Workcity2']%10000==0) and (JOB_OFFER['Job_Workplace_Code']/10000==JWINFO['Res_Workcity2']/10000) ) or \
		((JOB_OFFER['Job_Workplace_Code']%10000==0 or JWINFO['Res_Workcity3']%10000==0) and (JOB_OFFER['Job_Workplace_Code']/10000==JWINFO['Res_Workcity3']/10000) ) )==0:
		return 0

	return 1

def sex_city_IfEffect(JWINFO,JOB_OFFER):

	#数据库未设有效期
	# if JOB_OFFER['Job_effect']==0:
	# 	#return 0

	#性别限制
	if JOB_OFFER['Job_Sex']!=JWINFO['Res_Sex'] and JOB_OFFER['Job_Sex']!=0:
		return 0

	#工作城市
	if ((JOB_OFFER['Job_Workplace_Code']/100==JWINFO['Res_Workcity1']/100 or \
		JOB_OFFER['Job_Workplace_Code']/100==JWINFO['Res_Workcity2']/100 or \
		JOB_OFFER['Job_Workplace_Code']/100==JWINFO['Res_Workcity3']/100 ) or \
		( JWINFO['Res_Workcity1']==0 and JWINFO['Res_Workcity2']==0 and JWINFO['Res_Workcity3']==0 ) or \
		((JOB_OFFER['Job_Workplace_Code']%10000==0 or JWINFO['Res_Workcity1']%10000==0) and (JOB_OFFER['Job_Workplace_Code']/10000==JWINFO['Res_Workcity1']/10000) ) or \
		((JOB_OFFER['Job_Workplace_Code']%10000==0 or JWINFO['Res_Workcity2']%10000==0) and (JOB_OFFER['Job_Workplace_Code']/10000==JWINFO['Res_Workcity2']/10000) ) or \
		((JOB_OFFER['Job_Workplace_Code']%10000==0 or JWINFO['Res_Workcity3']%10000==0) and (JOB_OFFER['Job_Workplace_Code']/10000==JWINFO['Res_Workcity3']/10000) ) )==0:
		return 0

	return 1
