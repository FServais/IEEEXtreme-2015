class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, start, end):
        if start not in self.graph:
            self.graph[start] = [end]
        else:
            self.graph[start] += [end]


def create_graph():
    inp = list(map(int, input().split()))
    n = inp[0]
    m = inp[1]

    g = Graph()

    while True:
        inp = input()
        if inp == "END": break
        inp = inp.split(" ")
        g.add_edge(inp[0], inp[1])

    return g, n, m

def find_communities(graph):

    index_counter = [0]
    stack = []
    l_links = {}
    index = {}
    result = []

    def strongconnect(node):
        index[node] = index_counter[0]
        l_links[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)

        try:
            successors = graph[node]
        except:
            successors = []
        for successor in successors:
            if successor not in l_links:
                strongconnect(successor)
                l_links[node] = min(l_links[node],l_links[successor])
            elif successor in stack:
                l_links[node] = min(l_links[node],index[successor])

        if l_links[node] == index[node]:
            connected_component = []

            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node: break
            component = tuple(connected_component)

            result.append(component)

    for node in graph:
        if node not in l_links:
            strongconnect(node)

    return result


g, n, m = create_graph()

result = find_communities(g.graph)

to_print = [str(val) for val in reversed(sorted(list(map(len,result))))]
print("\n".join(to_print))

for _ in range(m-len(to_print)):
    print("Does not apply!")