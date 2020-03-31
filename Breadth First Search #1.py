from collections import deque

class Graph:
    def __init__(self, adj_list):
        self.adj_list = adj_list

    def return_neighbors(self, cur):
        return self.adj_list[cur]

def bfs(graph, start):
    visited = {}
    q = deque([start])
    visited[start] = True

    while q:
        cur = q.popleft()
        print(cur)
        for neighbor in graph.return_neighbors(cur):
            if neighbor not in visited:
                visited[neighbor] = True
                q.append(neighbor)

adj_list = {
    'A': ['B'],
    'B': ['A', 'C', 'D'],
    'C': ['A'],
    'D': ['E', 'A'],
    'E': ['B']
}
graph = Graph(adj_list)
bfs(graph, "A")