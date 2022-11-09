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

"""
Solve offline optimal LP
"""


def offline_LP(prob, LHS, RHS, W, pvt, T, K, lambd):
    # LHS (U): server nodes, RHS (V): call type nodes, W: weights
    # pvt: probability of v coming at time t
    # T: time horizons, K: occupied time steps
    # lambd: parameter for exponential distribution
    X = [[[LpVariable("edge_{}_{}_{}".format(str(u + 1), str(v + 1), str(t + 1)), lowBound=0.0, upBound=1.0,
                      cat='Continuous') for v in RHS] for u in LHS] for t in range(T)]
    print(np.shape(X))
    prob += np.sum((W[t][u][v] * X[t][u][v] for v in RHS for u in LHS for t in range(T)))

    # p = xp.problem("offline linear program")
    # p.addVariable(X)

    # constraint 1: no customer over matched
    for t in range(T):
        for v in RHS:
            prob += np.sum(X[t][u][v] for u in LHS) <= pvt[t][v]

    # constraint 2: no server over matched
    for t in range(T):
        for u in LHS:
            prob += np.sum(
                X[tau][u][v] * math.exp(-lambd * (t - tau)) for v in RHS for tau in range(t - K, t)) + np.sum(
                X[t][u][v] for v in RHS) <= 1
            # prob +=  np.sum(
            #     X[tau][u][v] for v in RHS for tau in range(t - K, t)) + np.sum(
            #     X[t][u][v] for v in RHS) <= 1

    prob.solve()

    # X_unnested = prob.variables()
    # _next = 0
    # print("X:", X[0][0][0].varValue)
    # print("X:", X[0][0][0].varValue)
    # print("X:", X[0][0][0].varValue)

    # matches = dict()

    res = [[[0 for v in RHS] for u in LHS] for t in range(T)]

    for u in LHS:
        for v in RHS:
            for t in range(T):
                res[t][u][v] = X[t][u][v].varValue
                # print("X_unnested:", X_unnested[_next])
                # _next += 1

    return res, prob.objective.value()
    # return [v.varValue for v in prob.variables()], prob.objective.value()
