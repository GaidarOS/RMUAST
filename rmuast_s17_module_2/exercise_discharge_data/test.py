# http://stackoverflow.com/questions/17452179/not-write-out-all-dates-on-an-axis-matplotlib
# http://stackoverflow.com/questions/1574088/plotting-time-in-python-with-matplotlib
"""
import datetime as dt
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
x = []
d = dt.datetime(2013, 7, 4)
for i in range(30):
        d = d + dt.timedelta(hours=2)
        x.append(d)

print(x)

y = range(len(x))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.bar(x, y, align='center')  # center the bars on their x-values
plt.title('DateLocator with interval=5')
plt.gcf().autofmt_xdate()
plt.show()
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline


T = np.array([6, 7, 8, 9, 10, 11, 12])
power = np.array([1.53E+03, 5.92E+02, 2.04E+02, 7.24E+01, 2.72E+01, 1.10E+01, 4.70E+00])

xnew = np.linspace(T.min(),T.max(),300) #300 represents number of points to make between T.min and T.max

power_smooth = spline(T,power,xnew)

plt.plot(xnew,power_smooth)
plt.show()
