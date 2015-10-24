def catalan_number_aux(n, l):
    next_index = len(l)
    if next_index == n+1:
        return l[n]

    s = 0
    for i in range(0, next_index):
        s += (l[i] * l[next_index-i-1])

    l.append(s)
    return catalan_number_aux(n, l)

def catalan_number(n):
    if n == 0:
        return 1

    return catalan_number_aux(n, [1])

def search_catalan(catalan_num):

    l = [1]

    while True:
        next_index = len(l)
        if l[next_index-1] == catalan_num:
            return next_index-1

        s = 0
        for i in range(0, next_index):
            s += (l[i] * l[next_index-i-1])

        l.append(s)

try:
    while True:
        n = int(input())

        if n <= 0: print("0")
        elif n == 1: print("3")
        else: print(search_catalan(n)+2)

except EOFError:
    pass