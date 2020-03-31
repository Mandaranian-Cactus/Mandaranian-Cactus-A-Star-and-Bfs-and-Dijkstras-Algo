import heapq

class Grid:
    def __init__(self, w, h, walls):
        self.w = w
        self.h = h
        self.walls = {}  # Hash table
        for x, y in walls:
            self.walls[(x, y)] = True

    def in_bounds(self, pos):  # Check to see if the position is within the outer-most boundaries of the Grid
        x, y = pos
        return 0 <= x <= self.w - 1 and 0 <= y <= self.h - 1

    def passable(self, pos):  # Check to see if there is a wall at the given location
        return pos not in self.walls

    def return_neighbors(self, pos):  # Return the unfiltered neighbors
        x, y = pos
        neighbors = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        neighbors = filter(self.passable, neighbors)
        neighbors = filter(self.in_bounds, neighbors)
        return neighbors

    def draw(self, came_from, start, end):
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) == end:
                    print("E", end = ' ')
                elif (x, y) == start:
                    print("S", end=' ')
                elif (x, y) in came_from:
                    new_x, new_y = came_from[(x, y)]
                    dx, dy = new_x - x, new_y - y
                    if [dx, dy] == [1,0]:
                        print(">", end = ' ')
                    elif [dx, dy] == [-1, 0]:
                        print("<", end = ' ')
                    elif [dx, dy] == [0, 1]:
                        print("v", end = ' ')
                    elif [dx, dy] == [0, -1]:
                        print("^", end = ' ')
                elif (x, y) in self.walls:
                    print("#", end = ' ')
                else:
                    print(".", end = ' ')
            print()


class Weighted_grid(Grid):
    def __init__(self, w, h, walls):
        super().__init__(w, h, walls)
        self.weights = {}

    def cur_to_next(self, to_node):
        # Finds the cost to move into a given node (If there is no specified weight, we default to 1)
        # The default to 1 is very useful when
        return self.weights.get(to_node, 1)


class Priority_queue:
    def __init__(self):
        # Note that the heap is a min heap and NOT max heap
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def get_min(self):
        return heapq.heappop(self.elements)[1]

    def push(self, item, weight):
        heapq.heappush(self.elements, [weight, item])


def dijkstra_search(grid, start, end):
    # The most important parts of dijkstras is the priority queue and the presence of weighted graphs (Usually)
    # The priority queue is used to choose paths with the least cost (No matter how far the path may have already gone)

    priority_queue = Priority_queue()
    cost_so_far = {}
    cost_so_far[start] = 0  # Lowest cost at any given node (At a given time)
    priority_queue.push(start, 0)
    came_from = {}
    came_from[start] = None

    while not priority_queue.empty():
        cur = priority_queue.get_min()

        if cur == end:
            break

        for neighbor in grid.return_neighbors(cur):
            new_cost = cost_so_far[cur] + grid.cur_to_next(neighbor)
            if neighbor not in cost_so_far:
                cost_so_far[neighbor] = new_cost
                priority_queue.push(neighbor, new_cost)
                came_from[neighbor] = cur
            elif new_cost < cost_so_far[neighbor]:  # It is possible to revisit a node if a more cost effective solution is found
                cost_so_far[neighbor] = new_cost
                priority_queue.push(neighbor, new_cost)
                came_from[neighbor] = cur

    return came_from, cost_so_far

def reconstruct_path(came_from, start, end):
    current = end
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]

    print(len(path))
    path.append(start)
    return path


weighted_grid = Weighted_grid(10, 10, [])

weighted_grid.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
weighted_grid.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6),
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6),
                                       (5, 7), (5, 8), (6, 2), (6, 3),
                                       (6, 4), (6, 5), (6, 6), (6, 7),
                                       (7, 3), (7, 4), (7, 5)]}

end = (7, 8)
start = (1, 4)
came_from, cost_so_far = dijkstra_search(weighted_grid, start, end)
print(cost_so_far)
path = reconstruct_path(came_from, start, end)
weighted_grid.draw(came_from, start,  end)

# Draw the path
for y in range(weighted_grid.h):
    for x in range(weighted_grid.w):
        if (x, y) in path:
            print("@", end = ' ')
        else:
            print(".", end = ' ')
    print()