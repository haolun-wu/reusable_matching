from cvxopt import matrix, solvers, spmatrix
from cvxopt.modeling import variable, op, dot
from scipy.stats import norm
import numpy as np
import ecos
import math
import sys

fname = sys.argv[2]
T = int(sys.argv[1])
f = open("trip_data_1/edgeWeights_" + fname + ".csv", "r")

count = 0
W = list()

for line in f:
    vals = line.split(",")
    for val in vals:
        W.append(float(val.split("\n")[0]))
f.close()

print "W has been created"
f = open("trip_data_1/LHSvertices_" + fname + ".csv", "r")

vert = dict()
for line in f:
    vals = line.split(",")
    vert[vals[1].split("\n")[0]] = int(vals[0])
f.close()

f = open("trip_data_1/LHSreappearMeans_" + fname + ".csv", "r")
g = dict()
for line in f:
    vals = line.split(",")
    if vals[0] not in vert:
        continue
    g[vert[vals[0]]] = vals[1].split("\n")[0]
f.close()

f = open("trip_data_1/splitRHSvertices_" + fname + ".csv", "r")
stats = dict()
count = 0
for line in f:
    stats[count] = [0 for i in xrange(T)]
    count = count + 1
f.close()

f = open("trip_data_1/RHSarrivals_" + fname + ".csv", "r")
count = 0
for line in f:
    val = line.split(",")
    time_s = int(val[1])-1
    stats[count/T][time_s] = float(val[2].split("\n")[0]) 
    count+=1
f.close()

print "Start with initializing LP"
#T = 350
size_u = sum(1 for line in open('trip_data_1/LHSvertices_' + fname + '.csv'))
size_v = sum(1 for line in open('trip_data_1/splitRHSvertices_' + fname + '.csv'))
print size_u,size_v, T
#cost function
cL = W*T
#cL = [1.0, 1.0, 1,1,1,1]*T
c = matrix(cL)
#b matrix
b_1 = [1.0]*(size_u*T)
b_2 = [1.0]*(size_v*T)
for i in range(size_v*T):
    b_2[i] = float(stats[i%size_v][i%T])
    #b_2[i] = 1.0/T

b = matrix(b_1 + b_2)

#Constraint matrix
w, h = size_u*size_v*T, (size_u + size_v)*T;

val = list()
I = list()
J = list()

print "Finish initialization"
for i in range(h):
    if i >= size_u*T:
        t = (i-size_u*T)/size_v+1
        j = (size_u*size_v)*(t-1)
        while j< (size_u*size_v)*t:
            if (j-(size_u*size_v)*(t-1))%size_v == (i-size_u*T)%size_v:
                val.append(1.0)
                I.append(i)
                J.append(j)
                j = j+size_v
            else:
                j = j + 1
    else:
        cur_t = i/size_u
        cur_u = i%size_u
        
        j = (i%size_u)*size_v
        while j < size_u*size_v*(cur_t+1):
            if j>=size_u*size_v*cur_t and (j-(size_u*size_v*cur_t))/size_v == i%size_u:
                val.append(1.0)
                I.append(i)
                J.append(j)
            elif j<size_u*size_v*cur_t and j/size_v == i%size_u:
                mu = float(g[i%size_u+1].split(";")[0])
                sig = float(g[i%size_u+1].split(";")[1])
                #alpha = float(g[i%size_u+1].split(";")[0])
                d = norm(loc=mu, scale=sig)
                trunc = cur_t-j/(size_u*size_v)-1
                val.append(1-d.cdf(cur_t-j/(size_u*size_v)-1))
                #xx = cur_t-j/(size_u*size_v)-1
                #if xx == 0:
                #    val.append(1.0)
                #else:
                #    val.append(1-(xx**(1-alpha))/(alpha - 1))
                #    print 1-(xx**(1-alpha))/(alpha - 1)
                #val.append(1.0)
                I.append(i)
                J.append(j)
            if (j+1)/size_v != i%size_u:
                j = j + (size_u-1)*size_v+1
            else:
                j = j+ 1
print " Done with M"
x = variable(size_u*size_v*T)
f = open("vals_" + fname + ".csv", "w+")
np.array(val).tofile(f, sep=",")
f.close()
f = open("I_" + fname + ".csv", "w+")
np.array(I).tofile(f, sep=",")
f.close()
f = open("J_" + fname + ".csv", "w+")
np.array(J).tofile(f, sep=",")
f.close()
f = open("b_" + fname + ".csv", "w+")
np.array(b).tofile(f, sep=",")
f.close()
f = open("c_" + fname + ".csv", "w+")
np.array(c).tofile(f, sep=",")
f.close()

#A = spmatrix(val, I, J)
#print A
#op(dot(c, x), [A*x<=b, x>=0, x<=1]).solve(solver=ecos, max_iter = 15)
#X = np.array(x.value)
#f = open("X.csv", "w+")
#X.tofile(f, sep=',')
#f.close()
