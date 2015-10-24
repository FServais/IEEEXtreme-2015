__author__ = 'Romain'

def compute_paths(K, cows_set):
    j = K - 2
    i_range = range(0,4)
    paths = [1, 0, 0, 0]
    while j >= 0:
        paths = [int(paths[0] + paths[1]),
                 int(paths[0] + paths[1] + paths[2]),
                 int(paths[1] + paths[2] + paths[3]),
                 int(paths[2] + paths[3])]
        for i in i_range:
            if "{},{}".format(i, j) in cows_set:
                paths[i] = 0
        j -= 1
        if sum(paths) == 0:
            break

    return paths[0]

if __name__ == "__main__":
    KN = [int(val) for val in input().split(" ")]
    K, N = KN[0], KN[1]
    cows_set = set()
    for i in range(0, N):
        XY = [int(val) for val in input().strip().split(" ")]
        cows_set.add("{},{}".format(XY[0] - 1, XY[1] - 1))

    print(compute_paths(K, cows_set) % 1000000007)


