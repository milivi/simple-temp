"""getWeather.py gets the weather from OpenWeatherMap.

It puts the temperature in a small draggable label in the lower left of the screen.
"""

import time
import math
import tkinter
import pyowm

class temperature:
	def __init__ (self, place):
		"""Constructor for temperature class.

		Parameter: place - the location to search.
		"""
		self.place = place
		
		self.label = tkinter.Label(text=':(', font=('Courier','20'), 
					fg='white', bg='lavender blush', 
					height=2, width=3)
		self.label.master.overrideredirect(True)
		self.label.master.wm_attributes("-topmost", True)
		self.label.master.geometry("+5+850")
		self.label.master.wm_attributes("-transparentcolor", "lavender blush")
		self.label.bind("<Button-1>", self.click)
		self.label.bind("<Button-3>", self.right_click)
		self.label.bind("<B1-Motion>", self.drag)
		self.label.pack()
		
		self.popup_menu = tkinter.Menu(self.label.master)
		self.popup_menu.add_command(label="Switch Color", command=self.change_color)
		self.popup_menu.add_command(label="Change Location", command=self.change_location)
		self.popup_menu.add_command(label="Exit", command=self.label.master.destroy)
		
		self.update_temp()

	def update_temp(self):
		"""Update the temperature every 10 minutes between 7 AM and 5 PM"""
		cur_hour = time.localtime()[3]
		if cur_hour > 6 and cur_hour < 17:
			observation = owm.weather_at_place(self.place)
			w = observation.get_weather()
			temp = math.ceil(w.get_temperature('fahrenheit')['temp'])
			ftemp = f'{temp}' + u'\N{DEGREE SIGN}'
			self.label.configure(text = ftemp)
		self.label.after(600000, self.update_temp)
		print(self.place)
	
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
		"""On right click, popup menu"""
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
		
	def change_location(self):
		"""Creates window to change the weather location."""
		location_win = tkinter.Tk()
		location_win.geometry("500x500")
		location_win.title("Get Outta Town")
		entry = tkinter.Entry(location_win)
		entry.pack()
		b = tkinter.Button(location_win, text="Enter", command=lambda: self.check_location(entry.get()))
		b.pack()
		location_win.mainloop()

	def check_location(self, new_location):
		"""Checks the entered weather location and updates if it is valid."""
		registry = owm.city_id_registry()
		poss_locations = registry.locations_for(new_location, country='US', matching='nocase')
		print(poss_locations)
		if poss_locations:
			print("You are valid")
			print(poss_locations[0])
			self.place = new_location
	


owm = pyowm.OWM('2e87feb9a967628ae1d395b6c0d26cab')
place = 'Olean,US'

widg = temperature(place)
widg.label.mainloop()

