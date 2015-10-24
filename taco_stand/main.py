__author__ = 'Romain'


def argmax(a, b, c):
    if a > b:
        if c > a:
            return 3
        else:
            return 1
    else:
        if c > b:
            return 3
        else:
            return 2


def argmin(a, b, c):
    if a > b:
        if b > c:
            return 3
        else:
            return 2
    else:
        if a > c:
            return 3
        else:
            return 1


def order_index(a, b, c):
    _max = argmax(a, b, c)
    _min = argmin(a, b, c)
    _mid = 6 - (_max + _min)
    return _max - 1, _mid - 1, _min - 1


def nb_tacos(shells, meat, rice, beans):
    ingrs = [meat, rice, beans]
    _max, _mid, _min = order_index(ingrs[0], ingrs[1], ingrs[2])

    # make two equals
    nb_tacos_1 = ingrs[_mid] - ingrs[_min]
    ingrs[_mid] -= nb_tacos_1
    ingrs[_max] -= nb_tacos_1

    if ingrs[_mid] == ingrs[_min] == 0:
        return min(nb_tacos_1, shells)

    if ingrs[_max] > ingrs[_mid] * 2:
        return min(nb_tacos_1 + ingrs[_min] * 2, shells)

    # make all equals
    nb_tacos_2 = 2 * (ingrs[_max] - ingrs[_mid])
    ingrs[_max] -= nb_tacos_2
    ingrs[_mid] -= nb_tacos_2 // 2
    ingrs[_min] -= nb_tacos_2 // 2

    # rotate
    nb_tacos_3 = (ingrs[_max] // 2) * 3

    return min(nb_tacos_1 + nb_tacos_2 + nb_tacos_3, shells)


if __name__ == "__main__":
    N = int(input())
    for i in range(0, N):
        ingredients = [int(val) for val in input().split(" ")]
        print(nb_tacos(ingredients[0], ingredients[1], ingredients[2], ingredients[3]))
