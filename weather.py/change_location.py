"""change_location.py gets a user entered location to update the weather location

The location's validity is checked through pyowm"""

import tkinter
import pyowm

class change_location:
	def __init__ (self, owm, cur_location, x_coordinate, y_coordinate):
		"""Constructor for change_location class.
		
		Creates window to change the weather location.
		Parameters: owm - Open Weather Map Object
			    cur_location - the current weather location"""
		self.location_win = tkinter.Tk()
		self.location_win.overrideredirect(True)
		self.location_win.geometry("200x150")
		self.location_win.geometry("+5+750")
		self.location_win.title("Get Outta Town")
		self.location_win.bind("<Button-1>", self.click)
		self.location_win.bind("<B1-Motion>", self.drag)
		
		tkinter.Label(self.location_win, text='City').grid(row=0, column=0, pady=10)
		self.city_entry = tkinter.Entry(self.location_win)
		self.city_entry.insert(0, cur_location.get_name())
		self.city_entry.grid(row=0, column=1, pady=10)
		
		tkinter.Label(self.location_win, text='Country').grid(row=1, column=0)
		self.country_entry = tkinter.Entry(self.location_win)
		self.country_entry.insert(0, "US")
		self.country_entry.grid(row=1, column=1)
		
		self.b = tkinter.Button(self.location_win, text="Enter", 
							command=lambda: 
								self.check_location(self.city_entry.get(), 
												self.country_entry.get().upper()))
		self.b.grid(row=2, column=1, pady=10)
		
		self.invalid = tkinter.Label(self.location_win, 
								text="Invalid City, try again", fg="red")
		
		self.owm = owm
		self.new_location = cur_location
		self.x_coordinate = x_coordinate()
		self.y_coordinate = y_coordinate()
		
	def get_location(self):
		"""Get the location change from the user"""
		self.location_win.geometry(f'+{self.x_coordinate}+{self.y_coordinate-150}')
		self.location_win.mainloop()
		self.destroy()
		return self.new_location

	def check_location(self, new_location, new_country):
		"""Checks the entered weather location and updates if it is valid."""
		registry = self.owm.city_id_registry()
		try:
			poss_locations = registry.locations_for(new_location, 
												country=new_country, 
												matching='nocase')
		except(ValueError):
			self.invalid_entry()
		else:
			if poss_locations:
				self.new_location = poss_locations[0]
				self.location_win.quit()
			else:
				self.invalid_entry()
		
	def destroy(self):
		"""Close the window."""
		try:
			self.location_win.destroy()
		except tkinter.TclError as error:
			pass
	
	def invalid_entry(self):
		"""Warn that the entered city is not a valid location."""
		self.invalid.grid(row=3, column=1)
		
	def click(self, event):
		"""On the left click event, saves the coordinates of the event."""
		self.offset_x = event.x
		self.offset_y = event.y
	
	def drag(self, event):
		"""On the drag event, calculates and updates the labels position."""
		x = self.location_win.winfo_pointerx() - self.offset_x 
		y = self.location_win.winfo_pointery() - self.offset_y
		self.location_win.geometry(f'+{x}+{y}')
