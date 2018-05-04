import sys
import random as rd

import numpy as np
import matplotlib.pyplot as plt

import mc_estimator as mce

def goal_function(x):
    return x * np.log(x)


def integral(x):
    return (x ** 2 ) * (np.log(x) - 0.5) * 0.5


# number of samples is a parameter
def boundary_integral_diff(x):
    return (integral(x + 1) - integral(x))


def linear(x):
    return x 

def second_moment(n_samples, dist, const):
    s = 0.0
    for i in range(1, n_samples + 1):
        s += (i * np.log(i) * i * np.log(i)) / dist(i)
    return s * const


def pseudo_alias_method(x, func, const):
    rd.random() * const # gets a value from 


def naive_sampler(f_x):
    i = 1
    s = 0
    sample_prob = rd.random()
    while s < sample_prob:
        s += f_x(i)
        i += 1
    return i


sample_range = int(sys.argv[1])
sum_length = int(sys.argv[2]) # use a 1000 for question 5

arguments = np.arange(1, sum_length + 1)

sum_ground_truth = np.dot(
    goal_function(arguments), np.ones(sum_length))

const1 = integral(sum_length + 1) # integral difference of ilog(i) as pdf
const2 = (1 + sum_length) / 2 * sum_length # linear relation for i as pdf



f_x = boundary_integral_diff(np.arange(1, sum_length + 1)) / const1
for i in range(1, len(f_x)):
    f_x[i] += f_x[i-1]

def not_that_naive_sampler():
    return np.searchsorted(f_x, rd.random(), side='right')
print(not_that_naive_sampler())


proposed_vs_linear_file = "proposed_vs_linear.png"
proposed, = plt.plot(arguments, boundary_integral_diff(arguments) / const1, label='Proposta')
lin, = plt.plot(arguments, arguments / const2, label='Proporcional linear')
plt.title('Densidades utilizadas.')
plt.xlabel('Suporte')
plt.ylabel('Densidade')
plt.legend(handles=[proposed, lin])
plt.grid(True)
plt.savefig(proposed_vs_linear_file)
plt.clf()

print("Solution to part 1.")
print("Second moment of the estimator using integral: {0}".format(
    second_moment(sum_length, boundary_integral_diff, const1)))
print("Second moment of the estimator using linear f: {0}".format(
    second_moment(sum_length, linear, const2)))

# print("Generating graph for part 2.")

# estimator = mce.MonteCarloEstimator(goal_function, 
#     not_that_naive_sampler,
#     bias_correction=lambda x: const1 / (boundary_integral_diff(x)))
# estimations = estimator.estimate_per_samples(sample_range)

plt.plot(np.arange(1, sample_range + 1, 1), estimations)
plt.title('Estimativa do somatório de ilog(i).')
plt.xlabel('Número de amostras')
plt.ylabel('Estimativa')
plt.grid(True)
plt.savefig('lin_log_sum_estimation.png')
plt.clf()

# ground_truth = np.sum(np.arange(1, 1001,1) * np.log(np.arange(1, 1001, 1)))
# mse = estimations - ground_truth
# plt.plot(np.arange(1, sample_range + 1, 1), np.sqrt(mse * mse))
# plt.title('SEM do somatório de ilog(i).')
# plt.xlabel('Número de amostras')
# plt.ylabel('SEM')
# plt.grid(True)
# plt.savefig('mse_lin_log_sum_estimation.png')

# print(estimations[-1])
