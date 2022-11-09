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
def sampleEdge(W_curr, safe):
    safe_index = np.where(safe == 1)[0]
    W_curr_safe = W_curr[safe_index]
    # print("W_curr_safe:", W_curr_safe)
    # print("safe_index:", safe_index)
    index = np.argmax(W_curr_safe)
    # print("index:", index)

    return safe_index[index]


def online_Greedy(LHS, RHS, W, pvt, T, K, Xopt):
    weightAlg = 0
    matches = dict()

    last_matched = [-K for cur_u in LHS]
    safe = np.array([1 for cur_u in LHS])

    for t in range(T):
        p_v = pvt[t]
        cur_v = sampleArrival(p_v, RHS)
        cur_u = sampleEdge(W[t][:, cur_v], safe)

        """
        After choosing an agent, set non-available
        """
        safe[cur_u] = 0
        last_matched[cur_u] = t
        weightAlg += W[t][cur_u][cur_v] * pvt[t][cur_v]
        matches[t] = (cur_u, cur_v)

        """
        Re-available for those occupied after K steps
        """
        unsafe_index = np.where(safe == 0)[0]
        for i in unsafe_index:
            if last_matched[i] + K <= t:
                safe[i] = 1

    return matches, weightAlg
