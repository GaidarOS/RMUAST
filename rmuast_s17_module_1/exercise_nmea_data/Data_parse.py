# __authors__= ""
from exportkml import kmlclass


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


nmea_data = open('nmea_trimble_gnss_eduquad_flight.txt', 'r')

line = nmea_data.readlines(1)
items = line[1].split(',')
# each item and its corresponding possition in the array
time = items[1]
latitude = items[2]
latitudeDirection = items[3]
longitude = items[4]
longitudeDirection = items[5]
satelitesTracked = items[7]
horizontalDilution = items[8]
altitude = items[9]
heightGeoid = items[10]

print(len(line))
print(items, '\n')
# basic output
print("time:", time[:2] + ":" + time[2:4] + ":" + time[4:], "\nlatitude:", latitude, "\nlongitude:", longitude, "\naltitude:", altitude)
converted_latitude, converted_longitude = convertLatLon(float(latitude), float(longitude))
print(converted_latitude, converted_longitude)

# Initiate class
kml = kmlclass()
# Create kml file to use with the gmaps api {begin(self, fname, name, desc, width)}
kml.begin('TestMap', 'First map', 'Trial map for drones coords', 2)
# Genarating section begining {trksegbegin(self, segname, segdesc, color, altitude)}
kml.trksegbegin('Blue Line', 'Test coords', 'blue', 'relative')
# Generating coordinate pairs {trkpt(self, lat, lon, ele)}
kml.trkpt(converted_latitude, converted_longitude, float(altitude))
# End coordinate section {no args}
kml.trksegend()
# End and close file {no arguments}
kml.end()
