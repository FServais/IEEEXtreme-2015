from sys import maxsize
from copy import deepcopy

def play_turn(p, winner, looser):
    p = deepcopy(p)

    if p[looser] < p[winner]:
        p[looser] = 0
    else:
        p[looser] -= p[winner]

    p[winner] *= 2

    return p

def is_over(p):
    return 0 in p

def is_tie(p):
    return len(list(set(p))) < len(p)

def play_quickest(p, length = 0, already_seen = None, path = None):
    possibs = [(0,1), (0,2), (1,2)]

    if is_over(p):
        return p, length, path

    elif is_tie(p):
        if p[0] == p[1]:
            ties = (0, 1)
        elif p[1] == p[2]:
            ties = (1, 2)
        else:
            ties = (1, 2)

        return play_turn(p, ties[0], ties[1]), length+1, path

    else:
        final_turns = []
        final_length = []

        for p_i, p_j in possibs:
            turn = []
            if p[p_i] >= p[p_j]:
                turn = play_turn(p, p_j, p_i)
            else:
                turn = play_turn(p, p_i, p_j)

            if tuple(set(turn)) in already_seen:
                continue
            else:
                already_seen.add(tuple(set(turn)))

            last, leng, path = play_quickest(turn, length+1, already_seen, path + [deepcopy(turn)])
            final_turns.append(last)
            final_length.append(leng)

        if not final_length:
            return p, length, path

        i_min = final_length.index(min(final_length))

        return final_turns[i_min], min(final_length), path


# def find_path(start):
#     already_seen = set()
#     path = [start]
#
#     return find_path_aux(start, path, already_seen)
#
#
# def find_path_aux(p, path, already_seen):
#
#     if is_over(p):
#         return p, path
#
#     elif is_tie(p):
#         if p[0] == p[1]:
#             ties = (0, 1)
#         elif p[1] == p[2]:
#             ties = (1, 2)
#         else:
#             ties = (1, 2)
#
#         return play_turn(p, ties[0], ties[1]), deepcopy(path + [play_turn(p, ties[0], ties[1])])
#
#     if tuple(set(p)) in already_seen:
#         return p, path
#     else:
#         already_seen.add(tuple(set(p)))
#
#     results_p = []
#     results_paths = []
#
#     for p_i, p_j in [(0,1), (0,2), (1,2)]:
#         turn = []
#
#         if p[p_i] >= p[p_j]:
#             turn = play_turn(p, p_j, p_i)
#         else:
#             turn = play_turn(p, p_i, p_j)
#
#         p_result, path_result = find_path_aux(turn, deepcopy(path + [turn]), deepcopy(already_seen))
#         results_p.append(p_result)
#         results_paths.append(path_result)
#
#     result_lengths = list(map(len, results_paths))
#     i_min = result_lengths.index(min(result_lengths))
#
#     return results_p[i_min], results_paths[i_min]


test = [3, 27, 8]
turn, path = (test)

print("{} -> {}".format(turn, len(path)))
print("Path : {}".format(path))