# __authors__= ""

from __future__ import print_function  # support for Pyhon 2.7 - comment out if you use python>2.7.
from matplotlib import pyplot as plt
import numpy as np

# read file without the newline characters
line = [line.rstrip('\n') for line in open('nmea_ublox_neo_24h_static.txt', 'r')]

hDOP = []
timeArray = []

for item in line:
    if item != "" and item != "---" and "$GPGGA"in item:
        item = item.split(',')
        if item[0] == "$GPGGA":
            # each item and its corresponding possition in the array
            identifier = item[0]
            time = item[1]
            latitude = item[2]
            latitudeDirection = item[3]
            longitude = item[4]
            longitudeDirection = item[5]
            satelitesTracked = item[7]
            horizontalDilution = item[8]
            altitude = item[9]
            heightGeoid = item[10]
            if latitude == "" or longitude == "" or time == "":
                continue
            hDOP.append(float(horizontalDilution))
            timeArray.append(float(time) / 10000)
            print(horizontalDilution)

# Last output
print("Mean of HDOP = ", np.mean(hDOP), "\nstandard deviation of HDOP =", np.std(hDOP))
print("time:", time[:2] + ":" + time[2:4] + ":" + time[4:], "\nlatitude:", latitude, "\nlongitude:", longitude, "\naltitude:", altitude, "\nHDOP:", horizontalDilution)

plt.plot(timeArray, hDOP)
plt.ylabel('HDOP in meters')
plt.xlabel('time in hours')
plt.axis([-1, 24, 0, 20])
a = range(0, 26, 2)
plt.xticks(a, rotation=-20)
plt.annotate(xy=(1, 15), s=("Mean = %.3fm\nStandard deviation = %.3fm" % (np.mean(hDOP), np.std(hDOP))))
plt.show()
