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


# Initiate class
kml = kmlclass()
# Create kml file to use with the gmaps api {begin(self, fname, name, desc, width)}
kml.begin('TestMap', 'First map', 'Trial map for drones coords', 2)
# Genarating section begining {trksegbegin(self, segname, segdesc, color, altitude)}
kml.trksegbegin('Blue Line', 'Test coords', 'blue', 'relative')

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
        satelitesTracked = item[7]
        horizontalDilution = item[8]
        altitude = item[9]
        heightGeoid = item[10]
        converted_latitude, converted_longitude = convertLatLon(float(latitude), float(longitude))
        # Generating coordinate pairs {trkpt(self, lat, lon, ele)}
        kml.trkpt(converted_latitude, converted_longitude, float(altitude))

# basic output
print('Last Item:\n')
print("time:", time[:2] + ":" + time[2:4] + ":" + time[4:], "\nlatitude:", latitude, "\nlongitude:", longitude, "\naltitude:", altitude)
print("UMT Latitude:", converted_latitude, ", UMT Longitude:", converted_longitude)

# End coordinate section {no args}
kml.trksegend()
# End and close file {no arguments}
kml.end()
