import sys
import urllib.request
import random as rd
import socket

import numpy as np

import mc_estimator as mce

str_table = ['']
for i in range(97, 123):
    str_table.append(chr(i))

# Return 1 if domain_name exists, 0 otherwise.
def subdomain_indicator(domain_name):
    try:
        # urllib.request.urlopen(domain_name).getcode()
        socket.gethostbyname(domain_name)
        return 1
    except:
        return 0


def sampler_factory(max_dim):
    str_ptr = "http://www.{0}.ufrj.br"
    return lambda : str_ptr.format("".join(
        list([str_table[x] for x in np.random.randint(0, 27, size=max_dim)])))
    # return lambda : "www.google.com"


sampler = sampler_factory(4)
estimator = mce.AsyncParallelMonteCarloEstimator(
    subdomain_indicator, sampler, 200)
print(estimator.estimate(10000))
# print(estimator.acumulator, estimator.samples)
