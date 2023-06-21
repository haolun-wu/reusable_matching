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
from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit

warnings.filterwarnings('ignore')

"""
Solve offline optimal LP
"""


def offline_LP_google(prob, LHS, RHS, W, pvt, T, K, lambd):
    # LHS (U): server nodes, RHS (V): call type nodes, W: weights
    # pvt: probability of v coming at time t
    # T: time horizons, K: occupied time steps
    # lambd: parameter for exponential distribution
    solver = pywraplp.Solver.CreateSolver('GLOP')
    X = [[[solver.NumVar(0.0, 1.0, "edge_{}_{}_{}".format(str(u), str(v), str(t)))
           for v in RHS] for u in LHS] for t in range(T)]
    print(np.shape(X))


    # p = xp.problem("offline linear program")
    # p.addVariable(X)

    # constraint 1: no customer over matched
    for t in range(T):
        for v in RHS:
            solver.Add(np.sum(X[t][u][v] for u in LHS) <= pvt[t][v])

    # constraint 2: no server over matched
    # for t in range(T):
    #     for u in LHS:
    #         prob += np.sum(
    #             X[tau][u][v] * math.exp(-lambd * (t - tau)) for v in RHS for tau in range(t - K, t)) + np.sum(
    #             X[t][u][v] for v in RHS) <= 1
    # prob +=  np.sum(
    #     X[tau][u][v] for v in RHS for tau in range(t - K, t)) + np.sum(
    #     X[t][u][v] for v in RHS) <= 1
    for t in range(T):
        for u in LHS:
            matched_before_raw = np.sum(
                X[tau][u][v] for v in RHS for tau in range(t - K[v], t))
            matched_before = np.sum(
                X[tau][u][v] * math.exp(-lambd[v] * (t - tau)) for v in RHS for tau in range(t - K[v], t))
            matched_now = np.sum(
                X[t][u][v] for v in RHS)

            solver.Add(matched_before + matched_now <= 1)
            # prob += matched_before_raw<= 1

    solver.Maximize(np.sum((W[t][u][v] * X[t][u][v] for v in RHS for u in LHS for t in range(T))))

    status = solver.Solve()

    # X_unnested = prob.variables()
    # _next = 0
    # print("X:", X[0][0][0].varValue)
    # print("X:", X[0][0][0].varValue)
    # print("X:", X[0][0][0].varValue)

    # matches = dict()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        # print('x =', X.solution_value())
    else:
        print('The problem does not have an optimal solution.')

    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())


    # res = [[[0 for v in RHS] for u in LHS] for t in range(T)]
    #
    # for u in LHS:
    #     for v in RHS:
    #         for t in range(T):
    #             res[t][u][v] = X[t][u][v].varValue
    #             # print("X_unnested:", X_unnested[_next])
    #             # _next += 1
    #
    # return res, prob.objective.value()
    # # return [v.varValue for v in prob.variables()], prob.objective.value()
