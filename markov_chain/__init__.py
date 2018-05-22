import numpy as np

__all__:["power_method"]


def total_variation(a,b):
        return np.sum(np.abs(a - b)) * 0.5



class MarkovChain:

    def __init__(self, p_matrix, st_dist=None):
        self.p_matriz = p_matrix
        self.states = len(self.p_matrix)
        if st_dits != None:
            self.st_dist = st_dist


    # compute empirical stationary distribuition
    def power_method(eps):
        d1 = np.zeros(self.states)
        d1[0] = 1
        d2 = np.zeros(self.states)
        power_probs = self.p_matrix
        mix_t = 1
        total_var = [1]

        while(total_variation(d1, d2) > 0.25): # search for fist convergence step
            d2 = d1
            power_probs = np.matmul(power_probs, power_probs)
            mix_t = t * 2
            d1 = np.dot(d1, power_probs)

        while(total_variation(d1,d2) > eps): # finish with logarithmic factor
            d2 = d1
            power_probs = np.matmul(self.p_matrix, power_probs)
            d1 = np.dot(d1, power_probs)
            mix_t += 1

        self.st_dist = d1
        return mix_t

    # compare 
    def total_variation_per_time(t):
        d1 = np.zeros(self.states)
        d1[0] = 1
        power_probs = self.p_matrix
        total_var = [total_variation(d1, self.st_dist)]
        times = np.arange(t, 1)

        for i in times:
            power_probs = np.matmul(power_probs, self.p_matrix)
            d1 = np.dot(d1, power_probs)
            total_var.append(total_variation(d1, self.st_dist))

        return times, np.array(total_var)




