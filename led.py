#!/usr/bin/env python
# dmx-led-rgbw-controller

import dmx512,time

DMX_CHANNEL_R=0
DMX_CHANNEL_G=1
DMX_CHANNEL_B=2
DMX_CHANNEL_W=3
BLACKOUT_SLEEPTIME=0.1

class led:

	def __init__(self, universe=0):
		self.dmx=dmx512.dmx()

	def set_channel(self,channel,value):
		if value<0:
			value=0
		if value>255:
			print "warning: over 12V"
		if value>393:
			print "value too big"
			return
		real_value=self.range_convert(value)
		self.dmx.set_channel(channel,real_value)

	def send(self):
		self.dmx.send()

	def range_convert(self,value,old_min=0,old_max=255,new_min=0,new_max=166):
		return (((value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min

	def red(self,value):
		self.set_channel(DMX_CHANNEL_R,value)
		self.send()

	def set_red(self,value):
		self.set_channel(DMX_CHANNEL_R,value)

	def green(self,value):
		self.set_channel(DMX_CHANNEL_G,value)
		self.send()

	def set_green(self,value):
		self.set_channel(DMX_CHANNEL_G,value)

	def blue(self,value):
		self.set_channel(DMX_CHANNEL_B,value)
		self.send()

	def set_blue(self,value):
		self.set_channel(DMX_CHANNEL_B,value)

	def white(self,value):
		self.set_channel(DMX_CHANNEL_W,value)
		self.send()

	def set_white(self,value):
		self.set_channel(DMX_CHANNEL_W,value)

	def all_white(self):
		self.set_channel(DMX_CHANNEL_R,255)
		self.set_channel(DMX_CHANNEL_G,155)
		self.set_channel(DMX_CHANNEL_B,100)
		self.set_channel(DMX_CHANNEL_W,053)
		self.send()

	def blackout(self):
		self.set_channel(DMX_CHANNEL_R,0)
		self.set_channel(DMX_CHANNEL_G,0)
		self.set_channel(DMX_CHANNEL_B,0)
		self.set_channel(DMX_CHANNEL_W,0)
		time.sleep(BLACKOUT_SLEEPTIME)
		self.send()
		
	def rgbw(self,red,green,blue,white=None):
		self.set_channel(DMX_CHANNEL_R,red)
		self.set_channel(DMX_CHANNEL_G,green)
		self.set_channel(DMX_CHANNEL_B,blue)
		if white is not None:
			self.set_channel(DMX_CHANNEL_W,white)
		self.send()
