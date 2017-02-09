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
from math import cos, asin, sin, sqrt

# instantiate utmconv class
uc = utmconv()

# define test variables. Google maps says this is corresponds to 1 km.
lat1 = 55.3668341
lon1 = 10.4305614
lat2 = 55.3758331
lon2 = 10.4305561


# param lat1, lon1, lat2, lon2
def measure_distance_lon_lat(lat1, lon1, lat2, lon2):
    d = 2*asin(sqrt((sin((lat1 - lat2) / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin((lon1 - lon2) / 2)) ** 2))
    return d * 100


def measure_distance_utm(lat1, lon1, lat2, lon2):
    (h1, z1, l1, e1, n1) = uc.geodetic_to_utm(lat1, lon1)
    (h2, z2, l2, e2, n2) = uc.geodetic_to_utm(lat2, lon2)
    return sqrt((n1 - n2) ** 2 + (e1 - e2) ** 2) / 1000

print "Measuring difference of distance from longitude and latitude to UTM"
print "Test longitude and latitude:"
print " longitude1: %.9f" % lat1
print " latitude1:  %.9f" % lon1
print " lontitude2: %.9f" % lat2
print " latitude2:  %.9f" % lon2
print "\nDistance for longitude, latitude:"
print " in km: %.9f" % measure_distance_lon_lat(lat1, lon1, lat2, lon2)
print "Distance for utm:"
print " in km: %.9f" % measure_distance_utm(lat1, lon1, lat2, lon2)

