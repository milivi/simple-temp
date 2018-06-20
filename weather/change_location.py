"""change_location.py gets a user entered location to update the weather location

The location's validity is checked through pyowm"""

import tkinter
import pyowm

class change_location:
	def __init__ (self, owm, cur_location):
		"""Constructor for change_location class.
		
		Creates window to change the weather location.
		Parameters: owm - Open Weather Map Object
			    cur_location - the current weather location"""
		self.location_win = tkinter.Toplevel()
		self.location_win.geometry("500x500")
		self.location_win.title("Get Outta Town")
		self.city_entry = tkinter.Entry(self.location_win)
		self.city_entry.insert(0, cur_location)
		self.city_entry.pack()
		self.country_entry = tkinter.Entry(self.location_win)
		self.country_entry.insert(0, "US")
		self.country_entry.pack()
		self.b = tkinter.Button(self.location_win, text="Enter", command=lambda: self.check_location(self.city_entry.get(), self.country_entry.get()))
		self.b.pack()
		self.owm = owm
		self.new_location = cur_location
		
	def get_location(self):
		"""Get the location change from the user"""
		self.location_win.mainloop()
		return self.new_location

	def check_location(self, new_location, new_country):
		"""Checks the entered weather location and updates if it is valid."""
		registry = self.owm.city_id_registry()
		print(new_country)
		try:
			poss_locations = registry.locations_for(new_location, country=new_country, matching='nocase')
		except(ValueError):
			self.invalid_entry()
		if poss_locations:
			self.new_location = poss_locations[0].get_ID()
			self.location_win.quit()
		else:
			self.invalid_entry()
		
	def destroy(self):
		"""Close the window."""
		try:
			self.location_win.destroy()
		except(tkinter.TclError):
			pass
	
	def invalid_entry(self):
		"""Warn that the entered city is not a valid location."""
		invalid = tkinter.Label(self.location_win, text="Invalid City, try again", fg="red")
		invalid.pack()
