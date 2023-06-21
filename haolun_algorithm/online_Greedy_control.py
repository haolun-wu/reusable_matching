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
def sampleEdge(W_curr, safe, ideal_alloc, serve_cum, t, alpha):
    safe_index = np.where(safe == 1)[0]

    if len(safe_index) == 0:
        return -1
    else:

        W_curr_safe = W_curr[safe_index]
        ideal_alloc_safe = ideal_alloc[safe_index]
        serve_cum_safe = serve_cum[safe_index]

        """
        compute control
        """
        proportion_safe = serve_cum_safe - ideal_alloc_safe
        control = float(t / (t+1)) * (proportion_safe)
        # proportion_safe = softmax(serve_cum_safe) - softmax(ideal_alloc_safe)
        # control = float(t / (t + 1)) * proportion_safe

        # control =
        # print("W_curr_safe:", W_curr_safe)
        # print("control:", control)

        # print("W_curr_safe:", W_curr_safe)
        # print("control:", control)

        W_curr_control_safe = W_curr_safe + alpha * control
        index = np.argmax(W_curr_control_safe)

        return safe_index[index]


def online_Greedy_control(LHS, RHS, W, pvt, T, K, ideal_allocation, alpha, simulate_cur_v):
    weightAlg = 0
    matches = dict()

    last_matched_time = [-100 for cur_u in LHS]
    last_matched_type = [-1 for cur_u in LHS]
    safe = np.array([1 for cur_u in LHS])
    serve_times_cum = np.array([[0 for _ in RHS] for _ in LHS])

    for t in range(T):
        p_v = pvt[t]
        # cur_v = sampleArrival(p_v, RHS)
        cur_v = simulate_cur_v[t]
        # print("W[t][:, cur_v]:", W[t][:, cur_v])
        # print("safe:", safe)
        # print("ideal_allocation:", np.array(ideal_allocation)[t])


        cur_u = sampleEdge(W[t][:, cur_v], safe, ideal_allocation[t][:, cur_v], serve_times_cum[:, cur_v], t, alpha)

        if cur_u != -1:
            """
            After choosing an agent, set non-available
            """
            serve_times_cum[cur_u][cur_v] += 1
            safe[cur_u] = 0
            last_matched_time[cur_u] = t
            last_matched_type[cur_u] = cur_v
            weightAlg += W[t][cur_u][cur_v] #* pvt[t][cur_v]
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

    return matches, weightAlg
