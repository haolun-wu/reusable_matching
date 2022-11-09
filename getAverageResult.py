import math

fname = "normal_and_pjt"
basefile = "weightLPwithoutsimulation"
f = open("trip_data_1/" + basefile + "_" + fname + ".csv", "r").readlines()
g = open("trip_data_1/" + basefile + "average_" + fname + ".csv", "w+")

weight = dict()
count = 0
for line in f:
    val = float(line.split(",")[0].split("\n")[0])
    if count%31 not in weight:
        weight[count%31] = val
    else:
        weight[count%31] += val
    count = count + 1

total = count/31
for key, val in weight.iteritems():
    g.write(str(key) + "," + str(weight[key]/total) + "\n")  
g.close()
