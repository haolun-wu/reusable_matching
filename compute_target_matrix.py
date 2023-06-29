import math
import numpy as np
from pulp import *
import warnings

warnings.filterwarnings('ignore')


def offline_LP(prob, LHS, RHS, W, pvt, T, K, lambd):
    # LHS (U): server nodes, RHS (V): call type nodes, W: weights
    # pvt: probability of v coming at time t
    # T: time horizons, K: occupied time steps
    # lambd: parameter for exponential distribution
    X = [[[LpVariable("edge_{}_{}_{}".format(str(u), str(v), str(t)), lowBound=0.0, upBound=1.0,
                      cat='Continuous') for v in RHS] for u in LHS] for t in range(T)]
    print(np.shape(X))
    print(np.shape(W))
    prob += np.sum((W[t][u][v] * X[t][u][v] for v in RHS for u in LHS for t in range(T)))

    # p = xp.problem("offline linear program")
    # p.addVariable(X)

    # constraint 1: no customer over matched
    for t in range(T):
        for v in RHS:
            prob += (np.sum(X[t][u][v] for u in LHS) <= pvt[t][v])

    # constraint 2: no server over matched
    for t in range(T):
        for u in LHS:
            matched_before_raw = np.sum(
                X[tau][u][v] for v in RHS for tau in range(t - K[v], t))
            matched_before = np.sum(
                X[tau][u][v] * math.exp(-lambd[v] * (t - tau)) for v in RHS for tau in range(t - K[v], t))
            matched_now = np.sum(
                X[t][u][v] for v in RHS)

            # prob += (matched_before_raw + matched_now <= 1)
            prob += matched_before_raw <= 1
            # prob += matched_before <= 1

    prob.solve(PULP_CBC_CMD(msg=0))

    res = [[[0 for v in RHS] for u in LHS] for t in range(T)]

    for u in LHS:
        for v in RHS:
            for t in range(T):
                res[t][u][v] = X[t][u][v].varValue
                # print("X_unnested:", X_unnested[_next])
                # _next += 1
    print("solver time:", prob.solutionTime)
    return res, prob.objective.value()
    # return [v.varValue for v in prob.variables()], prob.objective.value()


def run_all_exp(U, V, T, K, W, pvt, lambd, groups):
    prob = LpProblem("matching", LpMaximize)
    LHS, RHS = range(U), range(V)

    """
    Offline optimal
    """
    Xopt, weight_optimal = offline_LP(prob, LHS, RHS, W, pvt, T, K, lambd)
    normalized_W = W / np.reshape(np.sum(W, axis=1), (T, 1, V))

    Xopt = Xopt + normalized_W

    Xopt = np.array(Xopt).sum(0)
    print("Xopt:", Xopt.shape)

    # Split the array into groups
    split_arrays = np.split(Xopt, np.cumsum(groups)[:-1])

    # Compute the average of each group (Option 1)
    avg_arrays = [np.mean(arr, axis=0) for arr in split_arrays]

    # Compute the sum of each group (Option 2)
    sum_arrays = [np.sum(arr, axis=0) for arr in split_arrays]

    # Convert lists to numpy arrays
    avg_arrays = np.array(avg_arrays) / np.sum(avg_arrays)
    sum_arrays = np.array(sum_arrays) / np.sum(sum_arrays)

    print("avg_arrays:\n", avg_arrays)

    return avg_arrays


if __name__ == '__main__':
    """
    Simulate all the needed information
    # LHS (U): server nodes, RHS (V): call type nodes, W: weights
    # pvt: probability of v coming at time t
    # T: time horizons, K: occupied time steps
    # lambd: parameter for exponential distribution
    """

    # test the offline optimal
    groups = [6, 5, 5, 4]
    U = np.sum(groups)
    V = 3
    T_list = [100]
    # K = 25
    # K1, K2, K3 = 1, 1, 1
    # lambd1, lambd2, lambd3 = 1 / K1, 1 / K2, 1 / K3
    # K = [K1, K2, K3]
    # lambd = [lambd1, lambd2, lambd3]
    # W = np.array([[[random.uniform(0, 1) for j in range(V)] for i in range(U)] for t in range(T)])
    B_matrix = [[0.65, 0.42, 0.17], [0.63, 0.39, 0.15], [0.58, 0.35, 0.14], [0.42, 0.25, 0.11]]
    W_raw = []
    for i in range(len(groups)):
        for j in range(groups[i]):
            W_raw.append(B_matrix[i])

    offline_optimal_list, online_lp_list, online_greedy_list, online_greedy_control_list = [], [], [], []

    K_list = [3, 2, 1]

    for i in range(len(T_list)):
        print("i:", i)
        T = T_list[i]
        W = np.array([W_raw for t in range(T)])
        pvt = [[1. / 3, 1. / 4, 1. / 5] for t in range(T)]
        K = K_list
        lambd = [float(1 / K[0]), float(1 / K[1]), float(1 / K[2])]
        run_all_exp(U, V, T, K, W, pvt, lambd, groups)
