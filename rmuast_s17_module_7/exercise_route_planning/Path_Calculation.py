from aqlogreader import utm
from math import hypot, sqrt
from export_kml import kmlclass
from aqlogreader import Nmea_Parse


def CheckpointEstimation(oldLat, oldLng, coords, threshold):
    cpLat = []
    cpLng = []
    corAlt = []
    # Loop for calculating the best checkpoint from the available gps coordinates
    for i in range(len(oldLat)):
        if i == 0:
            initLat = oldLat[i]
            initLng = oldLng[i]
            initAlt = coords[i]
            cpLat.append(oldLat[i])
            cpLng.append(oldLng[i])
            corAlt.append(coords[i])
        nextLat = oldLat[i] - initLat
        nextLng = oldLng[i] - initLng
        nextAlt = coords[i] - initAlt
        # Calculating the square root of the sum of squares of the distances
        dstnc = hypot(nextLat, nextLng)
        dstnc = hypot(dstnc, nextAlt)
        # dstn = sqrt(nextLng**2 + nextLng**2 + nextAlt**2)
        if dstnc >= threshold:
            initLat = oldLat[i]
            initLng = oldLng[i]
            initAlt = coords[i]
            cpLat.append(oldLat[i])
            cpLng.append(oldLng[i])
            corAlt.append(coords[i])
    print(len(cpLat))
    return cpLat, cpLng, corAlt


def ReadData(filename):
    oldPath = []
    coords = []
    oldLat = []
    oldLng = []
    oldAlt = []

    line = [line.rstrip('\n') for line in open(filename, 'r')]
    for item in line:
        if item != "":
            item = item.split(',')
            # Lat: item[0][1:]
            # Lng: item[1]
            # Alt: item[2][:-1])
            # Euclidean distance for all 3 points
            if float(item[1]) != 0.0:
                oldPath.append(gsm.geodetic_to_utm(float(item[0][1:]), float(item[1])))
                # coords.append("{}, {}, {}".format(item[0][1:], item[1], item[2][:-1]))
                coords.append([float(item[0][1:]), float(item[1]), float(item[2][:-1])])
                # Altitude: coords[i][2] for use outside of the "data parsing loop"
                kml.trkpt(float(item[0][1:]), float(item[1]), float(item[2][:-1]))

    # Seperate the data in individual  arrays
    for i in range(len(oldPath)):
        oldLat.append(float(oldPath[i][3]))
        oldLng.append(float(oldPath[i][4]))
        oldAlt.append(float(coords[i][2]))

    return oldLat, oldLng, oldAlt


# Initiate classes
kml = kmlclass()
gsm = utm.utmconv()
nmea = Nmea_Parse.NmeaRead()

# Initiate variables
threshold = 1  # Change this value to increase/decrease the amount of checkpoints
newPath = []

# ************* File Begins ****************
kml.begin('TrackMap.kml', 'Track map', 'Track map for drone\'s coordinates', 2)
# ************* Section One ****************
kml.trksegbegin('Blue Line', 'Track coords', 'blue', 'relativeToGround')
oldLat, oldLng, oldAlt = ReadData("latlon.txt")
kml.trksegend()
# ************* Section Ends ****************
# ************* Section Two ****************
kml.trksegbegin('Red Line', 'Reduced Track coords', 'red', 'relativeToGround')
cpLat, cpLng, corAlt = CheckpointEstimation(oldLat, oldLng, oldAlt, threshold)

for i in range(len(cpLat)):
    newPath.append([gsm.utm_to_geodetic("N", 32, cpLat[i], cpLng[i]), corAlt[i]])
    kml.trkpt(newPath[i][0][0], newPath[i][0][1], newPath[i][1])
kml.trksegend()
# ************* Section Ends ****************
# ************* Section Three ****************
kml.trksegbegin('Green Line', 'Further Reduced Track coords', 'green', 'relativeToGround')
cpLat, cpLng, corAlt = CheckpointEstimation(oldLat, oldLng, oldAlt, threshold=5)
newPath = []
for i in range(len(cpLat)):
    newPath.append([gsm.utm_to_geodetic("N", 32, cpLat[i], cpLng[i]), corAlt[i]])
    kml.trkpt(newPath[i][0][0], newPath[i][0][1], newPath[i][1])
kml.trksegend()
# ************* Section Ends ****************
kml.end()
# ************* File Ends ****************


# ***************************************************************************
# Reading Nmea data
lat, lng, alt, sat, time = nmea.NmeaDataParce("nmea_trimble_gnss_eduquad_flight.txt")
print(len(lat))
# ************* File Begins ****************
kml.begin('TrackMapNmea.kml', 'Track map', 'Track map for drone\'s coordinates', 2)
# ************* Section One ****************
kml.trksegbegin('Blue Line', 'Track coords', 'blue', 'relativeToGround')
for i in range(len(lat)):
    kml.trkpt(lat[i], lng[i], alt[i])
kml.trksegend()
# ************* Section Ends ****************
# ************* Section Two  ****************
kml.trksegbegin('Red Line', 'Track coords', 'red', 'relativeToGround')
cpLat, cpLng, corAlt = CheckpointEstimation(lat, lng, alt, threshold=0.3)

for i in range(len(cpLat)):
    kml.trkpt(cpLat[i], cpLng[i], corAlt[i])
kml.trksegend()
# ************* Section Ends ****************
kml.end()
# ************* File Ends ****************
