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
def sampleEdge(safe, Xopt_curr, pvt_curr):
    safe_index = np.where(safe == 1)[0]
    # W_curr_safe = W_curr[safe_index]
    # print("W_curr_safe:", W_curr_safe)
    # print("safe_index:", safe_index)

    if len(safe_index) == 0:
        return 19
    else:
        prob = Xopt_curr / pvt_curr
        prob = prob[safe_index]

        index_select = np.arange(len(safe_index))

        if prob.sum() == 0:
            index = np.random.choice(index_select, 1, p=softmax(prob))[0]
        else:
            # index = np.random.choice(index_select, 1, p=prob)[0]
            index = np.argmax(prob)

        return safe_index[index]


def online_LP(LHS, RHS, W, pvt, T, K, Xopt, simulate_cur_v):
    # print("Xopt:", Xopt)
    Xopt = np.array(Xopt)
    weightAlg = 0
    matches = dict()

    last_matched_time = [-100 for cur_u in LHS]
    last_matched_type = [-1 for cur_u in LHS]
    safe = np.array([1 for cur_u in LHS])

    for t in range(T):
        p_v = pvt[t]
        cur_v = simulate_cur_v[t]
        cur_u = sampleEdge(safe, Xopt[t][:, cur_v], pvt[t][cur_v])

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
