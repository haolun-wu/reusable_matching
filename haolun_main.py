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
    print("Xopt:", np.array(Xopt).shape, np.array(Xopt).sum(0).shape)

    # print("Xopt:", np.array(Xopt)[:5])
    # print("Xopt:", np.shape(Xopt))

    # offline_LP_google(prob, LHS, RHS, W, pvt, T, K, lambd)
    # print("Xopt:", np.array(Xopt)[:5])
    # print("offline weight:", optimal)

    def sampleArrival(pv, RHS):
        r = random.uniform(0, 1)
        cur_sum = 0
        for cur_v in RHS:
            cur_sum += pv[cur_v]
            if r <= cur_sum:
                return cur_v
        return len(RHS) - 1

    run = 100
    weight_avg_adap = 0
    weight_avg_onlp = 0
    weight_avg_greedy = 0
    weight_avg_greedy_control = 0

    for _ in range(run):
        simulate_cur_v = []
        for t in range(T):
            p_v = pvt[t]
            simulate_cur_v.append(sampleArrival(p_v, RHS))

        # """ online_ADAP """
        # matched_pairs, online_ADAP_weight = online_ADAP(LHS, RHS, W, pvt, T, K, Xopt, simulate_cur_v)
        # weight_avg_adap += online_ADAP_weight

        """ online_LP """
        matched_pairs_onlp, online_LP_weight = online_LP(LHS, RHS, W, pvt, T, K, Xopt, simulate_cur_v)
        weight_avg_onlp += online_LP_weight

        """ Greedy """
        matched_pairs_greedy, online_Greedy_weight = online_Greedy(LHS, RHS, W, pvt, T, K, simulate_cur_v)
        weight_avg_greedy += online_Greedy_weight

        """ online_control """
        # ideal_allocation = Xopt.copy()
        # for i in range(T - 1, 0, -1):
        #     ideal_allocation[i] = np.sum(Xopt[0:i + 1], 0)
        # ideal_allocation = np.array(ideal_allocation)
        # print("Xopt:", np.shape(Xopt))

        # alpha = 1e-2
        # matched_pairs, online_Greedy_control_weight = online_Greedy_control(LHS, RHS, W, pvt, T, K, ideal_allocation,
        #                                                                     alpha,
        #                                                                     simulate_cur_v)
        # weight_avg_greedy_control += online_Greedy_control_weight

    # print("weight_optimal:", weight_optimal)
    # print("weight_avg_adap:", weight_avg_adap / run)
    # print("weight_avg_onlp:", weight_avg_onlp / run)
    # print("weight_avg_greedy:", weight_avg_greedy / run)
    # print("weight_avg_greedy_control:", weight_avg_greedy_control / run)
    # print("comp ratio:", weight_avg_greedy / run / optimal)
    # print("U:{}, V:{}, T:{}".format(U, V, T))
    # print("K:{}".format(K))

    # for i in range(T):
    #     print("u:{}, v:{}".format(matched_pairs[i][0], matched_pairs[i][1]))

    return weight_optimal, weight_avg_onlp / run, weight_avg_greedy / run, weight_avg_greedy / run


if __name__ == '__main__':
    """
    Simulate all the needed information
    # LHS (U): server nodes, RHS (V): call type nodes, W: weights
    # pvt: probability of v coming at time t
    # T: time horizons, K: occupied time steps
    # lambd: parameter for exponential distribution
    """

    # test the offline optimal
    a1, a2, a3, a4 = 6, 4, 6, 4
    U = a1 + a2 + a3 + a4
    V = 3
    # T_list = [60, 120, 180, 240, 300, 360, 420, 480]
    T_list = [60]
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
    # W = [tier1] * 5 + [tier2] * 5 + [tier3] * 5 + [tier4] * 5


    offline_optimal_list, online_lp_list, online_greedy_list, online_greedy_control_list = [], [], [], []

    # K_list = [[30, 30, 30], [30, 30, 20], [30, 30, 10], [30, 30, 5], [30, 20, 20], [30, 20, 10], [30, 20, 5],
    #           [30, 10, 10], [30, 10, 5], [30, 5, 5], [20, 20, 20], [20, 20, 10], [20, 20, 5], [20, 10, 10], [20, 10, 5],
    #           [20, 5, 5], [10, 10, 10], [10, 10, 5], [10, 5, 5], [5, 5, 5]]
    K_list = [48, 41, 40]

    for i in range(len(T_list)):
        print("i:", i)
        T = T_list[i]
        W = np.array([W_raw for t in range(T)])
        pvt = [[1. / 3, 1. / 4, 1. / 4] for t in range(T)]
        K = K_list
        lambd = [float(1 / K[0]), float(1 / K[1]), float(1 / K[2])]
        offline_optimal, online_lp, online_greedy, online_greedy_control = run_all_exp(U, V, T, K, W, pvt, lambd)
        offline_optimal_list.append(offline_optimal)
        online_lp_list.append(online_lp)
        online_greedy_list.append(online_greedy)
        # online_greedy_control_list.append(online_greedy_control)
        print("offline_optimal:", offline_optimal)
        print("online_lp:", online_lp)
        print("online_greedy:", online_greedy)

    print("offline_optimal_list:", offline_optimal_list)
    print("online_lp_list:", online_lp_list)
    print("online_greedy_list:", online_greedy_list)
    # print("online_greedy_control_list:", online_greedy_control_list)

    """ save """
    with open("./saved/offline_optimal_try1214.json", "w") as fp:  # Pickling
        json.dump(offline_optimal_list, fp)
    with open("./saved/online_LP_try1214.json", "w") as fp:  # Pickling
        json.dump(offline_optimal_list, fp)
    with open("./saved/online_greedy_try1214.json", "w") as fp:  # Pickling
        json.dump(online_greedy_list, fp)
    # with open("test", "rb") as fp:  # Unpickling
    #     b = pickle.load(fp)
