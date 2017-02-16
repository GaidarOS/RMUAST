# __author__ = ""
import re
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.interpolate import spline
import numpy as np 

# Initiate variables
voltage = []
time = []
data = []
s = []
sTime = []

# read file without the newline characters
line = [line.rstrip('\n') for line in open('log-2016-01-14.txt', 'r')]

for item in line:
    if item != "" and item != "---":
        item = re.sub("\s+", ",", item.strip())
        item = item.split(',')
        voltage.append(item[11])
        time.append(int(float(item[4])))

for i in time:
    s.append(dt.datetime.strptime(str(i), "%H%M%S"))

for i in range(len(s)):
    sTime.append(s[i].time())

# ploting the discharge graph with raw values
plt.plot(s, voltage)
plt.title('Battery discarge graph')
plt.ylabel('Voltage')
plt.xlabel('Timestamp')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
# plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1)) # it can further space the timestamps
# plt.gcf().autofmt_xdate() # Autoformating of the dates could use it
plt.show()

time = np.array(time)
voltage = np.array(voltage)

xnew = np.linspace(time.min(), time.max(), 10)  # 300 represents number of points to make between T.min and T.max
print(xnew)

power_smooth = spline(time, voltage, xnew)

plt.plot(xnew, power_smooth)
plt.show()
"""
"""