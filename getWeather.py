"""getWeather.py gets the weather from OpenWeatherMap.

It puts the temperature in a small label in the lower left of the screen.
"""

import time
import math

import tkinter
import pyowm


class temperature:
	def __init__ (self, place):
		"""Constructor for temperature class.

		Parameter: place - the location code to search.
		"""
		self.label = tkinter.Label(text=':(', font=('Courier','20'), 
					fg='white', bg='lavender blush', 
					height = 2, width=3)
		self.label.master.overrideredirect(True)
		self.label.master.wm_attributes("-topmost", True)
		self.label.master.geometry("+5+850")
		self.label.master.wm_attributes("-transparentcolor", "lavender blush")
		self.label.master.wm_attributes("-disabled", True)
		self.place = place
		self.update_temp()

	def update_temp(self):
		"""Update the temperature every 10 minutes"""
		cur_hour = time.localtime()[3]
		#only update between 7 AM and 5 PM
		if cur_hour > 6 and cur_hour < 17:
			observation = owm.weather_at_place(self.place)
			w = observation.get_weather()

			temp = math.ceil(w.get_temperature('fahrenheit')['temp'])
			ftemp = f'{temp}' + u'\N{DEGREE SIGN}'
			print(ftemp)
			self.label.configure(text = ftemp)
			print(time.localtime())
		self.label.after(600000, self.update_temp)


owm = pyowm.OWM('2e87feb9a967628ae1d395b6c0d26cab')
place = 'Olean,US'

widg = temperature(place)
widg.label.pack()
widg.label.mainloop()

