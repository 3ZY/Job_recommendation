#!usr/bin/env python
# -*- coding:utf-8 -*-
#test
from __future__ import division
from DB import *
from filTer import *
from getData import *
import math



sql="SELECT [Jw_Type]\
		,[Res_Sex]\
		,[Res_birthday]\
		,[Res_Learn]\
		,[Res_Expr_Years]\
		,[Res_SN]\
		from [AnalysisData].[dbo].[JWINFO]\
		where [Jw_SN]=2"
result=DBQuery(sql)
	
