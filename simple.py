#!/usr/bin/env python
# dmx-rgb-controller
# (c) 17.3.2013 by cyrill von wattenwyl
# h-powered

import pygtk,gtk,dmx512
pygtk.require('2.0')

#channel settings
DMX_CHANNEL_R=0
DMX_CHANNEL_G=1
DMX_CHANNEL_B=2
DMX_CHANNEL_DIM=4

class dmx_rgb_controller:
	
    def __init__(self):
        self.dmx=dmx512.dmx()
        self.drawingarea = gtk.DrawingArea()
        self.color = self.drawingarea.get_colormap().alloc_color(0, 255, 0)
        self.colorseldlg = gtk.ColorSelectionDialog("Select Lamp Color")
        colorsel = self.colorseldlg.colorsel
        colorsel.set_previous_color(self.color)
        colorsel.set_current_color(self.color)
        colorsel.set_has_palette(True)
        colorsel.set_has_opacity_control(True)
        colorsel.connect("color_changed", self.update_dmx_signal)        
        colorsel.connect("delete_event", self.bye)
        self.colorseldlg.run()
        self.bye()
    
    def bye(self, widget=False, event=False):
        try:
			gtk.main_quit()
        except RuntimeError: 
			quit()
        return True
        
    def update_dmx_signal(self, widget):
        color = self.colorseldlg.colorsel.get_current_color()
        alpha = self.colorseldlg.colorsel.get_current_alpha()
        dmx_dim=self.range_convert(alpha)
        dmx_red=self.range_convert(color.red)
        dmx_green=self.range_convert(color.green)
        dmx_blue=self.range_convert(color.blue)
        self.dmx.set_channel(DMX_CHANNEL_R,dmx_red)
        self.dmx.set_channel(DMX_CHANNEL_G,dmx_green)
        self.dmx.set_channel(DMX_CHANNEL_B,dmx_blue)
        self.dmx.set_channel(DMX_CHANNEL_DIM,dmx_dim)
        self.dmx.send()
        #print dmx_red,dmx_green,dmx_blue,dmx_dim

    def range_convert(self,value,old_min=0,old_max=65535,new_min=0,new_max=255):
		return (((value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
  
if __name__ == "__main__":
    dmx_rgb_controller()
