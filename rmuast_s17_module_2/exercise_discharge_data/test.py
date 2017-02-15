# http://stackoverflow.com/questions/17452179/not-write-out-all-dates-on-an-axis-matplotlib
# http://stackoverflow.com/questions/1574088/plotting-time-in-python-with-matplotlib

import datetime as dt
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
x = []
d = dt.datetime(2013, 7, 4)
for i in range(30):
        d = d + dt.timedelta(days=1)
        x.append(d)

y = range(len(x))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
plt.bar(x, y, align='center')  # center the bars on their x-values
plt.title('DateLocator with interval=5')
plt.gcf().autofmt_xdate()
plt.show()
