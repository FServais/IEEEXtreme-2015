__author__ = 'Romain'


def contains_0(tuple):
    return tuple[0] == 0 or tuple[1] == 0 or tuple[2] == 0


def play(hand, player1, player2):
    list_hand = [hand[0], hand[1], hand[2]]
    if hand[player1] > hand[player2]:
        list_hand[player1] -= hand[player2]
        list_hand[player2] *= 2
    else:
        list_hand[player2] -= hand[player1]
        list_hand[player1] *= 2
    return tuple(list_hand)


def argmin(lst, func):
    import sys
    _min = sys.maxsize
    _min_index = -1
    for i, item in enumerate(lst):
        if _min > func(item):
            _min = func(item)
            _min_index = i
    return _min_index


def add_tuple_perm(_set, tuple):
    _set.add(tuple)
    _set.add((tuple[0], tuple[2], tuple[1]))
    _set.add((tuple[1], tuple[0], tuple[2]))
    _set.add((tuple[1], tuple[2], tuple[0]))
    _set.add((tuple[2], tuple[0], tuple[1]))
    _set.add((tuple[2], tuple[1], tuple[2]))


# take - a 3-tuple containing the money of the three players
#      - the max_depth of the tree
# returns a combination of hands leading to the end of the game, None if the game couldnt
def find_end(hand, max_minute=60, time_resol=5):
    if max_minute <= 0:
        return None
    if contains_0(hand):
        return [hand]

    next_hand1 = play(hand, 0, 1)
    next_hand2 = play(hand, 0, 2)
    next_hand3 = play(hand, 1, 2)

    ret_hand1 = find_end(next_hand1, max_minute=max_minute - time_resol)
    ret_hand2 = find_end(next_hand2, max_minute=max_minute - time_resol)
    ret_hand3 = find_end(next_hand3, max_minute=max_minute - time_resol)

    if ret_hand1 == ret_hand2 == ret_hand3 is None:
        return None
    else:
        returned_lists = []
        if ret_hand1 is not None:
            returned_lists.append(ret_hand1)
        if ret_hand2 is not None:
            returned_lists.append(ret_hand2)
        if ret_hand3 is not None:
            returned_lists.append(ret_hand3)
        return [hand] + returned_lists[argmin(returned_lists, len)]


if __name__ == "__main__":
    lst_res = [int(val) for val in input().strip().split(" ")]
    res = find_end((lst_res[0], lst_res[1], lst_res[2]))
    if res is None:
        print("Ok")
    else:
        print('\n'.join(["{} {} {}".format(hand[0], hand[1], hand[2]) for hand in res]))