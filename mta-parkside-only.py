#!/usr/bin/python
import signal
import sys
from sys import exit
import math
import time
import datetime
from datetime import timedelta
import subprocess
from dateutil import parser
from custom_led_displays import * # Import custom LED display functions from other file
import urllib.request, json 

from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(0)
sense.low_light = True
sense.clear()

''' -----------------------------
NYC MTA Subway Live Train Arrival Time Display for the Raspberry Pi's SenseHat

This is a personally customized script to display the live train arrival times
for the station near where I live, Parkside Ave on the Q line.
It would be pretty simple to take this and customize it for another location
by changing the station names in the station_list below.
(Also remember to change the maps in custom_led_displays.py)

NOTE: In order for this script to work,
you must also be running MTAPI from Jon Thornton:
https://github.com/jonthornton/MTAPI

Authored by Dan Schneider (2018)
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
global easy_mode
easy_mode = False						# Sets to advanced mode by default (Easy mode is off)

'''----------------------------------------------------------------------------'''
# MINI-FUNCTIONS:

# Converts MTA's Date and Time to class datetime in UTC for delta comparison)
def mta_datetime_converter(time):
	convert_from_str_to_UTC_datetime = parser.parse(time[:-6],) #[:-6] Removes the time-zone offset so that it plays nice with datetime.now	
	return convert_from_str_to_UTC_datetime

#Converts wt_dec from string to int, then to binary, without 0b at the front
def dec_to_bin(wt_dec): 
	wt_bin = bin(int(wt_dec))[2:] 
	return wt_bin

#flak
def NoTrainInfo(): 
	print("No train information available at the moment.")
	sense.set_pixels(NoTrainWaitTimeInfo1())	# Sets screen with "waiting for train info" display
	time.sleep(0.75)
	sense.set_pixels(NoTrainWaitTimeInfo2())	# Sets screen with "waiting for train info" display
	time.sleep(0.75)
	sense.set_pixels(NoTrainWaitTimeInfo3())	# Sets screen with "waiting for train info" display
	time.sleep(0.75)
	
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


# Figures out the color of the number/train line (tr is train number)
def determine_text_color(tr,wts):
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
	elif wts[tr][0] == "L" or wts[tr][0] == "S" or wts[tr][0] == "FS":
		return GRAY

# Helps the joystick left right function loop around to be able to select from any of the stations available
def station_picker(right_or_left):
	
	global station_list
	global current_station
	global n

	if right_or_left == "right":
		if n < (len(station_list) - 1):				# If n is less than total number of stations minus one to account for index
			n = n + 1
			current_station = station_list[n]
		else: 										# If n has reached the last station
			n = 0									# Reset n to 0
			current_station = station_list[n]
			
	elif right_or_left == "left":
		if n > 0:									# If n is greater zero
			n = n - 1
			current_station = station_list[n]
		else: 										# If n has reached zero
			n = (len(station_list) - 1)				# Reset n to total number of stations minus one to account for index
			current_station = station_list[n]		
	else:
		pass
		
	return current_station

		
'''----------------------------------------------------------------------------'''

# JOYSTICK FUNCTIONS

def joystick_up(event):

	global current_station
	global is_held
	global which_direction
	global easy_mode

	if event.action == "pressed" and event.direction == "up":
		if which_direction == "S":		# If up_press on South, change to Both
			if easy_mode == False:			# If advanced mode is on, go up to "Both" mode
				which_direction = "B"
			elif easy_mode == True:			# If easy mode is on, skip up to "N" mode
				which_direction = "N"
			sense.set_pixels(N_B_S_display(which_direction))						# Displays up, both, or down mode
		elif which_direction == "B":	# If up_press on Both, change to North
			which_direction = "N"
			sense.set_pixels(N_B_S_display(which_direction))						# Displays up, both, or down mode
		else:							# If up_press on North, keep at North
			which_direction == "N"
			sense.set_pixels(N_B_S_display(which_direction))						# Displays up, both, or down mode
	if event.action == "held":
		is_held = True
	elif event.action == "released":
		pass
		
def joystick_down(event):

	global current_station
	global is_held
	global which_direction
	global easy_mode
	
	if event.action == "pressed" and event.direction == "down":
		if which_direction == "N":		 # If down_press on North, change to Both
			if easy_mode == False:			# If advanced mode is on, go down to "Both" mode
				which_direction = "B"
			elif easy_mode == True:			# If easy mode is on, skip down to "S" mode
				which_direction = "S"
			sense.set_pixels(N_B_S_display(which_direction))						# Displays up, both, or down mode
		elif which_direction == "B":	# If down_press on Both, change to South
			which_direction = "S"
			sense.set_pixels(N_B_S_display(which_direction))						# Displays up, both, or down mode
		else:                       	# If down_press on South, keep at South
			which_direction == "S"
			sense.set_pixels(N_B_S_display(which_direction))						# Displays up, both, or down mode
	if event.action == "held":
		is_held = True
	elif event.action == "released":
		pass

def joystick_left(event):	# Cycles station to the previous one in the list

	global current_station
	global is_held
	
	if event.action == "pressed" and event.direction == "left":
		current_station = station_picker("left")
		sense.set_pixels(station_map(current_station[0]))						# Displays station map for selected station
	if event.action == "held":
		is_held = True
	elif event.action == "released":
		pass
		
	
def joystick_right(event):	# Cycles station to the next one in the list
	
	global current_station
	global is_held
	
	if event.action == "pressed" and event.direction == "right":
		current_station = station_picker("right")
		sense.set_pixels(station_map(current_station[0]))						# Displays station map for selected station
	if event.action == "held":
		is_held = True
	elif event.action == "released":
		pass
		

def joystick_middle(event):				#Toggles Easy Mode on/off
	global is_held
	global easy_mode
	global which_direction
	
	if event.action == "pressed" and event.direction == "middle":
		if easy_mode == False:
			easy_mode = True
			sense.set_pixels(EasyModeOn())
			if which_direction == "B":   	#If Direction is Both when easy mode turned on, default to N (Both not available in easy mode)
				which_direction = "N"
		elif easy_mode == True:
			easy_mode = False
			sense.set_pixels(EasyModeOff())
	if event.action == "held":
		is_held = True
	elif event.action == "released":
		pass
		
'''----------------------------------------------------------------------------'''

# LOGIC
def run_logic_NorS(current_station,which_direction):

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
				#Uses function to convert the MTA Date and Time string to class datetime in the -05:00 EST timezone
			wait_time_secs = timedelta.total_seconds(conv_time - datetime.datetime.now())
				# find delta/difference in seconds between conv_time and current timewait_time
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
	

def run_logic_Both(current_station,which_direction):
	global wts
	run_logic_NorS(current_station,"N")
	N_wts = wts
	run_logic_NorS(current_station,"S")
	S_wts = wts
	SenseHatDisplayBoth(N_wts,S_wts)
	
# DISPLAY

def SenseHatDisplayEasy(tr):
	B = BLACK =  (  0,   0,   0)	# Background color (default BLACK)
	W = WHITE =  (150, 150, 150)	# WHITE
	T =          (255, 255, 255)	# Text color (default WHITE)	
		
	# Figures out the wait time for the 1st train (Digits at the top of the screen)
	if len(wts) >= 1:	# Checks if there's a 1st train wait time available	
		T = determine_text_color(tr,wts) # Figures out the color of the number/train line for train 'tr'
		first_wts = wts[tr][1]		# Puts first train wait time into variable
		#	first [] is item in list, i.e. next arriving train in order of arrival
		#	second [] is route letter [0] / wait time [1]. LEAVE AT [1]
		ones_digit = ones(T,B,first_wts[-1])		# Gets last char in first_wts string
		if len(first_wts) > 1:					# If wait time is more than 1 digit (9 mins)
			tens_digit = ones(T,B,first_wts[-2])		# Gets second to last char in first_wts string
		else:
			tens_digit = ones(T,B,"empty")
	else: #If no train times available at all
		ones_digit = black_pixels()[0:20] # Sets ones_digit pixels to black
		tens_digit = black_pixels()[0:20] # Sets tens_digit pixels to black
		NoTrainInfo()

	if len(wts) == 0:		# If no train times available at all, then tr_pixel_lines is all black.
		tr_pixel_lines = [B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]
	elif tr == 0:
		tr_pixel_lines = [W, W, B, B, B, B, B, B, W, W, B, B, B, B, B, B]
	elif tr == 1:
		tr_pixel_lines = [B, B, W, W, B, B, B, B, B, B, W, W, B, B, B, B]
	elif tr == 2:
		tr_pixel_lines = [B, B, B, B, W, W, B, B, B, B, B, B, W, W, B, B]	
	elif tr == 3:
		tr_pixel_lines = [B, B, B, B, B, B, W, W, B, B, B, B, B, B, W, W]	
		
	#Sends the pixel information to the LED screen all together
	sense.set_pixels(
	tens_digit[0:4]   + ones_digit[0:4]   +		# Pixel Line 1			Current Train in easy mode
	tens_digit[4:8]   + ones_digit[4:8]   +		# Pixel Line 2
	tens_digit[8:12]  + ones_digit[8:12]  +		# Pixel Line 3
	tens_digit[12:16] + ones_digit[12:16] +		# Pixel Line 4
	tens_digit[16:20] + ones_digit[16:20] +		# Pixel Line 5
	black_pixels()[0:8] + 						# Pixel Line 6			EMPTY LINE
	tr_pixel_lines[0:8] +				 		# Pixel Line 7			Square indicating train number
	tr_pixel_lines[8:16]						# Pixel Line 8			Square indicating train number
	)
	
def SenseHatDisplayNorS():
	
	B = BLACK =  (  0,   0,   0)	# Background color (default BLACK)
	T = WHITE =  (255, 255, 255)	# Text color (default WHITE)
		
	# Figures out the wait time for the 1st train (Digits at the top of the screen)
	if len(wts) >= 1:	# Checks if there's a 1st train wait time available	
		T = determine_text_color(0,wts) # Figures out the color of the number/train line for 1st train
		first_wts = wts[0][1]		# Puts first train wait time into variable
		#	first [] is item in list, i.e. next arriving train in order of arrival
		#	second [] is route letter [0] / wait time [1]. LEAVE AT [1]
		ones_digit = ones(T,B,first_wts[-1])		# Gets last char in first_wts string
		if len(first_wts) > 1:					# If wait time is more than 1 digit (9 mins)
			tens_digit = ones(T,B,first_wts[-2])		# Gets second to last char in first_wts string
		else:
			tens_digit = ones(T,B,"empty")
	else: #If no train times available at all
		ones_digit = black_pixels()[0:20] # Sets ones_digit pixels to black
		tens_digit = black_pixels()[0:20] # Sets tens_digit pixels to black
		NoTrainInfo()
			
	# Figures out the wait time for the 2nd train (upper binary line)
	if len(wts) >= 2:	# Checks if there's a 2nd train wait time available
		T = determine_text_color(1,wts) # Figures out the color of the number/train line for 2nd train
		wt_bin1 = dec_to_bin(wts[1][1])
		wt_bin1_pixels = wt_bin_to_pixels(T,B,wt_bin1)
	else:
		wt_bin1_pixels = black_pixels() # Sets all pixels to black
	
	# Figures out the wait time for the 3rd train (lower binary line)
	if len(wts) >= 3:	# Checks if there's a 3rd train wait time available
		T = determine_text_color(2,wts) # Figures out the color of the number/train line for 3rd train
		wt_bin2 = dec_to_bin(wts[2][1])
		wt_bin2_pixels = wt_bin_to_pixels(T,B,wt_bin2)
	else:
		wt_bin2_pixels = black_pixels() # Sets all pixels to black

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

def SenseHatDisplayBoth(N_wts,S_wts):
	
	B = BLACK =  (  0,   0,   0)	# Background color (default BLACK)
	T = WHITE =  (255, 255, 255)	# Text color (default WHITE)
	
	#NORTHBOUND TRAINS
	
	# Figures out the wait time for the 1st Northbound train
	if len(N_wts) >= 1:	# Checks if there's a 1st train wait time available
		T = determine_text_color(0,N_wts) # Figures out the color of the number/train line for 1st train
		wts_n_bin1 = dec_to_bin(N_wts[0][1])
		wts_n_bin1_pixels = wt_bin_to_pixels(T,B,wts_n_bin1)
	else: #If no train times available at all
		wts_n_bin1_pixels = black_pixels()[0:8]		# Sets first row to black
		NoTrainInfo()

	# Figures out the wait time for the 2nd Northbound train
	if len(N_wts) >= 2:	# Checks if there's a 2nd train wait time available
		T = determine_text_color(1,N_wts) # Figures out the color of the number/train line for 2nd train
		wts_n_bin2 = dec_to_bin(N_wts[1][1])
		wts_n_bin2_pixels = wt_bin_to_pixels(T,B,wts_n_bin2)
	else:
		wts_n_bin2_pixels = black_pixels() # Sets all pixels to black
	
	# Figures out the wait time for the 3rd Northbound train
	if len(N_wts) >= 3:	# Checks if there's a 3rd train wait time available
		T = determine_text_color(2,N_wts) # Figures out the color of the number/train line for 3rd train
		wts_n_bin3 = dec_to_bin(N_wts[2][1])
		wts_n_bin3_pixels = wt_bin_to_pixels(T,B,wts_n_bin3)
	else:
		wts_n_bin3_pixels = black_pixels() # Sets all pixels to black


	#SOUTHBOUND TRAINS
	
	if len(S_wts) >= 1:	# Checks if there's a 1st train wait time available
		T = determine_text_color(0,S_wts) # Figures out the color of the number/train line for 1st train
		wts_s_bin1 = dec_to_bin(S_wts[0][1])
		wts_s_bin1_pixels = wt_bin_to_pixels(T,B,wts_s_bin1)
	else: #If no train times available at all
		wts_s_bin1_pixels = black_pixels()[0:8]		# Sets first row to black
		NoTrainInfo()

	# Figures out the wait time for the 2nd Northbound train
	if len(S_wts) >= 2:	# Checks if there's a 2nd train wait time available
		T = determine_text_color(1,S_wts) # Figures out the color of the number/train line for 2nd train
		wts_s_bin2 = dec_to_bin(S_wts[1][1])
		wts_s_bin2_pixels = wt_bin_to_pixels(T,B,wts_s_bin2)
	else:
		wts_s_bin2_pixels = black_pixels() # Sets all pixels to black
	
	# Figures out the wait time for the 3rd Northbound train
	if len(S_wts) >= 3:	# Checks if there's a 3rd train wait time available
		T = determine_text_color(2,S_wts) # Figures out the color of the number/train line for 3rd train
		wts_s_bin3 = dec_to_bin(S_wts[2][1])
		wts_s_bin3_pixels = wt_bin_to_pixels(T,B,wts_s_bin3)
	else:
		wts_s_bin3_pixels = black_pixels() # Sets all pixels to black
		
		
	#Sends the pixel information to the LED screen all together
	sense.set_pixels(
	wts_n_bin1_pixels[0:8] +						# Pixel Line 1		Northbound Train 1 (Binary)
	wts_n_bin2_pixels[0:8] +						# Pixel Line 2		Northbound Train 2 (Binary)
	wts_n_bin3_pixels[0:8] +						# Pixel Line 3		Northbound Train 3 (Binary)
	black_pixels()[0:8] +						# Pixel Line 4
	black_pixels()[0:8] +						# Pixel Line 5
	wts_s_bin1_pixels[0:8] + 						# Pixel Line 6		Southbound Train 1 (Binary)
	wts_s_bin2_pixels[0:8] +				 		# Pixel Line 7		Southbound Train 2 (Binary)
	wts_s_bin3_pixels[0:8]							# Pixel Line 8		Southbound Train 3 (Binary)
	)

	
#MAIN
def main():
	global is_held
	is_held = False
	
	global which_direction
	which_direction = "N"	# Which direction do you want to check? ("N", "S", or "B") (North, South, Both) | "N" is default
	tr = 0					# tr (Train) defaults to first in list (0)
	
	sense.stick.direction_up = joystick_up
	sense.stick.direction_down = joystick_down
	sense.stick.direction_left = joystick_left
	sense.stick.direction_right = joystick_right
	sense.stick.direction_middle = joystick_middle
	
	#current_station = station_picker(right_or_left)
	
	while True:
		try:
			if subprocess.call(['curl', '-s', 'http://127.0.0.1:5000', '-o' , '/dev/null']) == 0 and is_held == False:	#If connection is okay (code 0) and joystick isn't being held
				if easy_mode == False:	# If easy mode is off (Advanced on)
					if which_direction == "N" or which_direction == "S":
						run_logic_NorS(current_station,which_direction)					#Then run logic North or South
						SenseHatDisplayNorS()
					else:																#Else both
						run_logic_Both(current_station,which_direction)					#Then run logic Both
				elif easy_mode == True:	# If easy mode is on
					run_logic_NorS(current_station,which_direction)					#Then run logic North or South
					SenseHatDisplayEasy(tr)
					if tr < (len(wts) - 1):				# If tr hasn't yet reached the last train available
						tr = tr + 1						# Go to next train
					else: 								# If tr has reached the last train available
						tr = 0							# Reset tr to 0
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
			raise
			
#Runs Main Program:
main()
