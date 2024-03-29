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

    if len(safe_index) == 0:
        return -1
    else:
        W_curr_safe = W_curr[safe_index]
        # print("W_curr_safe:", W_curr_safe)
        # print("safe_index:", safe_index)
        index = np.argmax(W_curr_safe)
        #  print("index:", index)

        return safe_index[index]


def online_Greedy(LHS, RHS, W, pvt, T, K, simulate_cur_v):
    weightAlg = 0
    matches = dict()

    last_matched_time = [-100 for cur_u in LHS]
    last_matched_type = [-1 for cur_u in LHS]
    safe = np.array([1 for cur_u in LHS])

    for t in range(T):
        p_v = pvt[t]
        # cur_v = sampleArrival(p_v, RHS)
        cur_v = simulate_cur_v[t]
        cur_u = sampleEdge(W[t][:, cur_v], safe)

        if cur_u != -1:
            """
            After choosing an agent, set non-available
            """
            safe[cur_u] = 0
            last_matched_time[cur_u] = t
            last_matched_type[cur_u] = cur_v
            weightAlg += W[t][cur_u][cur_v]  # * pvt[t][cur_v]
            matches[t] = (cur_u, cur_v)
        else:
            weightAlg += 0  # * pvt[t][cur_v]
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


if __name__ == '__main__':
    RHS = range(3)
    pv = [0.8, 0.1, 0.1]
    for i in range(20):
        print(sampleArrival(pv, RHS))
