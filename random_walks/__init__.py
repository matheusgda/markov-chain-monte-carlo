import numpy as np

__all__ = ["ring_rw", "full_bin_tree", "grid2D"]

# "grid_2D_rw", , "full_bin_tree_rw"

#
def ring(n):
    p_mat = np.zeros((n,n))
    for i in range(n):
        p_mat[i][i] = 0.5
        for j in range(n):
            if np.abs(i - j) == 1:
                p_mat[i][j] = 0.25
    p_mat[0][n - 1] = 0.25
    p_mat[n - 1][0] = 0.25
    return p_mat


# 
def full_bin_tree(k):
    deg, adj_mat = full_bin_tree_adj(k)
    return rd_matrix(deg, adj_mat)


# grid 2D

def grid2D(w,h):
    deg, adj_mat = grid2D_adj(w,h)
    return rd_matrix(deg, adj_mat)


def grid2D_adj(w, h):
    n = w * h
    adj_mat = np.zeros((n,n))
    deg = np.zeros(n)
    for x in range(w):
        for y in range(h):
            v = (w * y) + x
            u = list()
            if v % w != 0:
                u.append(v - 1)
            if (y + 1) * w - v != 1:
                u.append(v + 1)
            if v + w  < n:
                u.append(v + w)
            if v - w >= 0:
                u.append(v - w)
            for s in u:
                adj_mat[v][s] = 1
                adj_mat[v][v] += 1
                deg[s] += 1
                deg[v] += 1
    return deg, adj_mat

def full_bin_tree_adj(k):
    n = (2 ** (k + 1)) - 1
    h = lambda v: int(np.log2(v + 1))
    adj_mat = np.zeros((n,n))
    deg = np.zeros(n)
    for i in range(0, (2 ** k) - 1):
        h_i = h(i)
        v = i + 1
        right_dist = v - (2 ** h_i)
        left_dist = ((2 ** (h_i + 1)) - 1) - v
        j = 2 * right_dist + (2 ** (h_i + 1))
        deg[i] += 2
        deg[j] += 1
        deg[j - 1] += 1
        adj_mat[i][j] = 1
        adj_mat[j][i] = 1
        adj_mat[i][j - 1] = 1
        adj_mat[j - 1][i] = 1

    for i in range(n):
        adj_mat[i][i] = deg[i]
        deg[i] += deg[i]
    return deg, adj_mat


def rd_matrix(degrees, adj_matrix):
    t_deg = np.sum(degrees)
    rd_mat = np.copy(adj_matrix)
    for i in range(len(rd_mat)):
        rd_mat[i] = rd_mat[i] / degrees[i]
    return rd_mat