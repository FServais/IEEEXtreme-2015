def decompose_word(word):
    to_return = {}
    for letter in list(set(word)):
        to_return[letter] = word.count(letter)

    return to_return

# """
# Check if the letters of the word1 are in the word2
# """
# def is_in_word(word1, word2):
#     decompose_w1 = decompose_word(word1)
#     decompose_w2 = decompose_word(word2)
#
#     # Have to contain all the letters and enough of them
#     for letter, count in decompose_w1.items():
#         if letter not in decompose_w2 or decompose_w2[letter] < decompose_w1[letter]:
#             return False
#
#     return True
#
# def aggregate_words(words):
#     counts = {}
#
#     for word in words:
#         d_word = decompose_word(word)
#         for letter, count in d_word.items():
#             if letter not in counts:
#                 counts[letter] = count
#             else:
#                 counts[letter] = max(counts[letter], count)
#
#     return counts
#
# def difference_dict(counts, decompose_no_dict):
#     difference = 0
#
#     # decompose_no_dict = decompose_word(no_dict)
#
#     for letter, count in counts.items():
#         if letter not in decompose_no_dict:
#             difference += count
#         elif decompose_no_dict[letter] < count:
#             difference += (count - decompose_no_dict[letter])
#
#     return difference
#
# def difference_prefect_dict(counts, no_dict):
#     difference = 0
#
#     decompose_no_dict = decompose_word(no_dict)
#
#     if len(decompose_no_dict) != len(counts): return -1
#
#     for letter, count in counts.items():
#         if decompose_no_dict[letter] < count or decompose_no_dict[letter] > count:
#             difference += abs(count - decompose_no_dict[letter])
#
#     return difference
#
# def is_perfect(words, dictionary):
#     return difference_prefect_dict(aggregate_words(words), dictionary) == 0
#

# T = int(input())
#
# for _ in range(0,T):
#     inp = list(map(int, input().split(" ")))
#
#     N_DICT = inp[0]
#     N_TEST = inp[1]
#
#     # words = {}
#     words = set()
#     for _ in range(0, N_DICT):
#         words.add(input())
#
#     for _ in range(0, N_TEST):
#         potential_dict = input()
#         decomp_dict = decompose_word(potential_dict)
#
#         missing = 0
#         perfect = True
#         aggregation = {}
#
#         for word in words:
#             decomp_word = decompose_word(word)
#
#             for letter, count in decomp_word.items():
#                 if letter not in set(decomp_dict.keys()):
#                     missing += count
#                 else:
#                     dict_count = decomp_dict[letter]
#                     if dict_count < count:
#                         missing += (count - dict_count)
#
#                 if letter not in set(aggregation.keys()):
#                     aggregation[letter] = count
#                 elif count > aggregation[letter]:
#                         aggregation[letter] = count
#
#         if missing != 0:
#             print("{} {}".format("No", missing))
#         else:
#             if aggregation == decomp_dict: print("{} {}".format("Yes", "Yes"))
#             else: print("{} {}".format("Yes", "No"))


# T = int(input())
#
# for _ in range(0,T):
#     inp = list(map(int, input().split(" ")))
#
#     N_DICT = inp[0]
#     N_TEST = inp[1]
#
#     # words = {}
#     words = set()
#     words_decomp = {}
#     aggregation = {}
#     for _ in range(0, N_DICT):
#         word = input()
#         words.add(word)
#         words_decomp[word] = decompose_word(word)
#
#         for letter, count in words_decomp[word].items():
#             if letter not in set(aggregation.keys()):
#                 aggregation[letter] = count
#             else:
#                 aggregation[letter] = max(aggregation[letter], count)
#
#     for _ in range(0, N_TEST):
#         potential_dict = input()
#         decomp_dict = decompose_word(potential_dict)
#
#         missing = 0
#         perfect = True
#
#
#         for word in words:
#             decomp_word = words_decomp[word]
#
#             for letter, count in decomp_word.items():
#                 if letter not in set(decomp_dict.keys()):
#                     missing += count
#                 else:
#                     dict_count = decomp_dict[letter]
#                     if dict_count < count:
#                         missing += (count - dict_count)
#
#
#
#         if missing != 0:
#             print("{} {}".format("No", missing))
#         else:
#             if aggregation == decomp_dict: print("{} {}".format("Yes", "Yes"))
#             else: print("{} {}".format("Yes", "No"))

def difference_dict(aggregation, decomp_dict):
    difference = 0

    for letter, count in aggregation.items():
        if letter not in decomp_dict:
            difference += count
        elif decomp_dict[letter] < count:
            difference += (count - decomp_dict[letter])

    return difference

def difference_word(aggregation, decomp_dict):
    difference = 0

    for letter, count in decomp_dict.items():
        if letter not in aggregation:
            difference += count
        elif aggregation[letter] < count:
            difference += (count - aggregation[letter])

    return difference

T = int(input())

for _ in range(0,T):
    inp = list(map(int, input().split(" ")))

    N_DICT = inp[0]
    N_TEST = inp[1]

    # words = {}
    words = set()
    words_decomp = {}
    aggregation = {}
    for _ in range(0, N_DICT):
        word = input()
        words.add(word)
        words_decomp[word] = decompose_word(word)

        for letter, count in words_decomp[word].items():
            if letter not in set(aggregation.keys()):
                aggregation[letter] = count
            else:
                aggregation[letter] = max(aggregation[letter], count)

    for _ in range(0, N_TEST):
        potential_dict = input()
        decomp_dict = decompose_word(potential_dict)

        if aggregation == decomp_dict: print("{} {}".format("Yes", "Yes"))
        else:
            # Number of differences, letters that are not in the dict but on the words
            d = difference_dict(aggregation, decomp_dict)
            if d > 0:
                print("{} {}".format("No", d))
            else:
                # d = difference_word(aggregation, decomp_dict)
                print("{} {}".format("Yes", "No"))