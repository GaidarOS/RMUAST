#!/usr/bin/python
# -*- coding: utf-8 -*-

# import libraries
# import time
# import datetime as dt
from math import pi, sqrt, atan2
import matplotlib.pyplot as plt
# import matplotlib.dates as mdates

# IMU exercise
# Copyright (c) 2015-2017 Kjeld Jensen kjen@mmmi.sdu.dk kj@kjen.dk

# Insert initialize code below ###################

fileName = 'imu_razor_data_pitch_45deg.txt'

# IMU type
# imuType = 'vectornav_vn100'
imuType = 'sparkfun_razor'

# Variables for plotting ##
showPlot = True
plotData = []
timestamp = []
# Initialize your variables here ##
myValue = 0.0

######################################################

# open the imu data file
f = open(fileName, "r")

# initialize variables
count = 0

# looping through file

for line in f:
    count += 1

    # split the line into CSV formatted data
    line = line.replace('*', ',')  # make the checkum another csv value
    csv = line.split(',')

    # keep track of the timestamps
    ts_recv = float(csv[0])
    if count == 1:
        ts_now = ts_recv  # only the first time
    ts_prev = ts_now
    ts_now = ts_recv

    if imuType == 'sparkfun_razor':
        # import data from a SparkFun Razor IMU (SDU firmware)
        acc_x = int(csv[2]) / 1000.0 * 4 * 9.82
        acc_y = int(csv[3]) / 1000.0 * 4 * 9.82
        acc_z = int(csv[4]) / 1000.0 * 4 * 9.82
        gyro_x = int(csv[5]) * 1 / 14.375 * pi / 180.0
        gyro_y = int(csv[6]) * 1 / 14.375 * pi / 180.0
        gyro_z = int(csv[7]) * 1 / 14.375 * pi / 180.0

    elif imuType == 'vectornav_vn100':
        # import data from a VectorNav VN-100 configured to output $VNQMR
        acc_x = float(csv[9])
        acc_y = float(csv[10])
        acc_z = float(csv[11])
        gyro_x = float(csv[12])
        gyro_y = float(csv[13])
        gyro_z = float(csv[14])

    # Insert loop code below #########################

    # Variables available
    # ----------------------------------------------------
    # count		Current number of updates
    # ts_prev	Time stamp at the previous update
    # ts_now	Time stamp at this update
    # acc_x		Acceleration measured along the x axis
    # acc_y		Acceleration measured along the y axis
    # acc_z		Acceleration measured along the z axis
    # gyro_x	Angular velocity measured about the x axis
    # gyro_y	Angular velocity measured about the y axis
    # gyro_z	Angular velocity measured about the z axis

    # 4.1.1
    myValue = atan2(acc_y, sqrt(acc_x**2 + acc_z**2))
    # timestamp.append(dt.datetime.strptime(time.strftime("%H%M%S", time.gmtime(ts_now)), "%H%M%S"))
    plotData.append(myValue * 180.0 / pi)
    ######################################################

# show the plot
if showPlot:
    plt.plot(plotData, color="b")
    plt.title("Pitch angle")
    plt.ylabel("Angle")
    plt.xlabel("Time")
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.savefig('imu_exercise_4.1.1_plot.png')
    plt.show()
