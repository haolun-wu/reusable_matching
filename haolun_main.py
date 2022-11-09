import math
from datetime import datetime, date, timedelta
import random
import matplotlib.pyplot as plt
from statistics import mean
import imp
import os
import numpy as np
from pulp import *
import warnings
from scipy.special import softmax

from haolun_algorithm.offline_LP import offline_LP
from haolun_algorithm.online_LP import online_LP
from haolun_algorithm.online_ADAP import online_ADAP
from haolun_algorithm.online_Greedy import online_Greedy
from haolun_algorithm.online_Greedy_control import online_Greedy_control

warnings.filterwarnings('ignore')

"""
Simulate all the needed information
# LHS (U): server nodes, RHS (V): call type nodes, W: weights
# pvt: probability of v coming at time t
# T: time horizons, K: occupied time steps
# lambd: parameter for exponential distribution
"""
# Create the 'prob' variable to contain the problem data
prob = LpProblem("matching", LpMaximize)
# test the offline optimal
U, V = 20, 3
T, K = 100, 10
lambd = 0.5
# W = np.array([[[random.uniform(0, 1) for j in range(V)] for i in range(U)] for t in range(T)])
tier1 = [8, 6, 4]
tier2 = [7, 5, 3]
tier3 = [6, 4, 2]
tier4 = [5, 3, 1]
W = [tier1] * 5 + [tier2] * 5 + [tier3] * 5 + [tier4] * 5
W = np.array([W for t in range(T)])
pvt = [[1. / V for v in range(V)] for t in range(T)]
LHS, RHS = range(U), range(V)
print("W:", W.shape)

"""
Offline optimal
"""
Xopt, optimal = offline_LP(prob, LHS, RHS, W, pvt, T, K, lambd)
print("Xopt:", Xopt[:5])
print("offline weight:", optimal)


def sampleArrival(pv, RHS):
    r = random.uniform(0, 1)
    cur_sum = 0
    for cur_v in RHS:
        cur_sum += pv[cur_v]
        if r <= cur_sum:
            return cur_v
    return len(RHS) - 1


simulate_cur_v = []
for t in range(T):
    p_v = pvt[t]
    simulate_cur_v.append(sampleArrival(p_v, RHS))

run = 20

"""
online_ADAP
"""
weight_avg_adap = 0
for _ in range(run):
    matched_pairs, online_ADAP_weight = online_ADAP(LHS, RHS, W, pvt, T, K, Xopt)
    weight_avg_adap += online_ADAP_weight
print("weight_avg_adap:", weight_avg_adap / run)

"""
online_LP
"""
weight_avg_onlp = 0
for _ in range(run):
    matched_pairs, online_LP_weight = online_LP(LHS, RHS, W, pvt, T, K, Xopt)
    weight_avg_onlp += online_LP_weight
print("weight_avg_onlp:", weight_avg_onlp / run)

"""
# Greedy
# """
weight_avg_greedy = 0
for _ in range(run):
    matched_pairs, online_Greedy_weight = online_Greedy(LHS, RHS, W, pvt, T, K, Xopt)
    weight_avg_greedy += online_Greedy_weight
print("weight_avg_greedy:", weight_avg_greedy / run)
# print("offline weight:", optimal)


"""
online_control
"""
ideal_allocation = softmax(np.sum(Xopt, 0), 0)
# print("ideal_allocation:", ideal_allocation)


alpha = 1e-2
weight_avg_greedy_control = 0
for _ in range(run):
    matched_pairs, online_Greedy_control_weight = online_Greedy_control(LHS, RHS, W, pvt, T, K, ideal_allocation, alpha)
    weight_avg_greedy_control += online_Greedy_control_weight
print("weight_avg_greedy_control:", weight_avg_greedy_control / run)
