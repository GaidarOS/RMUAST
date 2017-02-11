#!/usr/bin/python3.5
# __authors__= ""\
from __future__ import print_function  # support for Pyhon 2.7 - comment out if you use python>2.7.
from exportkml import kmlclass
from matplotlib import pyplot as plt


def convertLatLon(latitude, longitude):
    # Obtaine the degrees of latitude and longitude
    lat_degree = int(latitude // 100)
    lng_degree = int(longitude // 100)

    # Obtaine the minutes of latitude and longitude
    lat_mm_mmmm = latitude % 100
    lng_mm_mmmmm = longitude % 100

    # Convert to Decimal Degrees format
    converted_latitude = lat_degree + (lat_mm_mmmm / 60)
    converted_longitude = lng_degree + (lng_mm_mmmmm / 60)

    return converted_latitude, converted_longitude


# Initiate arrays
altitudeList = []
satelliteList = []
timeList = []
# Initiate class
kml = kmlclass()
# Create kml file to use with the gmaps api {begin(self, fname, name, desc, width)}
kml.begin('TrackMap', 'Track map', 'Track map for drone\'s coordinates', 2)
# Genarating section begining {trksegbegin(self, segname, segdesc, color, altitude)}
kml.trksegbegin('Blue Line', 'Track coords', 'blue', 'relativeToGround')

# read file without the newline characters
line = [line.rstrip('\n') for line in open('nmea_trimble_gnss_eduquad_flight.txt', 'r')]

for item in line:
    if item != "" and item != "---":
        item = item.split(',')

        # each item and its corresponding possition in the array
        time = item[1]
        latitude = item[2]
        latitudeDirection = item[3]
        longitude = item[4]
        longitudeDirection = item[5]
        satellitesTracked = item[7]
        horizontalDilution = item[8]
        altitude = item[9]
        heightGeoid = item[10]
        converted_latitude, converted_longitude = convertLatLon(float(latitude), float(longitude))
        altitudeList.append(float(altitude))
        satelliteList.append(float(satellitesTracked))
        timeList.append(float(time) / 10000)
        # Generating coordinate pairs {trkpt(self, lat, lon, ele)}
        kml.trkpt(converted_latitude, converted_longitude, float(altitude))

# End coordinate section {no args}
kml.trksegend()
# End and close file {no arguments}
kml.end()

# Plot to visualize the altitude change in respect to time
plt.plot(timeList, altitudeList)
plt.title('Altitude above Mean Sea Level')
plt.ylabel('Altitude in meters')
plt.xlabel('Timestamp')
plt.show()

# Plot to visualize the tracked satellites every time
plt.plot(timeList, satelliteList)
plt.title('Number of satellites tracked')
plt.ylabel('Satellites tracked')
plt.xlabel('Timestamp')
plt.show()
