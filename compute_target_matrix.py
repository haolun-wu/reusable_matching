import math
from datetime import datetime, date, timedelta
import random
import matplotlib.pyplot as plt
from statistics import mean
import imp
import os
import json
import numpy as np
from pulp import *
import warnings
from scipy.special import softmax

from haolun_algorithm.offline_LP import offline_LP
from haolun_algorithm.offline_LP_google import offline_LP_google
from haolun_algorithm.online_LP import online_LP
from haolun_algorithm.online_ADAP_HL import online_ADAP
from haolun_algorithm.online_Greedy import online_Greedy
from haolun_algorithm.online_Greedy_control import online_Greedy_control

warnings.filterwarnings('ignore')


def run_all_exp(U, V, T, K, W, pvt, lambd):
    prob = LpProblem("matching", LpMaximize)
    LHS, RHS = range(U), range(V)

    """
    Offline optimal
    """
    Xopt, weight_optimal = offline_LP(prob, LHS, RHS, W, pvt, T, K, lambd)

    # Reshape the tensor so that the first dimension is now made up of 4 groups of 5 elements
    Xopt = np.array(Xopt).sum(0)
    Xopt = Xopt.reshape((4, 5, 3))

    # Sum across the new second dimension (original first dimension within each group)
    Xopt = np.sum(Xopt, axis=1)  # Shape becomes (4, 3)
    Xopt = Xopt / Xopt.sum()

    print("Xopt:", Xopt)


if __name__ == '__main__':
    """
    Simulate all the needed information
    # LHS (U): server nodes, RHS (V): call type nodes, W: weights
    # pvt: probability of v coming at time t
    # T: time horizons, K: occupied time steps
    # lambd: parameter for exponential distribution
    """

    # test the offline optimal
    a1, a2, a3, a4 = 5, 5, 5, 5
    U = a1 + a2 + a3 + a4
    V = 3
    # T_list = [60, 120, 180, 240, 300, 360, 420, 480]
    T_list = [100]
    # K = 25
    # K1, K2, K3 = 1, 1, 1
    # lambd1, lambd2, lambd3 = 1 / K1, 1 / K2, 1 / K3
    # K = [K1, K2, K3]
    # lambd = [lambd1, lambd2, lambd3]
    # W = np.array([[[random.uniform(0, 1) for j in range(V)] for i in range(U)] for t in range(T)])
    W_raw = []
    for i in range(a1):
        W_raw.append([0.65, 0.42, 0.17])
    for i in range(a2):
        W_raw.append([0.63, 0.39, 0.15])
    for i in range(a3):
        W_raw.append([0.58, 0.35, 0.14])
    for i in range(a4):
        W_raw.append([0.42, 0.25, 0.11])

    # tier1 = [0.65, 0.42, 0.17]
    # tier2 = [0.63, 0.39, 0.15]
    # tier3 = [0.58, 0.35, 0.14]
    # tier4 = [0.42, 0.25, 0.11]

    offline_optimal_list, online_lp_list, online_greedy_list, online_greedy_control_list = [], [], [], []

    K_list = [25, 20, 15]

    for i in range(len(T_list)):
        print("i:", i)
        T = T_list[i]
        W = np.array([W_raw for t in range(T)])
        pvt = [[1. / 3, 1. / 4, 1. / 4] for t in range(T)]
        K = K_list
        lambd = [float(1 / K[0]), float(1 / K[1]), float(1 / K[2])]
        run_all_exp(U, V, T, K, W, pvt, lambd)
