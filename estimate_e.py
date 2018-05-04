import sys
import random as rd

import numpy as np
import matplotlib.pyplot as plt

import mc_estimator as mc

def under_curve(x):
    if x[1] <= (1 / x[0]):
        return 1
    else:
        return 0

def build_samplers():
    sampler = lambda : np.random.rand(2) + np.array([1.0, 0.0])
    # ev = lambda x: x[1] <= 1 / x[0]
    return (under_curve, sampler)

n_of_samples = int(sys.argv[1])

points_inside = 0;
total_points = 0;
funcs = build_samplers()

e_mc = mc.MonteCarloEstimator(funcs[0], funcs[1])
ground_truth = np.exp(1)
estimations = e_mc.estimate_per_samples(n_of_samples)
print(estimations[n_of_samples - 10:])
for i in range(len(estimations)):
    estimations[i] = 2 ** (1 / estimations[i])
print(estimations[n_of_samples - 10:])

plt.loglog(
    np.arange(1, n_of_samples + 1, 1),
    np.abs((estimations - ground_truth) / ground_truth))
plt.loglog(
    np.arange(1, n_of_samples + 1, 1),
    np.log(2) *(1 - np.log(2)) /np.arange(1, n_of_samples + 1, 1)
    )
plt.title('Erro relativo e erro padrão da estimativa.')
plt.xlabel('Número de amostras')
plt.ylabel('Estimativa')
plt.grid(True)
plt.savefig('e_error.png')
plt.clf()