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
def sampleEdge(W_curr, safe, Xopt_curr, pvt_curr):
    safe_index = np.where(safe == 1)[0]
    W_curr_safe = W_curr[safe_index]
    # print("W_curr_safe:", W_curr_safe)
    # print("safe_index:", safe_index)
    prob = Xopt_curr / pvt_curr
    prob = prob[safe_index]

    index_select = np.arange(len(safe_index))

    if prob.sum() == 0:
        index = np.random.choice(index_select, 1, p=softmax(prob))[0]
    else:
        # index = np.random.choice(index_select, 1, p=prob)[0]
        index = index = np.argmax(prob)

    # print("prob:", prob.sum())

    # index = np.argmax(W_curr_safe)
    # print("index:", index)

    return safe_index[index]


def online_LP(LHS, RHS, W, pvt, T, K, Xopt):
    # print("Xopt:", Xopt)
    Xopt = np.array(Xopt)
    weightAlg = 0
    matches = dict()

    last_matched = [-K for cur_u in LHS]
    safe = np.array([1 for cur_u in LHS])

    for t in range(T):
        p_v = pvt[t]
        cur_v = sampleArrival(p_v, RHS)
        cur_u = sampleEdge(W[t][:, cur_v], safe, Xopt[t][:, cur_v], pvt[t][cur_v])

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
