__author__ = 'Romain'

class GameState(object):
    WIN = 0
    CYCLE = 1
    NONE = 2

    def __init__(self, board_size, player_count, shortcut_map, dice_rolls):
        self._board_size = board_size
        self._shortcut_map = shortcut_map
        self._dices = dice_rolls
        self._curr_dice = 0
        self._players = [0] * player_count

    def start(self):
        player = 0
        while self._curr_dice < len(self._dices):
            ret = self.play(player)

            if ret == GameState.CYCLE:
                print("PLAYER {} WINS BY EVIL CYCLE!".format(player + 1))
                return
            elif ret == GameState.WIN:
                self._print_player_pos()
                return
            player = (player + 1) % len(self._players)
        self._print_player_pos()

    def _print_player_pos(self):
        print(' '.join(str(min(player, self._board_size)) for player in self._players))

    def play(self, player):
        reached_slots = set()

        dice1, dice2 = self._dices[self._curr_dice], self._dices[self._curr_dice + 1]
        self._curr_dice += 2

        self._players[player] += dice1 + dice2

        if dice1 == dice2:
            dice3 = self._dices[self._curr_dice]
            self._curr_dice += 1
            self._players[player] += dice3

        if self._player_win(player):
            return GameState.WIN

        reached_slots.add(self._players[player])

        while not self._empty_slot(self._players[player], player):
            old_pos = self._players[player]
            if self._player_on_slot(old_pos, player):
                new_pos = old_pos + 1
            elif old_pos in self._shortcut_map:
                new_pos = self._shortcut_map[old_pos]

            if new_pos in reached_slots:
                return GameState.CYCLE

            self._players[player] = new_pos
            reached_slots.add(self._players[player])

            if self._player_win(player):
                return GameState.WIN

    def _empty_slot(self, slot, excluded_player):
        return not self._player_on_slot(slot, excluded_player) and slot not in self._shortcut_map

    def _player_win(self, player):
        return self._players[player] >= self._board_size

    def _player_on_slot(self, slot, player):  # the player on the slot, check all the others
        if player + 1 == len(self._players):
            return slot in self._players[0:-1]
        return slot in (self._players[0:player] + self._players[(player+1)::])


def parse_table():
    import sys
    N = int(input())
    board = [[row for row in input()] for _ in range(0,N)]
    M = int(input())
    dices = [int(val) for val in sys.stdin]
    return N, board, M, dices


def ind2num(i, j, N):
    return i * N + j


def sq2lin(square_board):
    lin_board = []
    for i, row in enumerate(reversed(square_board)):
        lin_board += row if i % 2 == 0 else reversed(row)
    return lin_board


def get_shortcuts(board):
    lin_board = sq2lin(board)
    bunnies_tmp = {}
    snakes_tmp = {}
    for i, slot in enumerate(lin_board):
        if slot.isalpha():
            if slot not in snakes_tmp:
                snakes_tmp[slot] = [-1, i + 1]
            else:
                snakes_tmp[slot][0] = i + 1
        elif slot.isdigit():
            if slot not in bunnies_tmp:
                bunnies_tmp[slot] = [i + 1, -1]
            else:
                bunnies_tmp[slot][1] = i + 1

    shortcuts = {}
    for bunny in bunnies_tmp:
        shortcuts[bunnies_tmp[bunny][0]] = bunnies_tmp[bunny][1]
    for bunny in snakes_tmp:
        shortcuts[snakes_tmp[bunny][0]] = snakes_tmp[bunny][1]
    return shortcuts

if __name__ == "__main__":
    N, board, M, dices = parse_table()
    shortcuts = get_shortcuts(board)
    game = GameState(N * N, M, shortcuts, dices)
    game.start()


