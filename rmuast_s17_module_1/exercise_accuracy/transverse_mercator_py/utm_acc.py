from utm import utmconv
from math import cos, asin, sin, sqrt

uc = utmconv()

lat1 = 55.3668341
lng1 = 10.4305614

lat2 = 55.3758331
lng2 = 10.4305561


d = 2*asin(sqrt((sin((lat1-lat2)/2)) ** 2 + cos(lat1)*cos(lat2) * (sin((lng1 - lng2)/2)) ** 2))
print d*100


# convert from geodetic to UTM
(hemisphere, zone, letter, easting, northing) = uc.geodetic_to_utm(lat1, lng1)
print '\nConverted from geodetic to UTM [m]'
print '  %d %c %.5fe %.5fn' % (zone, letter, easting, northing)




