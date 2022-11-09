import math
import datetime
import random

def timeExtrapolate(trip_time, start_long, start_lat, end_long, end_lat, carsLocation, endLocation ):
    car_long = float(carsLocation.split(";")[0])
    car_lat = float(carsLocation.split(";")[1].split("\n")[0])
    
    end_long = float(endLocation.split(";")[0])
    end_lat = float(endLocation.split(";")[1].split("\n")[0])
    
    dist = 300.0 + math.sqrt( (end_lat-car_lat)**2 + (end_long - car_long)**2 )
    dist2 = 300.0 + math.sqrt( (end_lat-start_lat)**2 + (end_long - start_long)**2 )

    return (dist2*trip_time)/dist

fname = "normal_and_pjt"
f= open("X_" + fname + ".csv", "r").readlines()

LHS = open("trip_data_1/LHSvertices_" + fname + ".csv", "r").readlines()
RHS = open("trip_data_1/splitRHSvertices_" + fname + ".csv", "r").readlines()

T = 615
size_u = 0
size_v = 0
gr = 15

print(len(LHS))
for line in LHS:
    size_u += 1

for line in RHS:
    size_v += 1
print(size_u, size_v)
Xopt = [[[0 for k in xrange(size_v)] for j in xrange(size_u)] for i in xrange(T)]

W = [[0 for i in xrange(size_v)] for j in xrange(size_u)]
print(len(W))
weights = open("trip_data_1/edgeWeights_" + fname + ".csv", "r").readlines()

cur_u = 0
for line in weights:
    vals = line.split(",")
    cur_v = 0
    for val in vals:
        W[cur_u][cur_v] = float( val.split("\n")[0] )
        cur_v += 1
    cur_u += 1

cur_T = 0
cur_u = 0
cur_v = 0
for line in f:
    Xopt[cur_T][cur_u][cur_v] = float( line.split(",")[0].split("\n")[0] )
    cur_v += 1
    if cur_v == size_v:
        cur_v = 0
        cur_u += 1

        if cur_u == size_u:
            cur_u = 0
            cur_T += 1

print("Loaded the LP values")
#Running the ALG on the test data starting from 13
g = open("trip_data_1/weightLPheuristic_" + fname + ".csv", "w+")
for test in range(1, 931):

    carsLocation = dict()
    f = open("trip_data_1/LHSlocations_" + fname + ".csv", "r")
    count = 0
    for line in f:
        vals = line.split(",")
        carsLocation[count] = vals[1].split("\n")[0]
        count+=1
    f.close()

    avCarsMap = dict()
    count = 0
    for line in LHS:
        vals = line.split(",")
        temp = dict()
        temp["flag"] = 1
        temp["lhs_num"] = count
        temp["start"] = datetime.datetime.now()
        temp["len"] = 0.0
        temp["end"] = datetime.datetime.now()
        avCarsMap[vals[1]] = temp
        count += 1



    num_times = dict()
    max_times = dict()

    f = open("trip_data_1/statistics_" + fname + ".csv", "r")

    for line in f:
        num_times[line.split(",")[0]] = 0
        max_times[line.split(",")[0]] = int( math.ceil( float(line.split(",")[1].split("\n")[0]) ) )
    f.close()

    #Get the RHS vertex number
    f = open("trip_data_1/splitRHSvertices_" + fname + ".csv", "r")
    rhs_num = dict()
    rhs_pv = dict()

    count = 0
    for line in f:
        vals = line.split(",") 
        rhs_num[vals[1]] = count
        rhs_pv[vals[1]] = float(vals[2].split("\n")[0])
        count += 1
    f.close()

    f = open("trip_data_1/trip_data_1_" + str(test%31 + 1) + ".csv", "r")
   
    cur_T = 0
    weightAlg = 0
    LPval = 0
    for line in f:
        vals = line.split(",")
        start_lat = math.floor(gr*float(vals[-3]))
        start_long = math.floor(gr*float(vals[-4]))
        end_lat = math.floor(gr*float(vals[-1].split("\n")[0]))
        end_long = math.floor(gr*float(vals[-2]))
       
        start_time = datetime.datetime.strptime(vals[5], "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(vals[6], "%Y-%m-%d %H:%M:%S")
        trip_time = int(vals[8]) 
        
        vert_type = str(start_long) + ";" + str(start_lat) + ";" + str(end_long) + ";" + str(end_lat)
        num_times[vert_type] += 1
        vert = vert_type + ";" + str((num_times[vert_type]%max_times[vert_type])+1)
        
        cur_v = rhs_num[vert]
        #p_v = float(rhs_pv[vert])/T
        p_v = 1.0/T
        #if p_v == 0:
        #    p_v = 0.001
        free_lhs = list()
        for key in avCarsMap:
            if avCarsMap[key]["flag"] == 1:
                free_lhs.append(avCarsMap[key]["lhs_num"])
            else:
                if (avCarsMap[key]["end"]-start_time).total_seconds() >= 0:
                    avCarsMap[key]["flag"] = 1
                    free_lhs.append(avCarsMap[key]["lhs_num"])
        r = random.uniform(0, 1)
        cur_sum = 0
        cur_u = -1
        
        total = 0
        for val in free_lhs:
            temp_u = Xopt[cur_T][val][cur_v]
            total += temp_u

        for val in free_lhs:
            temp_u = Xopt[cur_T][val][cur_v]
            if (r - cur_sum) <= temp_u/total:
                cur_u = val
                break
            cur_sum += temp_u/p_v
            
        if cur_u == -1:
            continue
        
        for key in avCarsMap:
            if avCarsMap[key]["lhs_num"] == cur_u:
                avCarsMap[key]["flag"] = 0
                avCarsMap[key]["start"] = start_time
                avCarsMap[key]["len"] = trip_time + timeExtrapolate(trip_time, start_long, start_lat, end_long, end_lat, carsLocation[cur_u], str(start_long) + ";" + str(start_lat)) + timeExtrapolate(trip_time, start_long, start_lat, end_long, end_lat, carsLocation[cur_u], str(end_long) + ";" + str(end_lat))
                avCarsMap[key]["end"] = start_time + datetime.timedelta(seconds=avCarsMap[key]["len"])
                weightAlg += W[cur_u][cur_v]
                #weightAlg+=1
        cur_T += 1
    g.write(str(weightAlg) + "\n")
    f.close()
