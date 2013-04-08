#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time,urllib2
from xml.dom import minidom
from led import led

TEMPURL="http://e23.ch/aare/xml/"
MIN_TEMP=0
MAX_TEMP=30
SLEEPTIME=20


def xml_get_tag_data(tag,xml):
	val=xml.getElementsByTagName(tag)[0].toxml()
	return float(val.replace('<'+tag+'>','').replace('</'+tag+'>',''))
	
def range_convert(value,old_min=0,old_max=40,new_min=0,new_max=510):
	return (((value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min

def col(val):
	cc=0
	out=None
	red=green=blue=0
	if val<0: return 0,0,255
	while True:
		blue=255
		for green in range(0,255):
			if cc==val:
				out=True
				break
			blue=blue-1
			cc=cc+1
		if out is True: 
			return red,green,blue
		green=255
		for red in range(0,255):
			if cc==val:
				out=True
				break
			green=green-1
			cc=cc+1
		if out is True: 
			return red,green,blue
		else:
			return 255,0,0

print "Server-Url:\t{0}\nReload every\t{1} Sec\n".format(TEMPURL,SLEEPTIME)
led=led()
reqnum=1
try:
	while True:
		data=urllib2.urlopen(TEMPURL).read()
		xml=minidom.parseString(data)
		temp=xml_get_tag_data("temp",xml)
		timestamp=xml_get_tag_data("timestamp",xml)
		temp_col=int(round(range_convert(temp,MIN_TEMP,MAX_TEMP)))
		date_human=time.strftime("%d.%m.%Y %H:%M:%S",time.gmtime(timestamp))
		r,g,b=col(temp_col)
		led.rgbw(r,g,b)
		print "#{3}\t{0}\t{1}°C\t\tscore={2}/512".format(date_human,temp,temp_col,reqnum)
		reqnum=reqnum+1
		time.sleep(SLEEPTIME)
		
except:
	led.blackout()
	print "bye"
	exit()
