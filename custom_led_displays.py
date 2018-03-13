# LED SenseHat screen with "ER" for ERROR
def MTAPIConnectionError():
	g = (150, 0, 0) # Red
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

# LED SenseHat screen with "ER" for ERROR
def NoTrainWaitTimeInfo1():
	w = (10, 10, 10) # White
	b = (0, 0, 0) # Black
	error_pixels = [
		b, b, b, b, b, b, b, b,
		b, b, b, b, b, b, b, b,
		b, b, b, b, b, b, b, b,
		w, w, b, b, b, b, b, b,
		w, w, b, b, b, b, b, b,
		b, b, b, b, b, b, b, b,
		b, b, b, b, b, b, b, b,
		b, b, b, b, b, b, b, b,
	]
	return error_pixels
	
def NoTrainWaitTimeInfo2():
	w = (10, 10, 10) # White
	b = (0, 0, 0) # Black
	error_pixels = [
		b, b, b, b, b, b, b, b,
		b, b, b, b, b, b, b, b,
		b, b, b, b, b, b, b, b,
		w, w, b, w, w, b, b, b,
		w, w, b, w, w, b, b, b,
		b, b, b, b, b, b, b, b,
		b, b, b, b, b, b, b, b,
		b, b, b, b, b, b, b, b,
	]
	return error_pixels
	
def NoTrainWaitTimeInfo3():
	w = (10, 10, 10) # White
	b = (0, 0, 0) # Black
	error_pixels = [
		b, b, b, b, b, b, b, b,
		b, b, b, b, b, b, b, b,
		b, b, b, b, b, b, b, b,
		w, w, b, w, w, b, w, w,
		w, w, b, w, w, b, w, w,
		b, b, b, b, b, b, b, b,
		b, b, b, b, b, b, b, b,
		b, b, b, b, b, b, b, b,
	]
	return error_pixels

def N_B_S_display(N_B_S):
	
	#Colors     r    g    b
	b =		(  0,   0,   0) #BLACK BACKGROUND
	f =		(155, 155, 155) #FOREGROUND
		
	if N_B_S == "N":
		display = [
			b, b, b, b, f, b, b, b,
			b, b, b, f, f, f, b, b,
			b, b, f, f, f, f, f, b,
			b, f, f, f, f, f, f, f,
			b, b, b, f, f, f, b, b,
			b, b, b, f, f, f, b, b,
			b, b, b, f, f, f, b, b,
			b, b, b, f, f, f, b, b,
		]
		return display
	elif N_B_S == "B":
		display = [
			b, b, b, b, f, b, b, b,
			b, b, b, f, f, f, b, b,
			b, b, f, b, f, b, f, b,
			b, b, b, b, f, b, b, b,
			b, b, b, b, f, b, b, b,
			b, b, f, b, f, b, f, b,
			b, b, b, f, f, f, b, b,
			b, b, b, b, f, b, b, b,
		]
		return display
	elif N_B_S == "S":
		display = [
			b, b, b, f, f, f, b, b,
			b, b, b, f, f, f, b, b,
			b, b, b, f, f, f, b, b,
			b, b, b, f, f, f, b, b,
			b, f, f, f, f, f, f, f,
			b, b, f, f, f, f, f, b,
			b, b, b, f, f, f, b, b,
			b, b, b, b, f, b, b, b,
		]
		return display

def station_map(current_station):
	
	#Colors     r    g    b
	b =		(  0,   0,   0) #BLACK BACKGROUND
	a =		(  10, 10,  10) #GRAY
	w =		(255, 255, 255) #WHITE
	o =		(255,  10,   0) #ORANGE LINE
	y =		(255, 140,   0) #YELLOW LINE
	g =		(  0, 200,   0) #GREEN LINE
	r =		(255,   0,   0) #RED LINE
	v =		(255,   0, 200) #PURPLE
	s =		( 45, 172, 213) #STATION COLOR
		
	if current_station == "Parkside Ave":	#Make sure the station name is spelled right, exactly like in main file under station_list
		map = [
			b, b, o, y, b, b, g, r,
			b, b, o, y, b, b, g, r,
			b, b, o, y, b, b, g, r,
			b, b, s, s, b, b, g, r,
			b, o, s, s, b, b, g, r,
			b, o, y, b, b, b, g, r,
			o, y, b, b, b, b, g, r,
			o, y, b, b, b, b, g, r,
		]
		return map
	elif current_station == "Church Ave":	#Make sure the station name is spelled right, exactly like in main file under station_list
		map = [
			b, b, o, y, b, b, g, r,
			b, b, o, y, b, b, g, r,
			b, b, o, y, b, b, g, r,
			b, b, o, y, b, b, g, r,
			b, o, y, b, b, b, g, r,
			b, o, y, b, b, b, g, r,
			s, s, b, b, b, b, g, r,
			s, s, b, b, b, b, g, r,
		]
		return map
	elif current_station == "Prospect Park":	#Make sure the station name is spelled right, exactly like in main file under station_list
		map = [
			b, b, s, s, b, b, g, r,
			b, b, s, s, b, b, g, r,
			b, b, o, y, b, b, g, r,
			b, b, o, y, b, b, g, r,
			b, o, y, b, b, b, g, r,
			b, o, y, b, b, b, g, r,
			o, y, b, b, b, b, g, r,
			o, y, b, b, b, b, g, r,
		]
		return map
	elif current_station == "Winthrop St":	#Make sure the station name is spelled right, exactly like in main file under station_list
		map = [
			b, b, o, y, b, b, g, r,
			b, b, o, y, b, b, g, r,
			b, b, o, y, b, b, s, s,
			b, b, o, y, b, b, s, s,
			b, o, y, b, b, b, g, r,
			b, o, y, b, b, b, g, r,
			o, y, b, b, b, b, g, r,
			o, y, b, b, b, b, g, r,
		]
		return map
	elif current_station == "Times Square - 42nd St":	#Make sure the station name is spelled right, exactly like in main file under station_list
		map = [
			b, b, b, r, y, b, b, b,
			b, b, b, r, y, b, b, b,
			b, b, b, r, y, b, b, b,
			b, b, b, s, s, a, a, a,
			v, v, v, s, s, v, v, v,
			b, b, b, r, y, b, b, b,
			b, b, b, r, b, y, b, b,
			b, b, b, r, b, b, y, b,
		]
		return map
	else:									#This is the backup map if no station map is found for current_station
		map = [
			b, b, o, y, b, b, g, r,
			b, b, o, y, b, b, g, r,
			b, b, o, y, b, b, g, r,
			b, b, o, y, b, b, g, r,
			b, o, y, b, b, b, g, r,
			b, o, y, b, b, b, g, r,
			o, y, b, b, b, b, g, r,
			o, y, b, b, b, b, g, r,
		]
		return map

