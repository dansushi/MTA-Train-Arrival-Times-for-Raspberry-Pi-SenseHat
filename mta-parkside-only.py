#!/usr/bin/python
import signal
import sys
import math
import time
import datetime
import subprocess
from datetime import timedelta
import pandas as pd
from sys import exit
from custom_led_displays import * # Import custom functions from other file
import urllib.request, json 

from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(0)
sense.low_light = True
sense.clear()


''' -----------------------------
MTA Live Time Checker

Description blah blah blah blah 
blah blah blah blah blah blah 
blah blah blah blah blah blah 
-------------------------------'''


'''----------------------------------------------------------------------------'''
# Defines global variables
global wts
wts = ""
global which_direction

# Defines all the stations in the list with their respective IDs
global station_list

station_list = 	[]
station_list.extend((
["Church Ave", "b2e2"],					# Station 0 in list
["Parkside Ave", "78f3"],				# Station 1 in list
["Prospect Park", "cf15"],				# Station 2 in list
["Winthrop St", "cb70"],				# Station 3 in list
["Times Square - 42nd St", "84ac"],		# Station 4 in list
))

global current_station
global n
n = 1									# Initial station number (n) set to 1
current_station = station_list[n]		# Sets current station to the first station in the list by default


'''----------------------------------------------------------------------------'''
# MINI-FUNCTIONS:

# Converts MTA's Date and Time to class datetime in UTC for delta comparison)
def mta_datetime_converter(time):
	convert_from_str_to_UTC_datetime = pd.to_datetime(time, format='%Y-%m-%dT%H:%M:%S')
	return convert_from_str_to_UTC_datetime

#Converts wt_dec from string to int, then to binary, without 0b at the front
def dec_to_bin(wt_dec): 
	wt_bin = bin(int(wt_dec))[2:] 
	return wt_bin

# 20 pixels of black for separating elements on the SenseHat LED screen
def black_pixels():
	b = (0, 0, 0) # Black
	black_pixel_line = [b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b,]
	return black_pixel_line

# Converts wt_bin from binary string to list with Bs and Ts
def wt_bin_to_pixels(T,B,wt_bin):
	bin_pixels = []	# bin_pixels starts out as empty list
	for x in list((8 - len(wt_bin)) * "0" + wt_bin):
	#Checks length of wt_bin, tacks on leading zeros to make total length 8 characters, then converts to list
		if x == "0":				# Replaces zeros with B
			bin_pixels.append(B)
		elif x == "1":				# Replaces ones with T
			bin_pixels.append(T)
	return bin_pixels

# LED SenseHat screen with "ER" for ERROR
def MTAPIConnectionError():
	g = (255, 0, 0) # Red
	b = (0, 0, 0) # Black
	error_pixels = [
		g, g, g, b, g, g, g, b,
		g, b, b, b, g, b, b, g,
		g, b, b, b, g, b, b, g,
		g, g, g, b, g, g, g, b,
		g, b, b, b, g, b, b, g,
		g, b, b, b, g, b, b, g,
		g, g, g, b, g, b, b, g,
		b, b, b, b, b, b, b, b,
	]
	return error_pixels

# Figures out the color of the number/train line (tr is train number)
def determine_text_color(tr):
	
	#Colors     r    g    b
	BLACK =  (  0,   0,   0)	# Background color (default BLACK)
	WHITE =  (255, 255, 255)	# Text color (default WHITE)
	GRAY =   ( 10,  10,  10) #( 128, 128, 118)
	BROWN =  (121,  76,  47)
	GREEN =  (  0, 255,   0)
	RED =    (255,   0,   0)
	BLUE =   (  0,   0, 255)
	YELLOW = (255, 140,   0)
	PURPLE = (255,   0, 200)
	ORANGE = (255,  10,   0)
	
	if wts[tr][0] == "N" or wts[tr][0] == "Q" or wts[tr][0] == "R" or wts[tr][0] == "W":
		return YELLOW
	elif wts[tr][0] == "B" or wts[tr][0] == "D" or wts[tr][0] == "F" or wts[tr][0] == "M":
		return ORANGE
	elif wts[tr][0] == "1" or wts[tr][0] == "2" or wts[tr][0] == "3":
		return RED
	elif wts[tr][0] == "4" or wts[tr][0] == "5" or wts[tr][0] == "6":
		return GREEN
	elif wts[tr][0] == "7":
		return PURPLE
	elif wts[tr][0] == "A" or wts[tr][0] == "C" or wts[tr][0] == "E":
		return BLUE
	elif wts[tr][0] == "G":
		return GREEN
	elif wts[tr][0] == "J" or wts[tr][0] == "Z":
		return BROWN
	elif wts[tr][0] == "L" or wts[tr][0] == "S":
		return GRAY
	
