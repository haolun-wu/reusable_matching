import math
from datetime import datetime, date
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
gr = 15
vert = "-1110.0;611.0;-1110.0;611.0"

times = dict()
for i in range(1,289):
    times[i] = 0

for i in range(1, 32):
    f = open("trip_data_1/trip_data_1_" + str(i) + ".csv", "r")

    for line in f:
        vals = line.split(",")
        start_long = str( math.floor(gr*float(vals[-4])))
        start_lat = str(math.floor(gr*float(vals[-3])))
        end_long = str(math.floor(gr*float(vals[-2])))
        end_lat = str(math.floor(gr*float(vals[-1].split("\n")[0])))

        type_v = start_long +";" + start_lat + ";" +end_long + ";" + end_lat
        if type_v != vert:
            continue

        ap_time = datetime.strptime(vals[5], "%Y-%m-%d %H:%M:%S").time()
        print type(ap_time)
        print type(ap_time.replace(hour=0, minute=0,second=0))
        time_in_seconds = (datetime.combine(date.today(),ap_time) - datetime.combine(date.today(), ap_time.replace(hour=0, minute=0,second=0))).total_seconds()
        times[int(time_in_seconds)/300+1] += 1
x = list()
y = list()
for key, value in times.iteritems():
    x.append(key)
    y.append(value)

t = np.array(x)
s = np.array(y)
plt.plot(t, s)

plt.xlabel('time-step')
plt.ylabel('Number of requests')
plt.savefig(vert + '_figure.png')
print "Done"
