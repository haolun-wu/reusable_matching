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
def sampleEdge(Xopt, LHS, t, cur_v, p_v, safe):
    r = random.uniform(0, 1)
    cur_sum = 0
    for cur_u in LHS:
        if safe[cur_u] == 0:
            temp_u = 0
        else:
            # temp_u = gamma * Xopt[t][cur_u][cur_v] / (p_v * beta[(cur_u, cur_v)])
            temp_u = Xopt[t][cur_u][cur_v] / p_v

        cur_sum += temp_u
        if r <= cur_sum:
            return cur_u

    return len(LHS) - 1


"""
SOTA online
"""


# # Matching function
def online_ADAP(LHS, RHS, W, pvt, T, K, Xopt, simulate_cur_v):
    weightAlg = 0
    last_matched = dict()
    matches = dict()

    last_matched_time = [-100 for cur_u in LHS]
    last_matched_type = [-1 for cur_u in LHS]
    safe = np.array([1 for cur_u in LHS])

    for t in range(T):
        p_v = pvt[t]
        # cur_v = sampleArrival(p_v, RHS)
        cur_v = simulate_cur_v[t]
        cur_u = sampleEdge(Xopt, LHS, t, cur_v, p_v[cur_v], safe)

        # if last_matched[cur_u] + K <= t:
        #     last_matched[cur_u] = t
        #     weightAlg += W[t][cur_u][cur_v]
        #     matches[t] = (cur_u, cur_v)

        """
        After choosing an agent, set non-available
        """
        safe[cur_u] = 0
        last_matched_time[cur_u] = t
        last_matched_type[cur_u] = cur_v
        weightAlg += W[t][cur_u][cur_v]
        matches[t] = (cur_u, cur_v)

        """
        Re-available for those occupied after K steps
        """
        unsafe_index = np.where(safe == 0)[0]
        for u in unsafe_index:
            if last_matched_time[u] + K[last_matched_type[u]] <= t:
                safe[u] = 1
                last_matched_time[u] = -100
                last_matched_type[u] = -1

    return matches, weightAlg
