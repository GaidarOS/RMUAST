# __author__ = ""
import re
import matplotlib.pyplot as plt
import datetime as dt

# Initiate arrays
voltage = []
time = []
data = []
s = []
i = 0
# read file without the newline characters
line = [line.rstrip('\n') for line in open('log-2016-01-14.txt', 'r')]

for item in line:
    if item != "" and item != "---":
        item = re.sub("\s+", ",", item.strip())
        item = item.split(',')
        voltage.append(item[11])
        time.append(int(float(item[4])))
        i += 1
        data.append(i)

for i in time:
    # temp = dt.datetime.strptime(str(i), "%H%M%S")
    # s.append(temp.strftime("%Y-%m-%d, %H:%M:%S"))
    s.append(dt.datetime.strptime(str(i), "%H%M%S"))
x = [dt.datetime.now() + dt.timedelta(hours=i) for i in range(12)]

print(s)
# dic = {"voltage": voltage, "time": s}

plt.plot(s, voltage)
# plt.xticks(range(0, len(s), 500), range(0, len(s), 500))
plt.gcf().autofmt_xdate()
plt.show()
