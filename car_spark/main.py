def best_score(i, take, prev_taken, bookings):
    if i == len(bookings) - 1:
        return bookings[i].revenue if take and (prev_taken is None or prev_taken.end <= bookings[i].start) else 0

    if take and (prev_taken is None or prev_taken.end <= bookings[i].start):
        return max(bookings[i].revenue + best_score(i + 1, True, bookings[i], bookings),
                   bookings[i].revenue + best_score(i + 1, False, bookings[i], bookings))
    else:
        return max(best_score(i + 1, True, prev_taken, bookings),
                   best_score(i + 1, False, prev_taken, bookings))


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
        print(max(best_score(0, True, None, bookings), best_score(0, False, None, bookings)))
