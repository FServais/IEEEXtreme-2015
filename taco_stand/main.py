T = int(input())

for _ in range(0,T):
    inp = list(map(int, input().split(" ")))
    s = inp[0]
    m = inp[1]
    r = inp[2]
    b = inp[3]

    count = 0

    ingr = [m, r, b]
    ingr = list(reversed(sorted(ingr)))

    if ingr[0] >= ingr[1] + ingr[2]:
        count = ingr[1] + ingr[2]
    else:
        first_step = ingr[0]//2
        ingr[0] -= 2*first_step
        ingr[1] -= first_step
        ingr[2] -= first_step

        if ingr[1] < 0:
            ingr[2] += ingr[1]
            ingr[1] = 0
        elif ingr[2] < 0:
            ingr[1] += ingr[2]
            ingr[2] = 0

        count += 2*first_step

        # Odd
        if ingr[0] != 0:
            if ingr[1] >= ingr[2]:
                ingr[1] -= 1
            else:
                ingr[2] -= 1
            ingr[0] -= 1
            count += 1

        count += min(ingr[1], ingr[2])

    print(min(s, count))
