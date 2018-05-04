import sys

import numpy as np
import seaborn as sbn
import matplotlib.pyplot as plt

import mc_estimator as mce
import samplers as smp

l_param = 1.0
tail_init = 5
eval_tail = lambda x: (x >= tail_init) * 1

max_num_of_samples = int(sys.argv[1])

i = 0
p_i = 1
estimations = np.zeros(max_num_of_samples)

# estimator = mce.MonteCarloEstimator(eval_tail, smp.normal_sampler(l_param))
# estimations = estimator.estimate_per_samples(max_num_of_samples)

# plt.plot(np.arange(1, max_num_of_samples + 1, 1), estimations)
# plt.title('Estimativa de probabilidade de cauda 1.')
# plt.xlabel('Número de amostras')
# plt.ylabel('Estimativa')
# plt.grid(True)
# plt.savefig('tail_estimation_1.png')
# plt.clf()
# print(estimations[-1])

def normal(mean):
    return lambda x: (1 / ((2 * np.pi) ** 0.5)) * np.exp(- (x - mean) * (x - mean) / 2)

estimator = mce.MonteCarloEstimator(eval_tail, 
    lambda : smp.normal_sampler(1.0)() + 5,
    bias_correction=lambda x: normal(0)(x) / normal(5)(x))

estimations = estimator.estimate_per_samples(max_num_of_samples)

plt.plot(np.arange(1, max_num_of_samples + 1, 1), estimations)
plt.title('Estimativa de probabilidade de cauda 2.')
plt.xlabel('Número de amostras')
plt.ylabel('Estimativa')
plt.grid(True)
plt.savefig('tail_estimation_2.png')
print(estimations[-1])


