#!/usr/bin/python3.5


class NmeaRead():

    def __init__(self, filename=None):
        self.filename = filename

    def convertLatLon(self, latitude, longitude):
        """Converts latitude and longitude from a UTM to
        Geodetic format"""

        # Obtain the degrees of latitude and longitude
        lat_degree = int(latitude // 100)
        lng_degree = int(longitude // 100)

        # Obtain the minutes of latitude and longitude
        lat_mm_mmmm = latitude % 100
        lng_mm_mmmmm = longitude % 100

        # Convert to Decimal Degrees format
        converted_latitude = lat_degree + (lat_mm_mmmm / 60)
        converted_longitude = lng_degree + (lng_mm_mmmmm / 60)

        return converted_latitude, converted_longitude

    def NmeaDataParce(self, filename):
        """Parce Nmea data file in GPGGA format
        Params
        @Input: filename type(txt) file of nmea GPGGA
        @Outputs: type(list) for every item of the output
            Latitude
            Longitude
            Altitude
            Amount of sattelites tracked
            TimeStamps(nmea time * 10000)"""
        altitudeList = []
        satelliteList = []
        timeList = []
        convLat = []
        convLng = []

        # read file without the newline characters
        self.line = [line.rstrip('\n') for line in open(filename, 'r')]
        for item in self.line:
            if item != "" and item != "---":
                item = item.split(',')
                # each item and its corresponding possition in the array
                # latitudeDirection = item[3]
                # longitudeDirection = item[5]
                # horizontalDilution = item[8]
                # heightGeoid = item[10]
                time = item[1]
                latitude = item[2]
                longitude = item[4]
                satellitesTracked = item[7]
                altitude = item[9]
                converted_latitude, converted_longitude = self.convertLatLon(float(latitude), float(longitude))
                convLat.append(converted_latitude)
                convLng.append(converted_longitude)
                altitudeList.append(float(altitude))
                satelliteList.append(float(satellitesTracked))
                timeList.append(float(time) / 10000)
        return convLat, convLng, altitudeList, satelliteList, timeList
