"""GetWeather.py gets the weather from OpenWeatherMap.

It puts the temperature in a small draggable label in the lower left of the screen.
"""

import time
import math
import tkinter
import pyowm
import change_location as wcl
from pyowm.exceptions.parse_response_error import ParseResponseError
from pyowm.exceptions.api_call_error import APICallError
import dateutil.parser
from tkinter.constants import RAISED
from Pmw import Balloon

class temperature:
	def __init__ (self, place):
		"""Constructor for temperature class.

		Parameter: place - the location to search.
		"""
		self.place = place
		
		self.label = tkinter.Label(text=':(', font=('Courier','20'), 
					fg='black', bg='grey', 
					height=2, width=3)
		self.label.master.overrideredirect(True)
		self.label.master.wm_attributes("-topmost", True)
		self.label.master.geometry("+5+850")
		self.label.master.wm_attributes("-transparentcolor", "grey")
		self.label.bind("<Button-1>", self.click)
		self.label.bind("<Button-3>", self.right_click)
		self.label.bind("<B1-Motion>", self.drag)
		self.label.pack()
		
		self.popup_menu = tkinter.Menu(self.label.master)
		self.popup_menu.add_command(label="Switch Color", command=self.change_color)
		self.popup_menu.add_command(label="Change Location", command=self.get_location)
		self.popup_menu.add_command(label="Exit", command=self.destroy)
		self.balloon = Balloon(self.label.master)

	def update_temp(self):
		"""Update the temperature every 10 minutes between 7 AM and 5 PM"""
		cur_hour = time.localtime()[3]
		if cur_hour > 6 and cur_hour < 18:
			try:
				self.observation = owm.weather_at_id(self.place)
			except (ParseResponseError, APICallError):
				ftemp = ':('
			else:
				w = self.observation.get_weather()
				temp = math.ceil(w.get_temperature('fahrenheit')['temp'])
				ftemp = f'{temp}' + u'\N{DEGREE SIGN}'
				self.balloon.unbind(self.label)
				self.balloon.bind(self.label, self.get_balloon_text(w))
			self.label.configure(text=ftemp)
		self.timer = self.label.after(600000, self.update_temp)
	
	def get_pointer_x(self):
		"""Return the x-coordinate of the cursor position."""
		return self.label.master.winfo_pointerx()
		
	def get_pointer_y(self):
		"""Return the y-coordinate of the cursor position."""
		return self.label.master.winfo_pointery()

	def update_position(self, x, y):
		"""Update the position of the label.
		
		Parameters: x - x-coordinate to move to
			    y - y-coordinate to move to
		"""
		self.label.master.geometry(f'+{x}+{y}')
		
	def click(self, event):
		"""On the left click event, saves the coordinates of the event."""
		self.offset_x = event.x
		self.offset_y = event.y
	
	def drag(self, event):
		"""On the drag event, calculates and updates the labels position."""
		x = self.get_pointer_x() - self.offset_x 
		y = self.get_pointer_y() - self.offset_y
		self.update_position(x, y)

	def right_click(self, event):
		"""On right click, popup menu appears."""
		try:
			self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
		finally:
			self.popup_menu.grab_release()
			
	def change_color(self):
		"""Switches the color of the label between light and dark."""
		if self.label.cget('fg') == 'black':
			font = 'white'
			backing = 'lavender blush'
		else:
			font = 'black'
			backing = 'grey'
		self.label.config(fg=font, bg=backing)
		self.label.master.wm_attributes("-transparentcolor", backing)
		
	def get_location(self):
		"""Get the location change input by user and update the temperature."""
		place_location = self.observation.get_location()
		self.change_loc = wcl.change_location(owm, place_location, self.get_pointer_x, self.get_pointer_y)
		place_location = self.change_loc.get_location()
		self.place = place_location.get_ID()
		self.label.after_cancel(self.timer)
		try:
			self.update_temp()
		except tkinter.TclError:
			pass
		
	def destroy(self):
		"""Destroy any windows remaining open."""
    
		try:
			self.change_loc.destroy()
		except AttributeError:
			pass
		self.label.master.destroy()
		
	def get_balloon_text(self, w):
		"""Get the weather text for the balloon.
		
		Parameters: w - a weather object"""
		last_update_time = dateutil.parser.parse(
									w.get_reference_time('iso')
								).astimezone(tz=None)
		rain = w.get_rain()
		snow = w.get_snow()
		wind = w.get_wind()['speed']
		balloon_string = f'Last updated {last_update_time.hour}:{last_update_time.minute}'
		if rain:
			balloon_string = ''.join([balloon_string, f'\nRain {rain}'])
		if snow:
			balloon_string = ''.join([balloon_string, f'\nSnow {snow}'])
		if wind:
			balloon_string = ''.join([balloon_string, f'\nWind Speed: {wind}'])
		return balloon_string
  
owm = pyowm.OWM('2e87feb9a967628ae1d395b6c0d26cab')
place = 5129780

widg = temperature(place)

widg.update_temp()
widg.label.mainloop()

