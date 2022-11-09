import random
import math
import sys
import numpy as np

gr = float(sys.argv[1])
fname = sys.argv[2]

gf = open("trip_data_1/statistics_" + fname + ".csv", "w+")
lf = open("trip_data_1/LHSlocations_" + fname + ".csv","w+")
lwf = open("trip_data_1/LHSreappearMeans_" + fname + ".csv","w+")

#Getting the 12 random "train" files
j = range(1,32)
random.shuffle(j)
j = j[1:13]


#Computing the rates
g = dict()
f = open("trip_data_1/RHSvertices_" + fname + ".csv", "r")

for line in f:
    vals = line.split(",")
    key =  vals[1].split("\n")[0]
    g[key] = 1
f.close()

total = 0
for i in j:
    f = open("trip_data_1/trip_data_1_" + str(i) + ".csv", "r")
    for line in f:
        vals = line.split(",")
        key =  str(math.floor(float(vals[-4])*gr)) + ";" + str(math.floor(gr*float(vals[-3]))) + ";" + str(math.floor(gr*float(vals[-2]))) + ";" + str(math.floor(gr*float(vals[-1].split("\n")[0]))) 
        g[key] += 1
        total+=1
    f.close()
for key, value in g.iteritems():
    gf.write(key + "," + str(value/13.0) + "\n")
gf.close()

#Computing the average loation of every car. Used to calculate the mean weight
glat = dict()
glong = dict()
galpha = 0
total = 0
cnt = dict()
f = open("trip_data_1/LHSvertices_" + fname + ".csv", "r")
for line in f:
    vals = line.split(",")
    key =  vals[1].split("\n")[0]
    cnt[key] = 1.0
    glat[key] = 40
    glong[key] = -73
f.close()

for i in j:
    f = open("trip_data_1/trip_data_1_" + str(i) + ".csv", "r")
    for line in f:
        vals = line.split(",")
        key = vals[1]
        cnt[key]+=1.0
        value =  float(vals[-3])
        glat[key] += value
        value =  float(vals[-4])
        glong[key] +=value
        value = float(vals[8])
        if value == 0:
            value = 300.0
        galpha += np.log(value/300.0)
        total+=1
    f.close()
for key, value in glat.iteritems():
    lf.write(key + "," + str(math.floor(gr*glong[key]/cnt[key])) + ";" + str(math.floor(gr*value/cnt[key])) +   "\n")
    lwf.write(key + "," + str(1+total*(galpha)**(-1))  +  "\n")
lf.close()
lwf.close()
