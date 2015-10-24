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

    GAME_GR = {
        (LIZARD, SCISSORS): ['B', 'T', 'T', 'B'],
        (LIZARD, LIZARD): ['T', 'B'],
        (PAPER, SCISSORS): ['B', 'T', 'T', 'B'],
        (PAPER, ROCK): ['A'],
        (PAPER, LIZARD): ['B', 'B'],
        (ROCK, SCISSORS): ['A', 'B'],
        (ROCK, PAPER): ['B'],
        (ROCK, ROCK): ['T'],
        (ROCK, LIZARD): ['A', 'B'],
        (ROCK, SPOCK): ['B'],
        (SCISSORS, SCISSORS): ['T', 'T', 'T', 'B'],
        (SCISSORS, ROCK): ['B'],
        (SCISSORS, LIZARD): ['A'],
        (SCISSORS, PAPER): ['A'],
        (SPOCK, SCISSORS): ['A', 'T', 'T', 'B'],
        (SPOCK, PAPER): ['B'],
        (SPOCK, ROCK): ['A', 'T', 'T', 'B'],
        (SPOCK, SPOCK): ['T', 'T', 'B'],
        (SPOCK, LIZARD): ['B', 'B']
    }

    CYCLES = {
        1: {
            (LIZARD, SPOCK): ("A", (LIZARD, PAPER)),
            (LIZARD, PAPER): ("A", (LIZARD, SPOCK))
        },
        2: {
            (LIZARD, ROCK): ("B", (PAPER, SPOCK)),
            (PAPER, SPOCK): ("A", (PAPER, PAPER)),
            (PAPER, PAPER): ("T", (SCISSORS, SPOCK)),
            (SCISSORS, SPOCK): ("B", (LIZARD, ROCK))
        }
    }

    CYCLE_ENTRANCE = {
        (LIZARD, SCISSORS): (LIZARD, ROCK),
        (LIZARD, LIZARD): (LIZARD, ROCK),
        (PAPER, SCISSORS): (LIZARD, ROCK),
        (PAPER, ROCK): (PAPER, SPOCK),
        (PAPER, LIZARD): (LIZARD, ROCK),
        (ROCK, SCISSORS): (LIZARD, ROCK),
        (ROCK, PAPER): (SCISSORS, SPOCK),
        (ROCK, ROCK): (PAPER, SPOCK),
        (ROCK, LIZARD): (LIZARD, ROCK),
        (ROCK, SPOCK): (LIZARD, ROCK),
        (SCISSORS, SCISSORS): (LIZARD, ROCK),
        (SCISSORS, PAPER): (SCISSORS, SPOCK),
        (SCISSORS, ROCK): (PAPER, SPOCK),
        (SCISSORS, LIZARD): (SCISSORS, SPOCK),
        (SPOCK, SCISSORS): (LIZARD, ROCK),
        (SPOCK, PAPER): (SCISSORS, SPOCK),
        (SPOCK, ROCK): (LIZARD, ROCK),
        (SPOCK, SPOCK): (LIZARD, ROCK),
        (SPOCK, LIZARD): (LIZARD, ROCK)
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

    @staticmethod
    def compute_score(n, starting_hand):
        # node is in a cycle
        if starting_hand in HandEnum.CYCLES[1]:
            return HandEnum.compute_score_cycle(n, 1, starting_hand)
        if starting_hand in HandEnum.CYCLES[2]:
            return HandEnum.compute_score_cycle(n, 2, starting_hand)

        alice_score = [0, 0, 0]
        path = HandEnum.GAME_GR[starting_hand]
        HandEnum.score_evt_update(alice_score, path[0:min(n,len(path))])

        if n <= len(path):
            return alice_score
        else:
            return HandEnum.compute_score_cycle(n - len(path), 2, HandEnum.CYCLE_ENTRANCE[starting_hand], alice_score=alice_score)

    @staticmethod
    def score_evt_update(alice_score, evt_lst, n=1):
        for evt in evt_lst:
            if evt == "A":
                alice_score[0] += n
            elif evt == "B":
                alice_score[2] += n
            else:
                alice_score[1] += n
        return alice_score

    @staticmethod
    def mk_evt_array_from_cycle(cycle_id, entry_node):
        lst = [HandEnum.CYCLES[cycle_id][entry_node][0]]
        next_node = HandEnum.CYCLES[cycle_id][entry_node][1]
        while next_node != entry_node:
            lst.append(HandEnum.CYCLES[cycle_id][next_node][0])
            next_node = HandEnum.CYCLES[cycle_id][next_node][1]
        return lst

    @staticmethod
    def compute_score_cycle(n, cycle_id, entry_node, alice_score=None):
        if alice_score is None:
            alice_score = [0, 0, 0]
        evt_lst = HandEnum.mk_evt_array_from_cycle(cycle_id, entry_node)
        nb_cycles = n // len(evt_lst)
        nb_hop = n % len(evt_lst)
        if nb_cycles > 0:
            HandEnum.score_evt_update(alice_score, evt_lst, n=nb_cycles)
        HandEnum.score_evt_update(alice_score, evt_lst[0:nb_hop])
        return alice_score

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

    def compute_score(self, start_hand, n):
        self._alice_score = HandEnum.compute_score(n, start_hand)

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

    T = int(input())
    for _ in range(0, T):
        alice_hand, bob_hand, n = parse_test_case()
        tournament = Tournament()
        tournament.compute_score((alice_hand,bob_hand), n)
        tournament.print_report()



