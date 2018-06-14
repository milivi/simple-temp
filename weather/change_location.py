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
		self.entry = tkinter.Entry(self.location_win)
		self.entry.pack()
		self.b = tkinter.Button(self.location_win, text="Enter", command=lambda: self.check_location(self.entry.get()))
		self.b.pack()
		self.owm = owm
		self.new_location = cur_location
		
	def get_location(self):
		"""Get the location change from the user"""
		self.location_win.mainloop()
		return self.new_location

	def check_location(self, new_location):
		"""Checks the entered weather location and updates if it is valid."""
		registry = self.owm.city_id_registry()
		poss_locations = registry.locations_for(new_location, country='US', matching='nocase')
		print(poss_locations)
		if poss_locations:
			print("You are valid")
			print(poss_locations[0])
			print(type(poss_locations[0]))
			self.new_location = poss_locations[0]
			self.location_win.quit()
		
	def destroy(self):
		"""Close the window."""
		self.location_win.destroy()