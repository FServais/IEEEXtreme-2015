from copy import copy

def ex_get_score(predictions, missings):

    missing_scores = {}
    for user in predictions:
        missing_scores[user] = []

    for missing in missings:
        for user in predictions:
            S1, S2 = predictions[user][missing][0], predictions[user][missing][1]
            missing_scores[user].append([get_score(predictions[user][missing][0], S1, predictions[user][missing][1], S2)
                                         for user in predictions])

    return missing_scores

def get_score(P1, S1, P2, S2):
    user_score = 0

    if (P1 > P2) == (S1 > S2):
        user_score += 10

    # Team1 score
    user_score += max(0, 5 - abs(S1 - P1))

    # Team2 score
    user_score += max(0, 5 - abs(S2 - P2))

    # Point spread
    user_score += max(0, 5 - abs(P1 - P2 - S1 + S2))

    return user_score

def argmax(l):
    max_index = 0
    _max = -1
    for i in range(0, len(l)):
        if _max < l[i]:
            _max = l[i]
            max_index = i
    return max_index

def compute_scores(predictions, real_scores):
    """
    return a dictionary {name: score}, ignore when '?'
    """
    missing_scores = []
    scores = {}

    for i, score in enumerate(real_scores):  # iterate over games
        if score == ('?', '?'):
            missing_scores.append(i)
            continue

        for j, user in enumerate(predictions):  # iterate over users
            if user not in scores:
                scores[user] = 0

            user_score = 0

            P1, P2 = predictions[user][i][0], predictions[user][i][1]
            S1, S2 = score[0], score[1]

            scores[user] += get_score(P1, S1, P2, S2)

    return scores, missing_scores

if __name__ == "__main__":
    T = int(input())

    for _ in range(0, T):
        inp = list(map(int, input().split(" ")))
        n_participants = inp[0]
        c = inp[1]

        predictions = {}
        for _ in range(0,n_participants):
            name = input()

            predict_values = []
            for _ in range(0,c):
                p = list(map(int, input().split(" ")))
                predict_values.append((p[0], p[1]))

            predictions[name] = predict_values

        real = []
        for _ in range(0,c):
            s = input().split(" ")
            if s[0] != "?" and s[1] != "?":
                s = list(map(int, s))
            real.append((s[0], s[1]))

        scores, missing_indexes = compute_scores(predictions, real)

        if len(missing_indexes) == 0:
            max_score = max([scores[user] for user in scores])
            print(' '.join(sorted(filter(lambda user: scores[user] == max_score, scores))))
        else:
            missing_scores = ex_get_score(predictions, missing_indexes)

            base_scores = []
            for user in predictions:
                base_scores.append(scores[user])

            winners = []
            for k, user in enumerate(predictions):
                curr_scores = copy(base_scores)
                for missing_score in missing_scores[user]:
                    for i in range(0, len(missing_score)):
                        curr_scores[i] += missing_score[i]
                if argmax(curr_scores) == k:
                    winners.append(user)
            print(' '.join(sorted(winners)))


    '''
    Pour le sample input, voil l'output :
    (predictions -> ) {'Alice': [(14, 17), (20, 7), (30, 7)], 'Bob': [(20, 7), (21, 17), (14, 13)]}
    (real -> ) [(14, 17), (17, 13), ('?', '?')]

    (predictions -> ) {'Dave': [(14, 17), (20, 17), (30, 7)], 'Chuck': [(20, 10), (27, 17), (30, 7)]}
    (real -> ) [('?', '?'), (27, 17), (30, 7)]

    (predictions -> ) {'Francis': [(14, 7)], 'Eve': [(10, 21)], 'George': [(7, 30)]}
    (real -> ) [(0, 1)]
    '''
