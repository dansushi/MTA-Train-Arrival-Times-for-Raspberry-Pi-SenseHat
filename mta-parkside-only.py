#!/usr/bin/python
import sys
import math
from random import randint
import time
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


global variable

