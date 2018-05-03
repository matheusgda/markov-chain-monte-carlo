from threading import Thread

import numpy as np

__all__ = ["MonteCarloEstimator", "AsyncParallelMonteCarloEstimator"]

class MonteCarloEstimator:

    # accepts function objects:
    #  Note that the sampler function must be called without any argument,
    #   simply returning a variable possible value within the domain.
    def __init__(self, eval_func, sampler_func):
        self.evaluation = eval_func
        self.sampler = sampler_func

    def estimate(self, samples):
        emp_mean = 0
        for i in range(samples):
            emp_mean += self.evaluation(self.sampler())
        return emp_mean / samples



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
                a = self.sampler()
                self.acumulator[thread] += self.evaluation(a)
                # self.acumulator += self.evaluation(self.sampler())
            else:
                break


    def estimate(self, samples):
        self.acumulator = np.zeros(self.n_threads)
        self.samples = np.ones(self.n_threads) * int(samples / self.n_threads)
        self.samples[0] += samples % self.n_threads # the exact number of samples
        threads = list()
        for i in range(self.n_threads): 
            t = Thread(target=self.eval_sampler, args=(i,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        return np.sum(self.acumulator) / samples






