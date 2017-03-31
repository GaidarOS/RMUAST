

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


def NmeaDataParse(filename):

    # Initiate arrays
    altitudeList = []
    satelliteList = []
    timeList = []
    convLat = []
    convLng = []
    # read file without the newline characters
    line = [line.rstrip('\n') for line in open(filename, 'r')]

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
            convLat.append(converted_latitude)
            convLng.append(converted_longitude)
            altitudeList.append(float(altitude))
            satelliteList.append(float(satellitesTracked))
            timeList.append(float(time) / 10000)
    return convLat, convLng, altitudeList, satelliteList, timeList
