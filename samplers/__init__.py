import numpy as np
import random as rdm

__all__ = ['rejection_sampler', 'normal_sampler', 'knuth_shuffle']

# Rejection sampler generic method 
def rejection_sampler(n_samples, f_func, envelope, g_sampler):
    samples = np.zeros(n_samples)
    for s in np.nditer(samples, op_flags=['readwrite']):
        sample = 0
        proceed = True
        while(proceed):
            sample = g_sampler()
            proceed = f_func(sample) <=  envelope(sample) * rdm.random()
        s[...] = sample
    return samples


# Sampler for normal distribution using exponential with lambda = l_param.
def normal_sampler(l_param):
    normal = lambda x: (1 / ((2 * np.pi) ** 0.5)) * np.exp(-x * x / 2)
    env = envelope_normal(l_param)
    env_sampler = sample_exponential(l_param)
    return lambda : rejection_sampler(1, normal, env, env_sampler)


# Create an envelope function for a normal distribution with a exponential dist
#  paremtrized by l.
def envelope_normal(l):
    c = np.exp((l ** 2) / 2 ) / (l * ((2 * np.pi) **0.5))
    # print(c) TODO: fix this later
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
    return lambda : x_0 / ((1 - rdm.random()) ** v)



# Use Knuth shuffle algorithm to shuffle np.array inplace
def knuth_shuffle(vector):
    offset = len(vector) - 1
    for i in range(len(vector)):
        swap(vector, i, np.random.random_integers(0, offset))


def swap(array, pos1, pos2):
    aux = array[pos2]
    array[pos2] = array[pos1]
    array[pos1] = aux
