#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time,led,rainbowmaker

rainbow=rainbowmaker.rainbowmaker(1024)
rainbow.center=63
rainbow.width=112
rainbow.rgb_factor(4,6,2)
led=led.led()

while True:
	r,g,b=rainbow.next()
	led.rgbw(r,g,b)
	time.sleep(0.08)