def ones(T,B,digit):
	if digit == "0":
		led_display = [
		B, T, T, T,
		B, T, B, T,
		B, T, B, T,
		B, T, B, T,
		B, T, T, T,
		]
		return led_display
	elif digit == "1":
		led_display = [
		B, B, T, B,
		B, B, T, B,
		B, B, T, B,
		B, B, T, B,
		B, B, T, B,
		]
		return led_display
	elif digit == "2":
		led_display = [
		B, T, T, T,
		B, B, B, T,
		B, T, T, T,
		B, T, B, B,
		B, T, T, T,
		]
		return led_display
	elif digit =="3":
		led_display = [
		B, T, T, T,
		B, B, B, T,
		B, T, T, T,
		B, B, B, T,
		B, T, T, T,
		]
		return led_display
	elif digit == "4":
		led_display = [
		B, T, B, T,
		B, T, B, T,
		B, T, T, T,
		B, B, B, T,
		B, B, B, T,
		]
		return led_display
	elif digit == "5":
		led_display = [
		B, T, T, T,
		B, T, B, B,
		B, T, T, T,
		B, B, B, T,
		B, T, T, T,
		]
		return led_display
	elif digit == "6":
		led_display = [
		B, T, T, T,
		B, T, B, B,
		B, T, T, T,
		B, T, B, T,
		B, T, T, T,
		]
		return led_display
	elif digit == "7":
		led_display = [
		B, T, T, T,
		B, B, B, T,
		B, B, B, T,
		B, B, B, T,
		B, B, B, T,
		]
		return led_display
	elif digit == "8":
		led_display = [
		B, T, T, T,
		B, T, B, T,
		B, T, T, T,
		B, T, B, T,
		B, T, T, T,
		]
		return led_display
	elif digit == "9":
		led_display = [
		B, T, T, T,
		B, T, B, T,
		B, T, T, T,
		B, B, B, T,
		B, T, T, T,
		]
		return led_display
	else:
		led_display = [
		B, B, B, B,
		B, B, B, B,
		B, B, B, B,
		B, B, B, B,
		B, B, B, B,
		]
		return led_display

def tens(T,B,digit):
	if digit == "0":
		led_display = [
		B, T, T, T,
		B, T, B, T,
		B, T, B, T,
		B, T, B, T,
		B, T, T, T,
		]
		return led_display
	elif digit == "1":
		led_display = [
		B, B, T, B,
		B, B, T, B,
		B, B, T, B,
		B, B, T, B,
		B, B, T, B,
		]
		return led_display
	elif digit == "2":
		led_display = [
		B, T, T, T,
		B, B, B, T,
		B, T, T, T,
		B, T, B, B,
		B, T, T, T,
		]
		return led_display
	elif digit =="3":
		led_display = [
		B, T, T, T,
		B, B, B, T,
		B, T, T, T,
		B, B, B, T,
		B, T, T, T,
		]
		return led_display
	elif digit == "4":
		led_display = [
		B, T, B, T,
		B, T, B, T,
		B, T, T, T,
		B, B, B, T,
		B, B, B, T,
		]
		return led_display
	elif digit == "5":
		led_display = [
		B, T, T, T,
		B, T, B, B,
		B, T, T, T,
		B, B, B, T,
		B, T, T, T,
		]
		return led_display
	elif digit == "6":
		led_display = [
		B, T, T, T,
		B, T, B, B,
		B, T, T, T,
		B, T, B, T,
		B, T, T, T,
		]
		return led_display
	elif digit == "7":
		led_display = [
		B, T, T, T,
		B, B, B, T,
		B, B, B, T,
		B, B, B, T,
		B, B, B, T,
		]
		return led_display
	elif digit == "8":
		led_display = [
		B, T, T, T,
		B, T, B, T,
		B, T, T, T,
		B, T, B, T,
		B, T, T, T,
		]
		return led_display
	elif digit == "9":
		led_display = [
		B, T, T, T,
		B, T, B, T,
		B, T, T, T,
		B, B, B, T,
		B, T, T, T,
		]
		return led_display
	else:
		led_display = [
		B, B, B, B,
		B, B, B, B,
		B, B, B, B,
		B, B, B, B,
		B, B, B, B,
		]
		return led_display

		
