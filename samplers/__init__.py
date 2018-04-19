import numpy as np
import random as rdm

__all__ = ['rejection_sampler']

# Generic method to perform a 
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
