import math
import sys

fname = sys.argv[1]


f = open("trip_data_1/statistics_" + fname + ".csv","r")
g = dict()

for line in f:
    vals = line.split(",")
    g[vals[0]] = float(vals[1].split("\n")[0])
f.close()

f = open("trip_data_1/RHSvertices_" + fname + ".csv", "r")
h = open("trip_data_1/splitRHSvertices_" + fname + ".csv", "w+")
    
for line in f:
    vals = line.split(",")
    num = g[vals[1].split("\n")[0]]
    if num <=1:
        h.write(vals[0] + "," + vals[1].split("\n")[0] + ";" + "1" +  "," + str(num) + "\n")
        continue
    else:
        for i in range(1, int(math.ceil(num))):
            h.write(vals[0] + "," + vals[1].split("\n")[0] + ";" + str(i) + ",1" + "\n")
        if num%1 == 0:
            h.write(vals[0] + "," + vals[1].split("\n")[0] + ";" + str(int(math.ceil(num))) + ", 1" + "\n")
        else:
            h.write(vals[0] + "," + vals[1].split("\n")[0] + ";" + str(int(math.ceil(num))) + "," + str(num%1) + "\n")
    

