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

warnings.filterwarnings('ignore')


# # Sample arrivals
def sampleArrival(pv, RHS):
    r = random.uniform(0, 1)
    cur_sum = 0
    for cur_v in RHS:
        cur_sum += pv[cur_v]
        if r <= cur_sum:
            return cur_v
    return len(RHS) - 1


# # Sample Edge
def sampleEdge(Xopt, LHS, t, cur_v, p_v, gamma, beta):
    r = random.uniform(0, 1)
    cur_sum = 0
    for cur_u in LHS:
        if beta[(cur_u, cur_v)] == 0:
            temp_u = 0
        else:
            temp_u = gamma * Xopt[t][cur_u][cur_v] / (p_v * beta[(cur_u, cur_v)])
            # temp_u = Xopt[t][cur_u][cur_v] / p_v

        cur_sum += temp_u
        if r <= cur_sum:
            return cur_u

    return len(LHS) - 1


"""
SOTA online
"""
# # Preprocess
def preprocess(Xopt, LHS, RHS, pvt, T, K, gamma, runs):
    # Return estimates
    Beta = dict()
    last_matched = dict()
    for _run in range(runs):
        last_matched[_run] = dict()
        for cur_u in LHS:
            last_matched[_run][cur_u] = -100

    for _ in range(T):
        Beta[_] = dict()

    # Compute statistics
    safe = [[1 for _run in range(runs)] for cur_u in LHS]
    # print("safe:", np.shape(safe))
    for t in range(T):
        pv = pvt[t]
        for cur_v in RHS:  # 0, ..., |V|-1
            for cur_u in LHS:  # 0, ..., |U|-1
                Beta[t][(cur_u, cur_v)] = mean(safe[cur_u])
        safe = [[1 for _run in range(runs)] for cur_u in LHS]
        for _run in range(runs):
            cur_v = sampleArrival(pv, RHS)
            cur_u = sampleEdge(Xopt, LHS, t, cur_v, pv[cur_v], gamma, Beta[t])

            if last_matched[_run][cur_u] + K <= t:
                last_matched[_run][cur_u] = t

            for cur_u in LHS:
                if last_matched[_run][cur_u] + K > t:
                    safe[cur_u][_run] = 0
    return Beta


# # Matching function
def online_ADAP(LHS, RHS, W, pvt, T, K, Xopt):
    gamma = 0.5
    runs = 10

    Beta = preprocess(Xopt, LHS, RHS, pvt, T, K, gamma, runs)

    weightAlg = 0
    last_matched = dict()
    matches = dict()

    for u in LHS:
        last_matched[u] = -K

    for t in range(T):
        p_v = pvt[t]
        cur_v = sampleArrival(p_v, RHS)
        cur_u = sampleEdge(Xopt, LHS, t, cur_v, p_v[cur_v], gamma, Beta[t])

        if last_matched[cur_u] + K <= t:
            last_matched[cur_u] = t
            weightAlg += W[t][cur_u][cur_v]
            matches[t] = (cur_u, cur_v)

    return matches, weightAlg

