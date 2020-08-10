#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/14 9:39
# @Author  : Addicated
# @Site    : 
# @File    : handle_yaml.py
# @Software: PyCharm
import yaml
from common.handle_path import DATA_DIR
class Handle_Yml:
	def __init__(self,file_name):
		self.file_name = file_name

	def read_yml(self):
		stream_yml = open(DATA_DIR + F"\{self.file_name}",encoding="utf-8")
		cases = yaml.load(stream_yml)
		# print(e)
		# print(type(e))
		# for i in e:
		# 	print(i)
		return cases
