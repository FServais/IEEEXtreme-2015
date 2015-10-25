__author__ = 'Romain'

LETTER_VAR_MAP = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    'I': 8,
    'K': 9
}

ID_VAR_MAP = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'K'
}

SIG_NAME_LEN = 6

class FSM(object):

    def __init__(self, states, start_state):
        self._states = states
        self._curr_state = start_state

    def feed(self, signal):
        state = self._states[self._curr_state].match(signal)
        #print("s({}) : {} -> {}".format(self._curr_state, signal, state))
        if state is not None:
            self._curr_state = state
        return self._curr_state, self._states[self._curr_state].output()


class State(object):

    def __init__(self, output, transitions):
        self._output = output
        self._transitions = transitions

    def match(self, inputs):
        for transition in self._transitions:
            if State._cmp_transition(transition[0], inputs):
                return transition[1]
        return None

    def __repr__(self):
        return "{} -> {}".format(self._transitions, self._output)

    def __str__(self):
        return self.__repr__()

    def output(self):
        return self._output

    @staticmethod
    def parse(_input, var_count):
        inputs = _input.strip().split(" ")
        output, trans_count = inputs[0], inputs[1]
        transitions = [State._parse_transition(trans, var_count) for trans in inputs[2::]]
        return State(output, transitions)

    @staticmethod
    def _parse_transition(str_trans, var_count):
        trans = str_trans.split("/")
        signals_raw = trans[0].split(",")
        signals = [-1] * var_count
        for signal_raw_str in signals_raw:
            signal_raw_list = signal_raw_str.split("=")
            letter = signal_raw_list[0]
            signals[LETTER_VAR_MAP[letter]] = int(signal_raw_list[1])
        return signals, int(trans[1])

    @staticmethod
    def _cmp_transition(t1, t2):
        for i, val1 in enumerate(t1):
            if val1 != -1 and val1 != t2[i]:
                return False
        return True


def print_signal(name, sig):
    print("{}{}".format(name, ''.join([' '] * (SIG_NAME_LEN - len(name)))), end="")
    print(''.join(["***" if val == 1 else "___" for val in sig]))


def print_sig_bin(name, sig):
    print("{}{}".format(name, ''.join([' '] * (SIG_NAME_LEN - len(name)))), end="")
    print(''.join(["  {}".format(val) for val in sig]))


def render_tick(start_tick, inputs, var_count, out, states):
    print("Tick #{}".format(start_tick + 1))
    for i in range(0, var_count):
        print_signal(ID_VAR_MAP[i], map(lambda l: l[i], inputs))
    print_signal("OUT", out)
    print_sig_bin("STATE", states)
    print()

if __name__ == "__main__":
    NM = input().strip().split(" ")
    N, M = int(NM[0]), int(NM[1])
    states = []
    for _ in range(0, N):
        states.append(State.parse(input().strip(), M))
    TI = input().strip().split(" ")
    T, I = int(TI[0]), int(TI[1])
    signals = [[int(val) for val in input().strip().split(" ")] for _ in range(0, T)]
    fsm = FSM(states, I)

    evol = [fsm.feed(signal) for signal in signals]
    evol_states = list(map(lambda sao: sao[0], evol))
    evol_out = list(map(lambda sao: int(sao[1]), evol))

    for i in range(0, T, 16):
        render_tick(i, signals[i:min(i+16, T)], M, evol_out[i:min(i+16, T)], evol_states[i:min(i+16, T)])
