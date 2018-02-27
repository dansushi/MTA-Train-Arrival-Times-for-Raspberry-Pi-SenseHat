#!/usr/bin/python
import signal
import sys
import json
import math
import time
import datetime
from datetime import timedelta
import pandas as pd
from sys import exit
from custom_led_displays import * # Import custom functions from other file

from sense_hat import SenseHat
sense = SenseHat()
sense.low_light = True     # Makes sure the SenseHat isn't in low light mode. This screws with the RGB values.
sense.clear()               # Clear the SenseHat screen

''' -----------------------------
MTA Live Time Checker for Parkside
-------------------------------'''

# MINI-FUNCTIONS:

def mta_datetime_converter(time):
	convert_from_str_to_UTC_datetime = pd.to_datetime(time, format='%Y-%m-%dT%H:%M:%S')
	return convert_from_str_to_UTC_datetime


# LOGIC

def run_logic(which_direction):
	import urllib.request, json 
	with urllib.request.urlopen("http://127.0.0.1:5000/by-id/78f3") as url: #check Parkside Only
	#with urllib.request.urlopen("http://127.0.0.1:5000/by-id/84ac") as url: #check Times Square Only
			MTAPI_JSON = json.loads(url.read().decode()) # MTAPI_JSON is a dictionary
			
			global wts
			wts = []	# makes empty list called wts
			direction = MTAPI_JSON["data"][0][which_direction] #show all north/southbound trains for Parkside
			print(which_direction, ":")
			for x in direction:
				route = x["route"]
				time = x["time"]
				conv_time = mta_datetime_converter(time)
					#Uses function to convert the MTA Date and Time string to class datetime in UTC
				wait_time_secs = timedelta.total_seconds(conv_time - datetime.datetime.utcnow())
					# find delta/difference in seconds between conv_time and current UTC timewait_time
				wait_time_mins = wait_time_secs / 60
					# wait time in minutes
				if wait_time_secs > 60:		#If train is more than one minute away
					wait_time = str(int(math.floor(wait_time_mins)))
				elif wait_time_secs < 0:	#If *negative seconds*
					wait_time = "0"
					wait_time_mins = 0		#Prevents negative second from showing up in ETA
				else:						#If train is less than one minute away
					wait_time = "0"
				# wait time in minutes, rounded down, converted to string
				wts.append([route,wait_time])
				#sense.show_message(wait_time)
				#print("wait_time_secs: ",wait_time_secs)
				#print("wait_time_mins: ",wait_time_mins)
				#print("wait_time: ",wait_time)
				print(str(route) + ': ' + str(wait_time) + 'm' + str(round((wait_time_mins - math.floor(wait_time_mins)) * 60)) + 's')
				
			print("")
			print(wts)



def SenseHatDisplay():
	
	#Colors     r    g    b
	B = BLACK =  (  0,   0,   0)	# Background color (default BLACK)
	T = WHITE =  (255, 255, 255)	# Text color (default WHITE)
	GRAY =   (128, 128, 128)
	BROWN =  (121,  76,  47)
	GREEN =  (  0, 255,   0)
	RED =    (255,   0,   0)
	BLUE =   (  0,   0, 255)
	YELLOW = (255, 140,   0)
	PURPLE = (255,   0, 200)
	ORANGE = (255, 10,   0)
	
	if wts[0][0] == "N" or wts[0][0] == "Q" or wts[0][0] == "R" or wts[0][0] == "W":
		T = YELLOW
	elif wts[0][0] == "B" or wts[0][0] == "D" or wts[0][0] == "F" or wts[0][0] == "M":
		T = ORANGE
	elif wts[0][0] == "1" or wts[0][0] == "2" or wts[0][0] == "3":
		T = RED
	elif wts[0][0] == "4" or wts[0][0] == "5" or wts[0][0] == "6":
		T = GREEN
	elif wts[0][0] == "7":
		T = PURPLE
	elif wts[0][0] == "A" or wts[0][0] == "C" or wts[0][0] == "E":
		T = BLUE
	elif wts[0][0] == "G":
		T = GREEN
	elif wts[0][0] == "J" or wts[0][0] == "Z":
		T = BROWN
	elif wts[0][0] == "L" or wts[0][0] == "S":
		T = GRAY

	current_pixels = sense.get_pixels()
	first_wts = wts[0][1]		# Puts first train wait time into variable
	#	first [] is item in list, i.e. next arriving train in order of arrival
	#	second [] is route letter [0] / wait time [1]. LEAVE AT [1]
	ones_digit = ones(T,B,first_wts[-1])		# Gets last char in first_wts string
	if len(first_wts) > 1:					# If wait time is more than 1 digit (9 mins)
		tens_digit = ones(T,B,first_wts[-2])		# Gets second to last char in first_wts string
	else:
		tens_digit = ones(T,B,"empty")
	sense.set_pixels(
	tens_digit[0:4]   + ones_digit[0:4]   +
	tens_digit[4:8]   + ones_digit[4:8]   +
	tens_digit[8:12]  + ones_digit[8:12]  +
	tens_digit[12:16] + ones_digit[12:16] +
	tens_digit[16:20] + ones_digit[16:20] +
	current_pixels[40:64]
	)

def main():
	#Allows for clearing SenseHat on keyboard interrupt exit

	while True:
		try:
			which_direction = "N"		#Which direction do you want to check? (N, S, or B)
			run_logic(which_direction)
			SenseHatDisplay()
			time.sleep(5) #sleep X seconds between running logic
		except (KeyboardInterrupt, SystemExit):
			sense.clear()
			print("\n\nKEYBOARD INTERRUPT EXIT\n")
			raise
			
#Runs Main Program:
main() 
