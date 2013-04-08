#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

#sudo sixad --start
kill it with if not quitting on interrupt:
#kill -9 `ps -A | grep python | tail -n1 | cut -d" " -f2`

"""

import pygame,time,trackspot,array

class App:
	
	
	def __init__(self):
		#init joystick
		pygame.init()
		self.j = pygame.joystick.Joystick(0)
		self.j.init()
		print 'Initialized Joystick : %s' % self.j.get_name()
				
		#init dmx device
		self.scanner=trackspot.trackspot()
		# gobo: 0 (open), shutter: 1 (open), color: 0 (0 open), 100%dimmer
		self.scanner.set_gobo(0)
		self.gobo_num=0
		self.scanner.set_shutter(1)
		self.shutter_num=1
		self.scanner.set_color(0)
		self.color_num=0
		self.scanner.dim(255)
		self.scanner.mspeed(255)
		self.time_gobo=self.utime()
		self.time_color=self.utime()
		self.rmbl_time=self.utime()
		
		self.act_dim=255
		self.act_ms=255
		
		self.clk = pygame.time.Clock()
		self.pos_buf=array.array("B")
		self.pos_buf.append(128) #x
		self.pos_buf.append(128)
		self.scanner.pan(128)
		self.scanner.tilt(128)
		
		self.saved_pos=array.array("B")
		self.saved_pos.append(50)
		self.saved_pos.append(90)
		
		self.time_sav=0
		self.time_rst=0
		
		
	#function for convert ps3axis in dmx-range
	def axisrange2dmxrange(self,axis_val):
		return int(((axis_val - (-1))*255) / 2 )
		
	def axis_calc(self,val,mr=1):
		return int(((val - (-1))*mr) / 2 )

	def utime(self):
		return int(float("%6f" % time.time())*10000)
	
	
	def main(self):
		
		while True:
			pygame.event.pump()
			for i in range(0, self.j.get_numbuttons()):
				
				
				#save pos push button O
				if (i==13) and (self.j.get_button(i) != 0):
					time_act=self.utime()
					diff=time_act-self.time_sav
					if diff>2000:
						self.saved_pos[0]=self.pos_buf[0]
						self.saved_pos[1]=self.pos_buf[1]
						print "position saved"
						self.time_sav=self.utime()
				
				#load pos push button X
				if (i==14) and (self.j.get_button(i) != 0):
					time_act=self.utime()
					diff=time_act-self.time_rst
					if diff>2000:
						self.pos_buf[0]=self.saved_pos[0]
						self.pos_buf[1]=self.saved_pos[1]
						self.scanner.tilt(self.saved_pos[0])
						self.scanner.pan(self.saved_pos[1])
						print "goto saved pos"
						self.time_rst=self.utime()
						
				
				#quit push on ps-putton
				if (i==16) and (self.j.get_button(i) != 0):
					#self.ff.rocks()
					#self.ff.stop()
					pygame.quit()
					quit()
				
				#color-changer +-
				elif (i==8) and (self.j.get_button(i) != 0):
					time_act=self.utime()
					diff=time_act-self.time_color
					if diff>1000:
						self.color_num+=1
						if (self.color_num>9):
							self.color_num=0
						print "++color act=%i" % self.color_num
						self.scanner.set_color(self.color_num)
						self.time_color=self.utime()
				elif (i==9) and (self.j.get_button(i) != 0):
					time_act=self.utime()
					diff=time_act-self.time_color
					if diff>1000:
						self.color_num-=1
						if (self.color_num<0):
							self.color_num=9
						print "--color act=%i" % self.color_num
						self.scanner.set_color(self.color_num)
						self.time_color=self.utime()
						
						
				#gobo-changer +-
				elif (i==10) and (self.j.get_button(i) != 0):
					time_act=self.utime()
					diff=time_act-self.time_gobo
					if diff>1000:
						self.gobo_num+=1
						if (self.gobo_num>9):
							self.gobo_num=0
						print "++gobo act=%i" % self.gobo_num
						self.scanner.set_gobo(self.gobo_num)
						self.time_gobo=self.utime()
					
				elif (i==11) and (self.j.get_button(i) != 0):
					time_act=self.utime()
					diff=time_act-self.time_gobo
					if diff>1000:
						self.gobo_num-=1
						if (self.gobo_num<0):
							self.gobo_num=9
						print "--gobo act=%i" % self.gobo_num
						self.scanner.set_gobo(self.gobo_num)
						self.time_gobo=self.utime()		
				
				#center pos
				elif (i==1) and (self.j.get_button(i) != 0): 	
					self.scanner.tilt(128)
					self.scanner.pan(128)
					self.pos_buf[0]=self.pos_buf[1]=128
					print "center mirror"
				
				#dim-
				elif (i==7) and (self.j.get_button(i) != 0):
					if (self.act_dim>11):
						self.act_dim=self.act_dim-10
						self.scanner.dim(self.act_dim)
						print("dim="+str(self.act_dim));
						
				elif (i==5) and (self.j.get_button(i) != 0):
					if (self.act_dim<250):
						self.act_dim=self.act_dim+10
						self.scanner.dim(self.act_dim)	
						print("dim="+str(self.act_dim));
	
	
				elif (i==6) and (self.j.get_button(i) != 0):
					if (self.act_ms>5):
						self.act_ms=int(self.act_ms)-5
						self.scanner.mspeed(self.act_ms)
						print("mspeed="+str(self.act_ms));
						
				elif (i==4) and (self.j.get_button(i) != 0):
					if (self.act_ms<255):
						self.act_ms=int(self.act_ms)+5
						self.scanner.mspeed(self.act_ms)	
						print("mspeed="+str(self.act_ms));
				

			#tilt <>
			if self.j.get_axis(0) != 0.00:
				ax=self.j.get_axis(0)
				if (ax>0): #go back
					ac=self.axis_calc(ax)
					if ((self.pos_buf[0]+ac)<256):
						self.pos_buf[0]=self.pos_buf[0]+ac
				if (ax<0): #go forward
					ax=(ax - (2*ax))
					ac=self.axis_calc(ax)
					if ((self.pos_buf[0]-ac)>-1):
						self.pos_buf[0]=self.pos_buf[0]-ac
				self.scanner.tilt(self.pos_buf[0])	
				print(self.pos_buf)
		
			#pan ^
			if self.j.get_axis(1) != 0.00:
				ay=self.j.get_axis(1)
				if (ay>0): #go up
					ac=self.axis_calc(ay)
					if ((self.pos_buf[1]+ac)<256):
						self.pos_buf[1]=self.pos_buf[1]+ac
				if (ay<0): #go down
					ay=(ay - (2*ay)) # make it (hiv) positive
					ac=self.axis_calc(ay)
					if ((self.pos_buf[1]-ac)>-1):
						self.pos_buf[1]=self.pos_buf[1]-ac
				print(self.pos_buf)
				self.scanner.pan(self.pos_buf[1])

			
			self.clk.tick(40) # max 40 fps

		
			
			
	
app = App()
app.main()
