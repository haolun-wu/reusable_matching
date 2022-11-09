import math
import sys

fname = sys.argv[1]

l = open("trip_data_1/LHSlocations_" + fname + ".csv", "r").readlines()
glat = dict()
glong = dict()
for line in l:
    vals = line.split(",")
    key = vals[0]
    glat[key] = float(vals[1].split(";")[1])
    glong[key] = float(vals[1].split(";")[0].split("\n")[0])
    
print "Done pre-process"

f = open("trip_data_1/LHSvertices_" + fname + ".csv", "r").readlines()
g = open("trip_data_1/splitRHSvertices_" + fname + ".csv", "r").readlines()
h = open("trip_data_1/edgeWeights_" + fname + ".csv", "w+")

for line1 in f:
    wr = ""
    for line2 in g:
        vals = line2.split(",")[1]
        Lon_s = float(vals.split(";")[0])
        Lat_s = float(vals.split(";")[1])
        Lon_t = float(vals.split(";")[2])
        Lat_t = float(vals.split(";")[3])
        
        vals1 = line1.split(",")[1].split("\n")[0]

        Lat_c = glat[vals1] 
        Lon_c = glong[vals1] 
        
        weight = max(0, (Lat_s-Lat_t)**2 + (Lon_s - Lon_t)**2 -2*( (Lat_s-Lat_c)**2 + (Lon_s - Lon_c)**2 ) )
        wr += str(weight) + ","
    wr = wr[:-1]
    h.write(wr + "\n")

