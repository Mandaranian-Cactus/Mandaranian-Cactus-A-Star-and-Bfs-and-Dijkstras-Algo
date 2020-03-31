import heapq
from sys import stdin

class Priority_Queue:
    def __init__(self):
        self.items = []

    def push(self, name, weight):
        heapq.heappush(self.items, [weight, name])

    def get(self):
        return heapq.heappop(self.items)[1]

def dijkstras(weighted_adj_list, start, end):
    priority_queue = Priority_Queue()
    min_cost_at = {}
    came_from = {}

    priority_queue.push(start, 0)
    came_from[start] = None
    min_cost_at[start] = 0

    while priority_queue.items:
        cur = priority_queue.get()
        if cur == end:
            break
        else:
            for neighbor, travel_cost in weighted_adj_list[cur]:
                new_cost = travel_cost + min_cost_at[cur]
                if new_cost < min_cost_at.get(neighbor, 10 ** 12):
                    min_cost_at[neighbor] = new_cost
                    came_from[neighbor] = cur
                    priority_queue.push(neighbor, new_cost)

    return came_from, min_cost_at


weighted_adj_list = {0:[[1,4],
                        [2,3]],
                     1:[[2,1],
                       [3,2]],
                     2:[[3,4]],
                     3:[[4,2]],
                     4:[[5,6]],
                     5:[]}

came_from, min_cost_at = dijkstras(weighted_adj_list, 1, 5)
print(came_from, min_cost_at, sep = '\n')
