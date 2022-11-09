def validLat(a):
    if a>=38 and a<=42:
        return True
    raise Exception

def validLong(a):
    if a>=-75 and a<=-71:
        return True
    raise Exception

for i in range(1,2):
    f = open("trip_data_" + str(i) + "_refined.csv.sorted", "r")
    g = open("trip_data_" + str(i) + "_refined_4.csv.sorted", "w+")

    miniLat = 1000
    miniLong = 1000
    maxiLat = -1000
    maxiLong = -1000

    first = True
    for line in f:
        if first:
            first = False
            continue
        vals = line.split(",")
        try:
            validLat(float(vals[-1].split("\n")[0]))
            validLat(float(vals[-3].split("\n")[0]))
            validLong(float(vals[-2].split("\n")[0]))
            validLong(float(vals[-4].split("\n")[0]))
            g.write(line)
        except:
            continue
        miniLat = min(miniLat, float(vals[-1].split("\n")[0]))
        miniLong = min(miniLong, float(vals[-2].split("\n")[0]))
        miniLat = min(miniLat, float(vals[-3].split("\n")[0]))
        miniLong = min(miniLong, float(vals[-4].split("\n")[0]))

        maxiLat = max(maxiLat, float(vals[-1].split("\n")[0]))
        maxiLong = max(maxiLong, float(vals[-2].split("\n")[0]))
        maxiLat = max(maxiLat, float(vals[-3].split("\n")[0]))
        maxiLong = max(maxiLong, float(vals[-4].split("\n")[0]))
    print miniLat,maxiLat, miniLong, maxiLong
    
