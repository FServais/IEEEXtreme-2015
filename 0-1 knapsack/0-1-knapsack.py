'''
0-1 Knapsack problem

We have a set of 'n' objects to possibly take, each one having a weight w_i and a value, and a maximum weight to carry 'W'.
'''

'''
zero_one_knapsack(p, v, W)

INPUTS:

p: array of weights
v: array of values
W: maximal weight

OUTPUT:
Maximum value to extract
'''
def zero_one_knapsack(p, v, W):
    assert len(p) == len(v)
    M = [[0 for _ in range(W+1)] for _ in range(len(v)+1)]
    p = [0] + p
    v = [0] + v

    for k in range(1, len(v)):
        for w in range(1, W+1):
            if p[k] > w:
                M[k][w] = M[k-1][w]
            elif M[k-1][w] > v[k] + M[k-1][w - p[k]]:
                M[k][w] = M[k-1][w]
            else:
                M[k][w] = v[k] + M[k-1][w-p[k]]

    return M[len(v)-1][W]

print(zero_one_knapsack([1, 2, 5, 6, 7], [1, 6, 18, 22, 28], 11))