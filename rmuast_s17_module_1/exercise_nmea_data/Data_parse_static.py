# __authors__= ""
from __future__ import print_function #support for Pyhon 2.7 - comment out if you use python>2.7.
from exportkml import kmlclass
from matplotlib import pyplot as plt
import numpy as np


def convertLatLon(latitude, longitude):
    # Obtaine the degrees of latitude and longitude
    lat_degree = int(latitude // 100)
    lng_degree = int(longitude // 100)

    # Obtaine the minutes of latitude and longitude
    lat_mm_mmmm = latitude % 100
    lng_mm_mmmmm = longitude % 100

    # Convert to UTM format
    converted_latitude = lat_degree + (lat_mm_mmmm / 60)
    converted_longitude = lng_degree + (lng_mm_mmmmm / 60)

    return converted_latitude, converted_longitude


# Initiate class
kml = kmlclass()
# Create kml file to use with the gmaps api {begin(self, fname, name, desc, width)}
kml.begin('TestMap', 'First map', 'Trial map for drones coords', 2)
# Genarating section begining {trksegbegin(self, segname, segdesc, color, altitude)}
kml.trksegbegin('Blue Line', 'Test coords', 'blue', 'relativeToGround')

# read file without the newline characters
#line = [line.rstrip('\n') for line in open('nmea_trimble_gnss_eduquad_flight.txt', 'r')]
line = [line.rstrip('\n') for line in open('nmea_ublox_neo_24h_static.txt', 'r')]

hDOP = []
timeArray = []

for item in line:
    if item != "" and item != "---" and "$GPGGA"in item :
        item = item.split(',')
        if item[0]=="$GPGGA":
            # each item and its corresponding possition in the array
            identifier=item[0]
            time = item[1]
            latitude = item[2]
            latitudeDirection = item[3]
            longitude = item[4]
            longitudeDirection = item[5]
            satelitesTracked = item[7]
            horizontalDilution = item[8]
            altitude = item[9]
            heightGeoid = item[10]
            if latitude=="" or longitude=="" or time=="":
                continue
            hDOP.append(float(horizontalDilution))
            timeArray.append(float(time)/10000)
            converted_latitude, converted_longitude = convertLatLon(float(latitude), float(longitude))
            # Generating coordinate pairs {trkpt(self, lat, lon, ele)}
            kml.trkpt(converted_latitude, converted_longitude, float(altitude))


# basic output

print("Mean of HDOP = ",np.mean(hDOP),"\nstandard deviation of HDOP =", np.std(hDOP) )

print("time:", time[:2] + ":" + time[2:4] + ":" + time[4:], "\nlatitude:", latitude, "\nlongitude:", longitude, "\naltitude:", altitude, "\nHDOP:", horizontalDilution)
print("UMT Latitude:", converted_latitude, ", UMT Longitude:", converted_longitude)


plt.plot(timeArray,hDOP)
plt.ylabel('HDOP in meters')
plt.xlabel('time in hours')
plt.axis([-1, 24, 0, 20])
a=range(0,26,2)
plt.xticks(a,rotation=-20)
plt.annotate(xy=(1,15), s=( "Mean = %.3fm\nStandard deviation = %.3fm" %( np.mean(hDOP),np.std(hDOP)  ) ))
plt.show()

# End coordinate section {no args}
kml.trksegend()
# End and close file {no arguments}
kml.end()