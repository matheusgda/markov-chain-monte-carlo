import numpy as np
import random_walks as rw
import markov_chain as mc

eps = 10 ** (-4)
n = [10, 50, 100, 300, 700, 1000, 3000, 5000, 10000]
grids = [(5, 2), (5, 10), (5, 20), (15, 20), (35, 20), (50, 20), (150, 20), (250, 20), (200, 50)]
bin_tree_h = np.log2(n)

# graphs = [rw.ring(1000), rw.full_bin_tree(9)), rw.grid2D(20, 50))]
# cs = list()
# for g in graphs:
#     cs.append(mc.MarkovChain((p_matrix)).power(method()))

mix_times = np.zeros((3, len(n)))
for i in range(len(n)):
    # mix_times[0][i] = mc.MarkovChain((rw.ring(n[i]))).power_method(eps)
    mix_times[1][i] = mc.MarkovChain((rw.full_bin_tree(int(bin_tree_h[i])))).power_method(eps)
    mix_times[2][i] = mc.MarkovChain((rw.grid2D(*grids[i]))).power_method(eps)

print(mix_times)