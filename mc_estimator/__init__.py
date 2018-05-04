from threading import Thread

import numpy as np

__all__ = ["MonteCarloEstimator", "AsyncParallelMonteCarloEstimator"]

class MonteCarloEstimator:

    # accepts function objects:
    #  Note that the sampler function must be called without any argument,
    #   simply returning a variable possible value within the domain.
    def __init__(self, eval_func, sampler_func, bias_correction=None):
        if bias_correction != None:
            self.evaluation = lambda x: eval_func(x) * bias_correction(x)
        else:
            self.evaluation = eval_func
        self.sampler = sampler_func

    def estimate(self, samples):
        emp_mean = 0
        for i in range(samples):
            emp_mean += self.evaluation(self.sampler())
        return emp_mean / samples


    def estimate_per_samples(self, samples):
        emp_mean = 0
        estimations = np.zeros(samples)
        for i in range(samples):
            emp_mean += self.evaluation(self.sampler())
            estimations[i] = emp_mean / (i + 1)
        return estimations



class AsyncParallelMonteCarloEstimator:

    def __init__(self, eval_func, sampler_func, n_threads):
        self.evaluation = eval_func
        self.sampler = sampler_func
        self.n_threads = n_threads
        self.acumulator = 0
        # Remember that, because of GIL, only 1 thread executes python code at a time
        #  ("things are atomic")


    def eval_sampler(self, thread):
        while True:
            if self.samples[thread] > 0:
                self.samples[thread] -= 1
                self.acumulator[thread] += self.evaluation(self.sampler())
            else:
                break


    # Store information to compute graph if desired
    def store_eval_sampler(self, thread):
        i = 0
        while True:
            if self.samples[thread] > 0:
                self.samples[thread] -= 1
                smp = self.sampler()
                val = self.evaluation(smp)
                self.acumulator[thread] += val
                self.sample_inf[i] = val
                i += 1
            else:
                break

    def estimate(self, samples, store_inf=False):
        self.acumulator = np.zeros(self.n_threads)
        self.samples = np.ones(self.n_threads, dtype=int) * int(samples / self.n_threads)
        self.samples[0] += samples % self.n_threads # the exact number of samples
        if store_inf:
            self.sample_inf = np.zeros((self.n_threads, self.samples[0]))
            eval_func = self.store_eval_sampler
        else:
            eval_func = self.eval_sampelr
        threads = list()
        for i in range(self.n_threads): 
            t = Thread(target=eval_func, args=(i,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        return np.sum(self.acumulator) / samples
