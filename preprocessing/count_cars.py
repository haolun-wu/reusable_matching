import random

f = open("trip_data_1_refined_4.csv.sorted", "r")
g = open("selectedCars_1.csv", "w+")

count = 0
licenses = set()

for line in f:
    vals = line.split(",")
    licenses.add(vals[1])

cars = []
for l in licenses:
    cars.append(l)

random.shuffle(cars)

count = 0
for car in cars:
    g.write(car + "\n")
    count += 1
    if count >= 30:
        break        

