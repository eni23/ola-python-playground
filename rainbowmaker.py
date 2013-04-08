#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
 
class rainbowmaker:
	def __init__(self,num=25):
		self.num=num
		self.act_num=0
		self.center=128
		self.width=128
		self.phase=0
		self.factor_red=30
		self.factor_green=6
		self.factor_blue=2
		self.freq=False
		
	def next(self):
		if self.freq is False:
			self.freq=math.pi*2/self.num
		i=self.act_num
		red=math.sin(self.freq*i+self.factor_red+self.phase) * self.width + self.center
		green=math.sin(self.freq*i+self.factor_green+self.phase) * self.width + self.center
		blue=math.sin(self.freq*i+self.factor_blue+self.phase) * self.width + self.center
		self.act_num=self.act_num+1
		if red<0:red=0
		if green<0:green=0
		if blue<0:blue=0
		return int(red),int(green),int(blue)

	def get(self,num):
		self.act_num=num-1
		return self.next()
		
	def rgb_factor(self,factor_red,factor_green,factor_blue):
		self.factor_red=factor_red
		self.factor_green=factor_green
		self.factor_blue=factor_blue
		
	def rgb2color(self,r,g,b):
		return "#" + str(hex(r))[2:] + str(hex(g))[2:] + str(hex(b))[2:]
 
