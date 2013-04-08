#!/usr/bin/env python
# dmx-rgb-controller

import time,led


SLEEPTIME=0.08


led=led.led()	


try:
	i=0
	while True:
		if i==2: i=0
		if (i==1):
			val=0
			duo=255
		else: 
			val=255
			duo=0
		led.set_white(val)
		#led.set_blue(duo)
		led.send()
		time.sleep(SLEEPTIME)
		i+=1
		
except:
	led.blackout()
	exit

