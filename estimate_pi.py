import sys
import random as rd
import mc_estimator as mc


def build_samplers():
    sampler = lambda : (rd.random(), rd.random())
    ev = lambda x: (x[0] * x[0] + x[1] * x[1]) <= 1
    return (ev, sampler)

n_of_samples = int(sys.argv[1])

points_inside = 0;
total_points = 0;
funcs = build_samplers(1)

pi_mc = mc.MonteCarloEstimator(funcs[0], funcs[1])
print(4 * pi_mc.estimate(n_of_samples))
