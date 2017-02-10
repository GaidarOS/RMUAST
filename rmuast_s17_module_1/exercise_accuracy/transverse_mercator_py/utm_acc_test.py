#!/usr/bin/env python
# *****************************************************************************
# UTM projection conversion test
# Copyright (c) 2013-2016, Kjeld Jensen <kjeld@frobomind.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# *****************************************************************************

# import utmconv class
from utm import utmconv
from math import cos, asin, sin, sqrt, pi

# instantiate utmconv class
uc = utmconv()

# define test variables. Google maps says this is corresponds to 1 km.
test_lat = 55.3668341
test_lon = 10.4305614

print '\nStart location [deg]'
print '  latitude:  %.10f' % test_lat
print '  longitude: %.10f' % test_lon


# param lat1, lon1, lat2, lon2
def measure_distance_lon_lat(lat1, lon1, lat2, lon2):
    d = 2*asin(sqrt((sin((lat1 - lat2) / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin((lon1 - lon2) / 2)) ** 2))
    return d * 100


def measure_distance_utm(n1, e1, n2, e2):
    return sqrt((n1 - n2) ** 2 + (e1 - e2) ** 2) / 1000


# convert from geodetic to UTM
(hemisphere, zone, letter, easting, northing) = uc.geodetic_to_utm(test_lat, test_lon)
print '\nConverted from geodetic to UTM [m]'
print '  %d %c %.5fe %.5fn' % (zone, letter, easting, northing)

# add 1 km to the distance, by adding 1000 to the value of northing
northing2 = northing + 1000
print '\nAdded 1km to the northing'
print '  %d %c %.5fe %.5fn' % (zone, letter, easting, northing2)

# convert back from UTM to geodetic
(lat, lon) = uc.utm_to_geodetic(hemisphere, zone, easting, northing2)
print '\nConverted back from UTM to geodetic [deg]:'
print '  latitude:  %.10f' % lat
print '  longitude: %.10f' % lon

# calculate distance for UTM and GCD
print '\nCalculating distance between points [deg] and [m]'
print '  Distance in km [deg]: %.10f' % measure_distance_lon_lat(test_lat, test_lon, lat, lon)
print '  Distance in km [m]:   %.10f' % measure_distance_utm(northing, easting, northing2, easting)

# determine conversion position error [m]
lat_err = abs(lat-test_lat)
lon_err = abs(lon-test_lon)
earth_radius = 6378137.0  # [m]
lat_pos_err = lat_err/360.0 * 2*pi*earth_radius
lon_pos_err = lon_err/360.0 * 2*pi*(cos(lat)*earth_radius)
print '\nPositional error from the two conversions [m]:'
print '  latitude:  %.9f' % lat_pos_err
print '  longitude: %.9f' % lon_pos_err

