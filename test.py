#!usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import division
from getData import *
from itemCF_IUF import itemCF_IUF_finallyRecommend
from userCF_IIF import userCF_IIF_finallyRecommend
from user_cold_start import *
from show import formatToHtml
import math
import operator
import time


if __name__ == '__main__':
	start = time.clock()
	nowtime,lastime=getTimes()

	print nowtime,lastime



	end = time.clock()
	print u"耗时: %f s" % (end - start)
