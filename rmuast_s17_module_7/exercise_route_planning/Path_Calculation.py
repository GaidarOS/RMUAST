from aqlogreader import utm
from math import hypot
from export_kml import kmlclass


def CheckpointEstimation(oldPath, coords, threshold):
    cpLat = []
    cpLng = []
    corAlt = []
    # Loop for calculating the best checkpoint from the available gps coordinates
    for i in range(len(oldPath)):
        if i == 0:
            initLat = oldPath[i][3]
            initLng = oldPath[i][4]
            cpLat.append(oldPath[i][3])
            cpLng.append(oldPath[i][4])
            corAlt.append(coords[i][2])

        nextLat = oldPath[i][3] - initLat
        nextLng = oldPath[i][4] - initLng
        dstnc = hypot(nextLat, nextLng)
        # dstnc = sqrt(nextLat**2 + nextLng**2)
        if dstnc > threshold:
            corAlt.append(coords[i][2])
            initLat = oldPath[i][3]
            initLng = oldPath[i][4]
            cpLat.append(oldPath[i][3])
            cpLng.append(oldPath[i][4])
    print(len(cpLng))
    return cpLat, cpLng, corAlt


# Initiate classes
kml = kmlclass()
gsm = utm.utmconv()

# Initiate variables
threshold = 1  # Change this value to increase/decrease the amount of checkpoints
oldPath = []
newPath = []
coords = []

# Create kml file to use with the gmaps api {begin(self, fname, name, desc, width)}
kml.begin('TrackMap.kml', 'Track map', 'Track map for drone\'s coordinates', 2)
# Genarating section begining {trksegbegin(self, segname, segdesc, color, altitude)}
kml.trksegbegin('Blue Line', 'Track coords', 'blue', 'relativeToGround')

line = [line.rstrip('\n') for line in open('latlon.txt', 'r')]
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


# End coordinate section {no args}
kml.trksegend()

# Genarating section begining {trksegbegin(self, segname, segdesc, color, altitude)}
kml.trksegbegin('Red Line', 'Reduced Track coords', 'red', 'relativeToGround')

cpLat, cpLng, corAlt = CheckpointEstimation(oldPath, coords, threshold)
# print(len(cpLng))  # Uncomment to see the new total of points

for i in range(len(cpLat)):
    newPath.append([gsm.utm_to_geodetic("N", 32, cpLat[i], cpLng[i]), corAlt[i]])
    # Generating coordinate pairs {trkpt(self, lat, lon, ele)}
    kml.trkpt(newPath[i][0][0], newPath[i][0][1], newPath[i][1])

# End coordinate section {no args}
kml.trksegend()

# Genarating section begining {trksegbegin(self, segname, segdesc, color, altitude)}
kml.trksegbegin('Green Line', 'Further Reduced Track coords', 'green', 'relativeToGround')
cpLat, cpLng, corAlt = CheckpointEstimation(oldPath, coords, threshold=5)
# print(len(cpLng))  # Uncomment to see the new total of points

newPath = []
for i in range(len(cpLat)):
    newPath.append([gsm.utm_to_geodetic("N", 32, cpLat[i], cpLng[i]), corAlt[i]])
    # Generating coordinate pairs {trkpt(self, lat, lon, ele)}
    kml.trkpt(newPath[i][0][0], newPath[i][0][1], newPath[i][1])

# End coordinate section {no args}
kml.trksegend()

# End and close file {no arguments}
kml.end()
