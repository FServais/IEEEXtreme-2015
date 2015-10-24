__author__ = 'Romain'


class HandEnum(object):
    SPOCK = 1
    LIZARD = 2
    ROCK = 3
    PAPER = 4
    SCISSORS = 5

    STR_TO_HAND = {
        "Rock": ROCK,
        "Lizard": LIZARD,
        "Paper": PAPER,
        "Spock": SPOCK,
        "Scissors": SCISSORS
    }

    HAND_TO_STR = {
         ROCK: "Rock",
         LIZARD: "Lizard",
         PAPER: "Paper",
         SPOCK: "Spock",
         SCISSORS: "Scissors"
    }

    # hand 1 beats hand 2 ?
    @staticmethod
    def beats(hand1, hand2):
        if hand1 == HandEnum.SPOCK:
            return hand2 != HandEnum.PAPER and hand2 != HandEnum.LIZARD and hand2 != HandEnum.SPOCK
        elif hand1 == HandEnum.LIZARD:
            return hand2 != HandEnum.SCISSORS and hand2 != HandEnum.ROCK and hand2 != HandEnum.LIZARD
        elif hand1 == HandEnum.ROCK:
            return hand2 != HandEnum.PAPER and hand2 != HandEnum.SPOCK and hand2 != HandEnum.ROCK
        elif hand1 == HandEnum.PAPER:
            return hand2 != HandEnum.SCISSORS and hand2 != HandEnum.LIZARD and hand2 != HandEnum.PAPER
        elif hand1 == HandEnum.SCISSORS:
            return hand2 != HandEnum.SPOCK and hand2 != HandEnum.ROCK and hand2 != HandEnum.SCISSORS

    @staticmethod
    def beaten_by(hand):
        if hand == HandEnum.SPOCK:
            return [HandEnum.PAPER, HandEnum.LIZARD]
        elif hand == HandEnum.LIZARD:
            return [HandEnum.SCISSORS, HandEnum.ROCK]
        elif hand == HandEnum.ROCK:
            return [HandEnum.PAPER, HandEnum.SPOCK]
        elif hand == HandEnum.PAPER:
            return [HandEnum.SCISSORS, HandEnum.LIZARD]
        elif hand == HandEnum.SCISSORS:
            return [HandEnum.SPOCK, HandEnum.ROCK]

    @staticmethod
    def ties(hand1, hand2):
        return hand2 == hand1


class Bob(object):

    @staticmethod
    def next(own, oppo):
        won = HandEnum.beats(own, oppo)
        if won and own == HandEnum.SPOCK:
            return HandEnum.ROCK
        elif HandEnum.ties(own, oppo) and own == HandEnum.SPOCK:
            return HandEnum.LIZARD
        elif not won and own == HandEnum.SPOCK:
            return HandEnum.PAPER
        else:
            return HandEnum.SPOCK


class Alice(object):

    @staticmethod
    def next(own, oppo):
        won = HandEnum.beats(own, oppo)
        if won:
            return own
        elif HandEnum.ties(own, oppo):
            beaten_by = HandEnum.beaten_by(own)
            if HandEnum.beats(beaten_by[0], beaten_by[1]):
                return beaten_by[0]
            else:
                return beaten_by[1]
        else:
            beaten_by = HandEnum.beaten_by(oppo)
            if HandEnum.beats(beaten_by[0], beaten_by[1]):
                return beaten_by[0]
            else:
                return beaten_by[1]

class Tournament(object):

    def __init__(self):
        self._alice_score = [0,0,0]

    def print_report(self):
        if self._alice_score[0] == self._alice_score[2]:
            print("Alice and Bob tie, each winning {} game(s) and tying {} game(s)".format(self._alice_score[0], self._alice_score[1]))
        else:
            winner = "Alice" if self._alice_score[0] > self._alice_score[2] else "Bob"
            win, tie = (self._alice_score[0], self._alice_score[2]) if winner == "Alice" else \
                (self._alice_score[2], self._alice_score[1])
            print("{} wins, by winning {} game(s) and tying {} game(s)".format(winner, win, tie))

    def record_turn(self, alice, bob):
        if HandEnum.beats(alice, bob):
            self._alice_score[0] += 1
        elif HandEnum.ties(alice, bob):
            self._alice_score[1] += 1
        else:
            self._alice_score[2] += 1


def parse_test_case():
    test_case = input().strip().split(" ")
    return HandEnum.STR_TO_HAND[test_case[0]], HandEnum.STR_TO_HAND[test_case[1]], int(test_case[2])


if __name__ == "__main__":
    from itertools import combinations_with_replacement
    hands = [HandEnum.SCISSORS, HandEnum.PAPER, HandEnum.ROCK, HandEnum.SPOCK, HandEnum.LIZARD]
    comb = []
    for hand1 in hands:
        for hand2 in hands:
            comb.append((hand1, hand2))
    print(comb)

    for c in comb:
        alice, bob = c[0], c[1]
        alice_next, bob_next = Alice.next(alice, bob), Bob.next(bob, alice)
        print("{},{} -> {} -> {},{}".format(HandEnum.HAND_TO_STR[alice],
                                            HandEnum.HAND_TO_STR[bob],
                                            "A" if HandEnum.beats(alice, bob) else ("T" if HandEnum.ties(alice, bob) else "B"),
                                            HandEnum.HAND_TO_STR[alice_next],
                                            HandEnum.HAND_TO_STR[bob_next]))

    #T = int(input())
    #for _ in range(0, T):
    #    alice_hand, bob_hand, n = parse_test_case()
    #    tournament = Tournament()
    #    for i in range(0, n):
    #        tournament.record_turn(alice_hand, bob_hand)
    #        alice_hand, bob_hand = Alice.next(alice_hand, bob_hand), Bob.next(bob_hand, alice_hand)
    #    tournament.print_report()



