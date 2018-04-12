
__all__ = ["MonteCarloEstimator"]

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
