import sys
import math
from datetime import datetime, date

T = int(sys.argv[1])
gr = int(sys.argv[2])
fname = sys.argv[3]

f = open("trip_data_1/splitRHSvertices_" + fname + ".csv", "r").readlines()

size_v = 0
for line in f:
    size_v += 1 

times = dict()
for line in f:
    vals = line.split(",")
    times[vals[1]] = [0 for t in xrange(T)]

num_times = dict()
max_times = dict()
f = open("trip_data_1/statistics_" +  fname + ".csv", "r").readlines()
for line in f:
    vals = line.split(",")
    num_times[vals[0]] = 0
    max_times[vals[0]] = math.ceil(float(vals[1].split("\n")[0]))

for i in range(1, 32):
    f = open("trip_data_1/trip_data_1_" + str(i) + ".csv", "r")

    dict.fromkeys(num_times, 0)

    for line in f:
        vals = line.split(",")
        start_long = str( math.floor(gr*float(vals[-4])))
        start_lat = str(math.floor(gr*float(vals[-3])))
        end_long = str(math.floor(gr*float(vals[-2])))
        end_lat = str(math.floor(gr*float(vals[-1].split("\n")[0])))

        type_v = start_long +";" + start_lat + ";" +end_long + ";" + end_lat
        ap_time = datetime.strptime(vals[5], "%Y-%m-%d %H:%M:%S").time()
        time_in_seconds = (datetime.combine(date.today(),ap_time) - datetime.combine(date.today(), ap_time.replace(hour=0, minute=0,second=0))).total_seconds()
        num_times[type_v]+=1
        ac_type_v = type_v + ";" + str(int(num_times[type_v]%max_times[type_v] + 1))
        times[ac_type_v][int(time_in_seconds)/300+1] += 1

f = open("trip_data_1/RHSarrivals_" + fname + ".csv", "w+")

for key, value in times.iteritems():
    count = 1
    for val in value:
        f.write(key + "," + str(count) + "," + str(val/31.0) + "\n")
        count += 1
f.close()
