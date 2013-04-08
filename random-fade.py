#!/usr/bin/env python
# -*- coding: utf-8 -*-

import led,random,time

SLEEPTIME=0.08
FADESIZE=80

def interpolate_tuple( start, end, steps ):
    start_red = start[0]
    start_green = start[1]
    start_blue = start[2]
    target_red = end[0]
    target_green = end[1]
    target_blue = end[2]
    diff_red = target_red - start_red
    diff_green = target_green - start_green
    diff_blue = target_blue - start_blue
    buf = []
    for i in range(0, steps +1):
        r = start_red + (diff_red * i / steps)
        g = start_green + (diff_green * i / steps)
        b = start_blue + (diff_blue * i / steps)
        buf.append([r,g,b])
    return buf


def randlist(array):
    random.shuffle(array)
    return array

def random_color():
    unc=[random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255)]
    hc=0
    cln=[]
    for c in unc:
		if c>30:
			hc+=1
    if hc>2:
		cln=randlist([unc[0],unc[1],random.randrange(0, 5)])
    else:
        cln=unc		
    return cln
	
print random_color()

led=led.led()

col0=random_color()
while True:
	col1=random_color()
	print col0,col1
	colorlist=interpolate_tuple(col0,col1,FADESIZE)
	for color in colorlist:
		led.rgbw(color[0],color[1],color[2])
		time.sleep(SLEEPTIME)
	col0=col1
	col1=random_color()
	
	

