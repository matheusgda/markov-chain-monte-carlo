import random as rdm # mersenne twister algorithm with random()
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

from samplers import rejection_sampler

# Create an envelope function for a normal distribution with a exponential dist
#  paremtrized by l.
def envelope_normal(l):
    c = np.exp((l ** 2) / 2 ) / (l * ((2 * np.pi) **0.5))
    print(c)
    return lambda x: c * l * np.exp(-l * x)


# Exponential distribution parametrized by l.
def exponential_dist(l):
    return lambda x: l * np.exp(-x * l)



# Create a sampler function for a Exponential distribution using the inverse 
#  transform method. The distribution is parametrized with l (lambda).
def sample_exponential(l):
    return lambda : (-1 / l) * np.log(1 - rdm.random())


# Create a sampler function for a Pareto distribution using the inverse 
#  transform method. The distribution is parametrized with x_0 and alpha.
#  FIX
def sample_pareto(x_0, alpha):
    v = 1 / alpha
    return lambda : x_0 * ((1 - rdm.random()) ** v)



l_param = float(sys.argv[1])
num_of_samples = int(sys.argv[2])

# support = np.arange(0.0, 10.0, 0.02)
normal = lambda x: (1 / ((2 * np.pi) ** 0.5)) * np.exp(-x * x / 2)
env = envelope_normal(l_param)
env_sampler = sample_exponential(l_param)
samples = rejection_sampler(num_of_samples, normal, env, env_sampler)

for s in np.nditer(samples, op_flags=['readwrite']):
    if rdm.random() < 0.5:
        s[...] = - s
sbn.distplot(samples)

# plt.plot(support, env(support), 'r')
# plt.plot(support, normal(support), 'b')
plt.show()
