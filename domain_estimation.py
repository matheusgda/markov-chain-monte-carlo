import sys
import urllib.request
import random as rd
import socket

import numpy as np
import matplotlib.pyplot as plt

import mc_estimator as mce


# Return 1 if domain_name exists, 0 otherwise.
def subdomain_indicator(domain_name):
    domain_file.write(domain_name + '\n')
    try:
        # urllib.request.urlopen(domain_name).getcode()
        socket.gethostbyname(domain_name) # blocks since waits network
        return 1
    except:
        return 0


def sampler_factory(max_dim):
    str_ptr = "http://www.{0}.ufrj.br"
    return lambda : str_ptr.format("".join(
        list([str_table[x] for x in np.random.random_integers(0, 26, size=max_dim)])))


n_samples = int(sys.argv[1])
n_threads = int(sys.argv[2])
n_dim = int(sys.argv[3])
domain_file = open(sys.argv[4], 'w')

str_table = ['']
for i in range(97, 123):
    str_table.append(chr(i))



sampler = sampler_factory(n_dim)
estimator = mce.AsyncParallelMonteCarloEstimator(
    subdomain_indicator, sampler, n_threads)
n = estimator.estimate(n_samples, store_inf=True)
print(n)

estimations = np.append([],estimator.sample_inf)
for i in range(1, len(estimations)):
    estimations[i] = estimations[i - 1]

plt.plot(np.arange(1, n_samples + 1, 1), estimations)
plt.title('Número de domínios encontrados.')
plt.xlabel('Número de amostras')
plt.ylabel('Domínios')
plt.grid(True)
plt.savefig('subdomains.png')
plt.clf()

domain_file.close()
