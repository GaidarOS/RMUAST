#!/usr/bin/python
# -*- coding: utf-8 -*-

# NMEA data logger
# Copyright (c) 2015 Kjeld Jensen kjeld@mmmi.sdu.dk kj@kjen.dk

# This app saves data from a device outputting NMEA data to a CSV formatted file.
# The app terminates when CTRL-C is pressed.

# parameters
serDev = '/dev/ttyUSB0'
baudRate = 115200
#baudRate = 57600
fileName = 'nmea_data_student.txt'

# import external libraries
import signal
import time 
import serial

# variables
stopFlag = 0

# define ctrl-c handler
def signal_handler(signal, frame):
	global stopFlag
	stopFlag = True	
	print '\nCtrl-C pressed'
    
# install ctrl-c handler
signal.signal(signal.SIGINT, signal_handler)

# configure and open serial device
print 'Opening the serial device: '+serDev
try :
	ser = serial.Serial(serDev, baudRate, timeout=10)
except Exception as e:
	stopFlag = 1
	print 'Error: Unable to open the serial device!'
	exit()
	pass

# if serial device opened correctly
if stopFlag == 0:
	print 'Press CTRL-C to quit'
	f = open(fileName, 'w')
 
	# loop until ctrl-c
	while stopFlag == 0:
		s = ser.readline()
		if s[0] == '$':
			f.write ('%f,%s' % (time.time(), s))

	# close file and serial device
	f.close()
	ser.close()
	

