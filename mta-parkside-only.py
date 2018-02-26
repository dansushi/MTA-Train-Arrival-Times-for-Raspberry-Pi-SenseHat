#!/usr/bin/python
import sys
import json
import time
import datetime
from sys import exit

from sense_hat import SenseHat
sense = SenseHat()
sense.low_light = False     # Makes sure the SenseHat isn't in low light mode. This screws with the RGB values.
sense.clear()               # Clear the SenseHat screen

''' -----------------------------
MTA Live Time Checker for Parkside
-------------------------------'''

#CONSTANTS
#Colors     r    g    b
black =     0,   0,   0
white =   255, 255, 255
BLACK =  (  0,   0,   0)
WHITE =  (255, 255, 255)
GREEN =  (  0, 255,   0)
RED =    (255,   0,   0)
BLUE =   (  0,   0, 255)
YELLOW = (255, 255,   0)
PURPLE = (255,   0, 255)
CYAN =   (  0, 255, 255)
X = WHITE
O = BLACK


import urllib.request, json 
with urllib.request.urlopen("http://127.0.0.1:5000/by-id/78f3") as url: #check Parkside Only
#with urllib.request.urlopen("http://127.0.0.1:5000/by-id/84ac") as url: #check Times Square Only
		MTAPI_JSON = json.loads(url.read().decode()) # MTAPI_JSON is a dictionary
		
		northbound = MTAPI_JSON["data"][0]["N"] #show all northbound trains for Parkside
		print("Northbound trains are:")
		for x in northbound:
			route = x["route"]
			time = x["time"]
			#sense.show_message(time) 
			wait_in_minutes = 2 ## FIGURE OUT HOW TO CONVERT THIS DATETIME TO datetime format AND CALCULATE THE DIFFERENCE BETWEEN NOW AND ARRIVAL TIME
			sense.show_message(str(wait_in_minutes))
			print("Route is:", route)
			print("Arrival time is:", time,"\n")
				
		print("")
		
		southbound = MTAPI_JSON["data"][0]["S"] #show all southbound trains for Parkside
		print("Southbound trains are:")
		for x in southbound:
			route = x["route"]
			time = x["time"]
			print("Route is:", route)
			print("Arrival time is:", time,"\n")
			
