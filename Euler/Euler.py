T = int(input())

def propagate_mark()

class Node:
    def __init__(self, color):
        self.color = color
        self.marked = False

    def set_marked(self):
        self.marked = True

    def unmark(self):
        self.marked = False

    def is_white(self):
        return self.color == "O"

    def is_black(self):
        return self.color == "X"


for _ in range(T):
    height = int(input())
    width = int(input())

    graph = [[None for w in range(width)] for h in range(height)]

    for h in range(height):
        line = list(input())
        i = 0
        for color in line:
            graph[h][i] = Node(color)
            i += 1

    for h in range(height):
        for w in range(width):
            if graph[h][w].is_white():
