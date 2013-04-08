#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# dmx512 library
# sending dmx-frames, the class handles buffering of channels
# and only packs data frames long as needed.
#
# example usage:
# dmx=dmx512.dmx
# dmx.set_channel(1,255)
# dmx.set_channel(419,39)
# dmx.send()
#
# dmx.channel[21] //get buffer of channel 21
#

import array
from ola.ClientWrapper import ClientWrapper


class dmx:
	
	def __init__(self,universe=1,send_only_changes=True):
		self.channel=array.array('B')
		self.channel_new=array.array('B')
		self.send_only_changes=send_only_changes
		for i in range(512):
			self.channel.append(0)
			self.channel_new.append(0)
		self.channels_change=array.array('H')
		self.dataframe=array.array('B')
		self.universe=universe
		self.count=0
		self.ola_wrapper=ClientWrapper()
		self.ola_client = self.ola_wrapper.Client()
		
	def reset_internal_buffers(self):
		for i in range(0,512):
			self.channel_new.append(0)
		del self.channels_change, self.dataframe
		self.channels_change=array.array('H')
		self.dataframe=array.array('B')
			
	def set_channel(self,channel,value):
		self.channel_new[channel]=value
		self.channels_change.append(channel)
	
	def build_sendframe(self):
		num_channels=512 if self.send_only_changes is False else max(self.channels_change)+1
		for i in range(0,num_channels):
			if i in self.channels_change:
				self.dataframe.append(self.channel_new[i])
			else:
				self.dataframe.append(self.channel[i])

	def send(self):
		self.build_sendframe()
		num_channels=512 if self.send_only_changes is False else max(self.channels_change)+1
		for i in range(0,num_channels):
			if i in self.channels_change:
				self.channel[i]=self.dataframe[i]
		self.count=self.count+1
		self.ola_wrapper.Client().SendDmx(self.universe,self.dataframe)
		self.reset_internal_buffers()
