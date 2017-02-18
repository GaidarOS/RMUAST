# __author__ = ""
# import necessary components
import re
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
# from scipy.interpolate import spline  # Need it again in case we want to smooth the curves

# Initiate variables
voltage = []
time = []
data = []
s = []
sTime = []

# read file without the newline characters
line = [line.rstrip('\n') for line in open('log-2016-01-14.txt', 'r')]
# Parsing data
for item in line:
    if item != "" and item != "---":
        item = re.sub("\s+", ",", item.strip())
        item = item.split(',')
        voltage.append(item[11])
        time.append(int(float(item[4])))
# Convert time in a datetime.datetime(HH:MM:SS) format
for i in time:
    s.append(dt.datetime.strptime(str(i), "%H%M%S"))

# ploting the discharge graph with raw values
plt.plot(s, voltage)
plt.title('Battery discarge graph')
plt.ylabel('Voltage(V)')
plt.xlabel('Time')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
# plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1)) # it can further space the timestamps
# plt.gcf().autofmt_xdate() # Autoformating of the dates could use it
plt.show()

# Generating a persentage range for the values available
soc = np.linspace(100, 10, len(voltage))

# Creating the ploting space
fig = plt.figure(1, (7, 4))
ax = fig.add_subplot(1, 1, 1)
ax.plot(voltage, soc)

fmt = '%.0f%%'  # Formating the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(xticks)
plt.gca().invert_xaxis()  # Inverting the x-axis values
plt.title('State of Charge graph')
plt.ylabel('SoC(%)')
plt.xlabel('Voltage(V)')
# function looks sort of the form of: y= e^(-x^2)-x
plt.show()


"""
# smooth the voltage graph
time = np.array(time)
voltage = np.array(voltage)

xnew = np.linspace(time.min(), time.max(), 10)  # 300 represents number of points to make between T.min and T.max
print(xnew)

power_smooth = spline(time, voltage, xnew)
plt.plot(xnew, power_smooth)
plt.show()
"""
