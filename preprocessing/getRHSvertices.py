import math
import sys


gr = float(sys.argv[1])
fname = sys.argv[2] 

g = open("trip_data_1/RHSvertices_" + fname + ".csv", "w+")
count = 1
types = set()

for i in range(1, 32):
    f = open("trip_data_1/trip_data_1_" + str(i) + ".csv", "r")

    for line in f:
        vals = line.split(",")
        l1 = float(vals[-4])
        l2 = float(vals[-3])
        l3 = float(vals[-2])
        l4 = float(vals[-1].split("\n")[0])

        key = str(math.floor(gr*l1)) + ";" + str(math.floor(gr*l2)) + ";" + str(math.floor(gr*l3)) + ";" + str(math.floor(gr*l4))
        if key not in types:
            types.add(key)
            g.write(str(count) + "," + key  + "\n")
            count += 1

