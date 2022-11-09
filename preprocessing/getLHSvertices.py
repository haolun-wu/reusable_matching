import math
import sys

fname = sys.argv[1]
g = open("trip_data_1/LHSvertices_" + fname + ".csv", "w+")
count = 1
cars = set()

for i in range(1, 32):
    f = open("trip_data_1/trip_data_1_" + str(i) + ".csv", "r")
    
    for line in f:
        vals = line.split(",")
        #key = vals[1] + ";" + str(int(math.floor(10*float(vals[-4])))) + ";" + str(int(math.floor(10*float(vals[-3]))))
        key = vals[1]
        if key not in cars:
            cars.add(key)
            g.write(str(count) + "," + key  + "\n")
            count += 1
