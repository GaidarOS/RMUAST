from aqlogreader import utm
from math import sqrt


gsm = utm.utmconv()
oldPath = []
newPath = []
threshold = 1  # Change this value to increase/decrease the amount of checkpoints
cpLat = []
cpLng = []
coords = []

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
            coords.append([item[0][1:], item[1], item[2][:-1]])
            # Altidute: coords[i][2] for use outside of the "data parsing loop"


for i in range(len(oldPath)):
    if i == 0:
        initLat = oldPath[i][3]
        initLng = oldPath[i][4]
    nextLat = oldPath[i][3] - initLat
    nextLng = oldPath[i][4] - initLng
    dstnc = sqrt(nextLat**2 + nextLng**2)
    if dstnc > threshold:
        initLat = oldPath[i][3]
        initLng = oldPath[i][4]
        cpLat.append(oldPath[i][3])
        cpLng.append(oldPath[i][4])

# print("Latitude:", cpLat)
# print("Longitude:", cpLng)
# print(len(cpLng))

for i in range(len(cpLat)):
    newPath.append(gsm.utm_to_geodetic("N", 32, cpLat[i], cpLng[i]))
