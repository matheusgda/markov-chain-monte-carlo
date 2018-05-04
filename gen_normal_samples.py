import random as rdm # mersenne twister algorithm with random()
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

from samplers import *

num_of_samples = int(sys.argv[1])
params = list(map(float, sys.argv[2:]))

# support = np.arange(0.0, 10.0, 0.02)
normal = lambda x: (1 / ((2 * np.pi) ** 0.5)) * np.exp(-x * x / 2)
hands = list()

for l_param in params:
    env = envelope_normal(l_param)
    env_sampler = sample_exponential(l_param)
    samples = rejection_sampler(num_of_samples, normal, env, env_sampler)
    for s in np.nditer(samples, op_flags=['readwrite']):
        if rdm.random() < 0.5:
            s[...] = - s
    hands.append(sbn.distplot(samples))
    plt.title('Densidade empírica das amostras com lambda={0}.'.format(l_param))
    plt.xlabel('Suporte')
    plt.ylabel('Densidade')
    plt.legend(handles=hands)
    plt.grid(True)
    plt.savefig('normal_samples_from_exponential{0}.png'.format(l_param))
    plt.clf()


# plt.plot(support, env(support), 'r')
# plt.plot(support, normal(support), 'b')