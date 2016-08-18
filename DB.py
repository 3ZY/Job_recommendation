#!usr/bin/env python
# -*- coding:utf-8 -*-
#数据库操作
import pymssql
import ConfigParser

conf = ConfigParser.ConfigParser()
conf.read("conf.ini")
host = conf.get('db','host')
port = conf.get('db','port')
user = conf.get('db','user')
password = conf.get('db','password')
database = conf.get('db','database')

def DBQuery(sql):

	#连接
	conn=pymssql.connect(host=host,port=port,user=user,password=password,database=database)
	#获取游标对象
	cur=conn.cursor()
	#查询
	cur.execute(sql)
	result=cur.fetchall()
	cur.close()
	conn.close()
	return result


def DBInsert(sql):

	conn=pymssql.connect(host=host,port=port,user=user,password=password,database=database)
	cur=conn.cursor()
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