'''----------------------------------------------------------------------------'''

# JOYSTICK FUNCTIONS

def joystick_up(event):

	global current_station
	global is_held
	global which_direction

	print("up event which_direction is" , which_direction)
	if event.action == "pressed" and event.direction == "up":
		print("Up")
		if which_direction == "S": #If up_press on South, change to Both
			which_direction = "N"														# <-- CHANGE BACK TO "B" when both mode is ready
			print("S -> B")
			sense.set_pixels(N_B_S_display(which_direction))						# Displays up, both, or down mode
		elif which_direction == "B":   #If up_press on Both, change to North
			which_direction = "N"
			print("B -> N")
			sense.set_pixels(N_B_S_display(which_direction))						# Displays up, both, or down mode
		else:                       #If up_press on North, keep at North
			which_direction == "N"
			print("N -> N")
			sense.set_pixels(N_B_S_display(which_direction))						# Displays up, both, or down mode
	if event.action == "held":
		is_held = True
	elif event.action == "released":
		print("You released Up")
		
def joystick_down(event):

	global current_station
	global is_held
	global which_direction
	
	print("down event which_direction is" , which_direction)
	if event.action == "pressed" and event.direction == "down":
		print("Down")
		if which_direction == "N": #If down_press on North, change to Both
			which_direction = "S"														# <-- CHANGE BACK TO "B" when both mode is ready
			print("N -> B")
			sense.set_pixels(N_B_S_display(which_direction))						# Displays up, both, or down mode
		elif which_direction == "B":   #If down_press on Both, change to South
			which_direction = "S"
			print("B -> S")
			sense.set_pixels(N_B_S_display(which_direction))						# Displays up, both, or down mode
		else:                       #If down_press on South, keep at South
			which_direction == "S"
			print("S -> S")
			sense.set_pixels(N_B_S_display(which_direction))						# Displays up, both, or down mode
	if event.action == "held":
		is_held = True
	elif event.action == "released":
		print("You released Down")

def joystick_left(event):	# Cycles station to the previous one in the list

	global current_station
	global is_held
	
	if event.action == "pressed" and event.direction == "left":
		print("Joystick left pressed")
		current_station = station_picker("left")
		sense.set_pixels(station_map(current_station[0]))						# Displays station map for selected station
	if event.action == "held":
		is_held = True
	elif event.action == "released":
		print("Joystick left released")
		
	
def joystick_right(event):	# Cycles station to the next one in the list
	
	global current_station
	global is_held
	
	if event.action == "pressed" and event.direction == "right":
		print("Joystick right pressed")
		current_station = station_picker("right")
		sense.set_pixels(station_map(current_station[0]))						# Displays station map for selected station
	print("BLAH1")
	if event.action == "held":
		is_held = True
		print("BLAH2")
	elif event.action == "released":
		print("Joystick right released")
		

def joystick_middle(event):											#LATER, SET THIS TO EASY MODE STUFF
	global is_held
	sense.clear(0, 0, 255)
	if event.action == "held":
		is_held = True
		
'''----------------------------------------------------------------------------'''

# LOGIC
def run_logic_NS(current_station,which_direction):

	with urllib.request.urlopen("http://127.0.0.1:5000/by-id/" + current_station[1]) as url: #Pull info for chosen station
		MTAPI_JSON = json.loads(url.read().decode()) # Loads MTAPI_JSON as a dictionary
		global wts
		wts = []	# makes empty list called wts
		direction = MTAPI_JSON["data"][0][which_direction] #show all north/southbound trains for the station
		print("\n",current_station[0],":",which_direction, ":")
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
			print(str(route) + ': ' + str(wait_time) + 'm' + str(round((wait_time_mins - math.floor(wait_time_mins)) * 60)) + 's') # Prints train info line by line

