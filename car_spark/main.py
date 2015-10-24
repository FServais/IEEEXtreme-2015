class DPParameters(object):

    """A class for dealing with the parameters of a dynamic programming function
    params: tuple representing a set of parameters
    """
    def __init__(self, params=None):
        self.params = params
        return

    """Set the internal parameters with the given set of parameters
    """
    def set_params(self, params):
        self.params = params

    """Set the internal parameters with the given set of parameters and return the corresponding hash string
    """
    def set_and_hash(self, params):
        self.params = params
        return self.hash()

    """Returns a hash string identifying the set of parameters
    By default, the hash is the paramters joined with commas
    To use another kind of hash, this class should be reimplemented
    """
    def hash(self):
        return ','.join([str(param) for param in self.params]) if self.params is not None else ""


class DPCache(object):

    """
    """
    def __init__(self, dp_parameters=None):
        self.save_map = {}
        self.dp_parameters = DPParameters() if dp_parameters is None else dp_parameters

    """Returns the optimal value for the given set of parameters
    If the optimal value was already computed, then the result is retrieved in O(1)
    Otherwise, it is computed by calling optfunc with the set of parameters
    """
    def get(self, params):
        key = self.dp_parameters.set_and_hash(params)

        if key not in self.save_map:
            self.save_map[key] = self.optfunc(params)

        return self.save_map[key]

    """Returns true if the optimal value for the given set of parameters was already computed
    """
    def isset(self, params):
        return self.dp_parameters.set_and_hash(params) in self.save_map

    """ Returns the value of the optimal function for the given parameters
    Must implement the dynamic programming formulation in subclasses of DPCache
    In order to cache the computed results (recursively) the function should get the optimal values for
    subproblems with the function get()
    """
    def optfunc(self, params):
        pass

def best_score(i, take, prev_taken, bookings):
    if i == len(bookings) - 1:
        return bookings[i].revenue if take and (prev_taken is None or prev_taken.end <= bookings[i].start) else 0

    if take and (prev_taken is None or prev_taken.end <= bookings[i].start):
        return max(bookings[i].revenue + best_score(i + 1, True, bookings[i], bookings),
                   bookings[i].revenue + best_score(i + 1, False, bookings[i], bookings))
    else:
        return max(best_score(i + 1, True, prev_taken, bookings),
                   best_score(i + 1, False, prev_taken, bookings))



class Schedule(DPCache):

    def __init__(self, bookings):
        super().__init__()
        self._bks = bookings

    def schedule(self):
        return max(self.get((0, True, -1)), self.get((0, False, -1)))

    def optfunc(self, params):
        i = params[0]
        take = params[1]
        prev_taken = params[2]
        if i == len(bookings) - 1:
            return bookings[i].revenue if take and (prev_taken == -1 or bookings[prev_taken].end <= bookings[i].start) else 0

        if take and (prev_taken == -1 or bookings[prev_taken].end <= bookings[i].start):
            return max(bookings[i].revenue + self.get((i + 1, True, i)),
                       bookings[i].revenue + self.get((i + 1, False, i)))
        else:
            return max(self.get((i + 1, True, prev_taken)),
                       self.get((i + 1, False, prev_taken)))

class Booking(object):

    def __init__(self, start, end, revenue):
        self.start = start
        self.end = end
        self.revenue = revenue

    def __lt__(self, other):
        return self.start < other.start if self.start != other.start else self.end < other.end

    def __repr__(self):
        return "({}, {}, {})".format(self.start, self.end, self.revenue)

    def __str__(self):
        return self.__repr__()

if __name__ == "__main__" :

    T = int(input())

    for _ in range(0, T):
        N = int(input())
        bookings = []
        for _ in range(0, N):
            booking = [int(val) for val in input().strip().split(" ")]
            bookings.append(Booking(booking[0], booking[1], booking[2]))
        bookings = sorted(bookings)
        print(Schedule(bookings).schedule())
