#!/usr/bin/python

from aqlogreader import AQLogReader
# from aqlogreader import utm

aql = AQLogReader.aqLogReader()
# aql.help()
aql.setLogFile("021-AQL.LOG")
# aql.printChannelNames()
data = aql.getData()
text = "latlon.txt"
f = open(text, "w")
for i in data:
    f.write(str(i) + "\n")
f.close()