# DISPLAY
def SenseHatDisplay():
	
	B = BLACK =  (  0,   0,   0)	# Background color (default BLACK)
	T = WHITE =  (255, 255, 255)	# Text color (default WHITE)
		
	# Figures out the wait time for the first train (Digits at the top of the screen)
	if len(wts) >= 1:	# Checks if there's a 2nd train wait time available	
		T = determine_text_color(0) # Figures out the color of the number/train line for first train
		first_wts = wts[0][1]		# Puts first train wait time into variable
		#	first [] is item in list, i.e. next arriving train in order of arrival
		#	second [] is route letter [0] / wait time [1]. LEAVE AT [1]
		ones_digit = ones(T,B,first_wts[-1])		# Gets last char in first_wts string
		if len(first_wts) > 1:					# If wait time is more than 1 digit (9 mins)
			tens_digit = ones(T,B,first_wts[-2])		# Gets second to last char in first_wts string
		else:
			tens_digit = ones(T,B,"empty")
	else:
		ones_digit = black_pixels()[0:20] # Sets ones_digit pixels to black
		tens_digit = black_pixels()[0:20] # Sets tens_digit pixels to black
		print("No first train information")
			
	# Figures out the wait time for the second train (upper binary line)
	if len(wts) >= 2:	# Checks if there's a 2nd train wait time available
		T = determine_text_color(1) # Figures out the color of the number/train line for second train
		wt_bin1 = dec_to_bin(wts[1][1])
		wt_bin1_pixels = wt_bin_to_pixels(T,B,wt_bin1)
	else:
		wt_bin1_pixels = black_pixels() # Sets all pixels to black
		print("No second train information")
	
	# Figures out the wait time for the third train (lower binary line)
	if len(wts) >= 3:	# Checks if there's a 3rd train wait time available
		T = determine_text_color(2) # Figures out the color of the number/train line for third train
		wt_bin2 = dec_to_bin(wts[2][1])
		wt_bin2_pixels = wt_bin_to_pixels(T,B,wt_bin2)
	else:
		wt_bin2_pixels = black_pixels() # Sets all pixels to black
		print("No third train information")

	#Sends the pixel information to the LED screen all together
	sense.set_pixels(
	tens_digit[0:4]   + ones_digit[0:4]   +		# Pixel Line 1		Train 1
	tens_digit[4:8]   + ones_digit[4:8]   +		# Pixel Line 2
	tens_digit[8:12]  + ones_digit[8:12]  +		# Pixel Line 3
	tens_digit[12:16] + ones_digit[12:16] +		# Pixel Line 4
	tens_digit[16:20] + ones_digit[16:20] +		# Pixel Line 5
	black_pixels()[0:8] + 						# Pixel Line 6			EMPTY LINE
	wt_bin1_pixels[0:8] +				 		# Pixel Line 7			Train 2 (Binary)
	wt_bin2_pixels[0:8]							# Pixel Line 8			Train 3 (Binary)
	)

	
def station_picker(right_or_left):
	
	global station_list
	global current_station
	global n

	if right_or_left == "right":
		if n < (len(station_list) - 1):				# If n is less than total number of stations (5) minus one to account for index
			n = n + 1
			current_station = station_list[n]
		else: 										# If n has reached the last station (index = 4)
			n = 0									# Reset n to 0
			current_station = station_list[n]
			
	elif right_or_left == "left":
		if n > 0:									# If n is greater zero
			n = n - 1
			current_station = station_list[n]
		else: 										# If n has reached zero
			n = (len(station_list) - 1)				# Reset n to total number of stations (5) minus one to account for index
			current_station = station_list[n]		
	else:
		pass
		
	return current_station

#MAIN
def main():
	global is_held
	is_held = False
	
	global which_direction
	which_direction = "N"	# Which direction do you want to check? ("N", "S", or "B") (North, South, Both) | "N" is default
	
	sense.stick.direction_up = joystick_up
	sense.stick.direction_down = joystick_down
	sense.stick.direction_left = joystick_left
	sense.stick.direction_right = joystick_right
	sense.stick.direction_middle = joystick_middle
	
	#current_station = station_picker(right_or_left)
	
	while True:
		try:
			if subprocess.call(['curl', '-l', 'http://127.0.0.1:5000']) == 0 and is_held == False:	#If connection is okay
				run_logic_NS(current_station,which_direction)						#Then run logic
				SenseHatDisplay()
				print("")
				time.sleep(1.5)
			elif is_held == True:
				is_held = False
				pass
			else:												#If any problem with the connection
				print("MTAPI Connection Error")
				error_pixels = MTAPIConnectionError()				#Display error
				sense.set_pixels(error_pixels)
				time.sleep(1)
				sense.clear(0, 0, 0)								#Flashes error if MTAPI is not running
				time.sleep(1)
			#sleep X seconds between running logic
			
		except (KeyboardInterrupt, SystemExit): #Allows for clearing SenseHat on keyboard interrupt exit
			sense.clear()
			print("\n\nKEYBOARD INTERRUPT EXIT\n")
			raise
			
#Runs Main Program:
main() 
