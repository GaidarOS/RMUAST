from aqlogreader import utm
from math import sqrt


gsm = utm.utmconv()
oldPath = []
threshold = 1
cpLat = []
cpLng = []

line = [line.rstrip('\n') for line in open('latlon.txt', 'r')]
for item in line:
    if item != "":
        item = item.split(',')
        # Lat: item[0][1:]
        # Lng: item[1]
        # Alt: item[2][:-1])
        # Euclidean distance for all 3 points
        print(item)
        if float(item[1]) != 0.0:
            oldPath.append(gsm.geodetic_to_utm(float(item[0][1:]), float(item[1])))


for i in range(len(oldPath)):
    print(gsm.utm_to_geodetic("N", 32, oldPath[i][3], oldPath[i][4]))