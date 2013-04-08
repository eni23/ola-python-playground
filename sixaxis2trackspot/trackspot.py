#!/usr/bin/env python
# -*- coding: utf-8 -*-


#
# python class for controlling higend systems trackspot 41
# (c) 2013 by cyrill von wattenwyl
#
# example-usage:
# scanner=trackspot();
# scanner.dim(255)
# scanner.set_color(2);
# scanner.mspeed(100)
# scanner.pan(10)
# scanner.tilt(200)
#

import sys
sys.path.append("..")
import dmx512

class trackspot(dmx512.dmx):
	
	def __init__(self):
		dmx512.dmx.__init__(self)
		self.ch_pan=0
		self.ch_tilt=1
		self.ch_color=2
		self.ch_gobo=3
		self.ch_shutter=4
		self.ch_dimmer=5
		self.ch_mspeed=6
		self.color_pos=[0x00,0x20,0x36,0x4F,0x6E,0x8A,0xA0,0xC8,0xD2,0xF0]
		self.gobo_pos=[0x00,0x20,0x36,0x4F,0x6E,0x8A,0xA0,0xC8,0xD2,0xF0]
		self.shutter_pos=[0x00,0x1A,0x33,0x4D,0x66,0x80,0x99,0xB3,0xCC,0xE6,0xF2]
		print "Initialized Scanner : Trakspot TS41 Universe "+str(self.universe)+", Start Address: 0, Cannels: 7"
		
	def set_color(self,color_id):
		self.send_dmx(self.ch_color,self.color_pos[color_id])
	
	def set_gobo(self,gobo_id):
		self.send_dmx(self.ch_gobo,self.gobo_pos[gobo_id])
	
	def set_shutter(self,shutter_id):
		self.send_dmx(self.ch_shutter,self.shutter_pos[shutter_id])	
	
	def pan(self,value):
		self.send_dmx(self.ch_pan,value)
			
	def tilt(self,value):
		self.send_dmx(self.ch_tilt,value)	
		
	def dim(self,value):
		self.send_dmx(self.ch_dimmer,value)
	
	def mspeed(self,value):
		self.send_dmx(self.ch_mspeed,value)

	def send_dmx(self,channel,value):
		self.set_channel(channel,value)
		self.send()
	
