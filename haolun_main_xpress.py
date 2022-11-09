import math
from datetime import datetime, date, timedelta
import random
import matplotlib.pyplot as plt
from statistics import mean
import imp
import os
import numpy as np

os.environ["XPRESS"] = os.path.dirname(imp.find_module("xpress")[1])
import xpress as xp

xp.init('/Users/haolunwu/opt/anaconda3/envs/py38/lib/python3.8/site-packages/xpress/license/community-xpauth.xpr')


# Solve
def solveLP(LHS, RHS, W, pvt, T, K):
    # LHS (U): server nodes, RHS (V): customer nodes, W: weights
    # pvt: probability of v coming at time t
    # T: time horizons, K: occupied time steps
    X = [[[xp.var(vartype=xp.continuous) for v in RHS] for u in LHS] for t in range(T)]
    objective = xp.Sum((W[t][u][v] * X[t][u][v] for v in RHS for u in LHS for t in range(T)))

    p = xp.problem("offline linear program")
    p.addVariable(X)

    # constraint 1: no customer over matched
    for t in range(T):
        for v in RHS:
            p.addConstraint(xp.Sum(X[t][u][v] for u in LHS) <= pvt[t][v])

    # constraint 2: no server over matched
    for t in range(T):
        for u in LHS:
            p.addConstraint(xp.Sum(X[tau][u][v] for v in RHS for tau in range(t - K, t)) <= 1)

    # constraint 3: probability of each edge selected at any time t is in [0, 1]
    for t in range(T):
        for u in LHS:
            for v in RHS:
                p.addConstraint(X[t][u][v] <= 1)
                p.addConstraint(X[t][u][v] >= 0)

    p.setObjective(objective, sense=xp.maximize)
    p.solve()

    X_unnested = p.getSolution(p.getVariable())

    _next = 0
    for t in range(T):
        for u in LHS:
            for v in RHS:
                X[t][u][v] = X_unnested[_next]
                _next += 1

    return X, p.getAttrib()["lpobjval"]


# test the offline optimal
U, V = 20, 4
T, K = 10, 6
W = np.array([[[random.uniform(0, 1) for j in range(V)] for i in range(U)] for t in range(T)])
pvt = [[1. / V for v in range(V)] for t in range(T)]
LHS, RHS = range(U), range(V)
assert np.shape(W) == (T, U, V)
assert np.shape(pvt) == (T, V)

Xopt, optimal = solveLP(LHS, RHS, W, pvt, T, K)
print("offline:", optimal)


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

        cur_sum += temp_u
        if r <= cur_sum:
            return cur_u

    return len(LHS) - 1


# # Preprocess
def preprocess(Xopt, LHS, RHS, pvt, T, K, gamma, runs):
    # Return estimates
    Beta = dict()
    last_matched = dict()
    for _run in range(runs):
        last_matched[_run] = dict()
        for cur_u in LHS:
            last_matched[_run][cur_u] = -K

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
def getMatching(LHS, RHS, W, pvt, T, K):
    gamma = 0.5
    runs = 10

    # Xopt, optimal = solveLP(LHS, RHS, W, pvt, T, K)
    Beta = preprocess(Xopt, LHS, RHS, pvt, T, K, gamma, runs)
    # print("Beta:", len(Beta), len(Beta[9]))

    weightAlg = 0
    last_matched = dict()
    matches = dict()

    for u in LHS:
        last_matched[u] = -K

    for t in range(T):
        p_v = pvt[t]
        cur_v = simulate_cur_v[t]
        cur_u = sampleEdge(Xopt, LHS, t, cur_v, p_v[cur_v], gamma, Beta[t])

        if last_matched[cur_u] + K <= t:
            last_matched[cur_u] = t
            weightAlg += W[t][cur_u][cur_v]
            matches[t] = (cur_u, cur_v)

    return matches, weightAlg


# # Run the algorithm assuming that the LP is solved

matched_pairs, total_weight = getMatching(LHS, RHS, W, pvt, T, K)
print("total_weight:", total_weight)




"""
Greedy
"""
def sampleEdge(W_curr, safe):
    safe_index = np.where(safe == 1)[0]
    W_curr_safe = W_curr[safe_index]
    # print("W_curr_safe:", W_curr_safe)
    # print("safe_index:", safe_index)
    index = np.argmax(W_curr_safe)
    # print("index:", index)

    return safe_index[index]


def online_Greedy(LHS, RHS, W, pvt, T, K, Xopt, simulate_cur_v):
    weightAlg = 0
    matches = dict()

    last_matched = [-K for cur_u in LHS]
    safe = np.array([1 for cur_u in LHS])

    for t in range(T):
        cur_v = simulate_cur_v[t]
        cur_u = sampleEdge(W[t][:, cur_v], safe)

        safe[cur_u] = 0
        last_matched[cur_u] = t
        weightAlg += W[t][cur_u][cur_v]
        matches[t] = (cur_u, cur_v)

        # re-available after K
        unsafe_index = np.where(safe == 0)[0]
        for i in unsafe_index:
            if last_matched[i] + K <= t:
                safe[i] = 1

    return matches, weightAlg

matched_pairs, total_weight = online_Greedy(LHS, RHS, W, pvt, T, K, Xopt, simulate_cur_v)
print("total_weight:", total_weight)