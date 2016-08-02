#!usr/bin/env python
# -*- coding:utf-8 -*-
#数据库操作
import pymssql

def DBQuery(sql):
	#连接
	host='127.0.0.1'
	port='1433'
	user='sa'
	password='1122334455'
	database='AnalysisData'
	conn=pymssql.connect(host=host,port=port,user=user,password=password,database=database)
	#获取游标对象
	cur=conn.cursor()

	#查询
	cur.execute(sql)
	result=cur.fetchall()

	#关闭连接
	conn.close()

	return result