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


def greedy_dist(a, b):  # Returns the manhattan distance from point a to b or b to a
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


# A* Is 90% the same code as dijkstras
# The only difference is the introduction of a greedy implementation.
# The priority of items depend not only on the cost to get to a given node but that and also the distance from that node to the goal/end.
# This way, we provide the algorithm with a preference to go in low cost paths in combination with paths that lead towards the goal/end
# NOTE THAT THE WEIGHTS WITHIN THE PRIORITY QUEUE NO LONGER REFERENCE THE LOWEST COST TO GET TO THOSE NODES (At that moment)
def a_star_search(grid, start, end):
    # The most important parts of dijkstras is the priority queue and the presence of weighted graphs (Usually)
    # The priority queue is used to choose paths with the least cost (No matter how far the path may have already gone)

    priority_queue = Priority_queue()  # Priority queue is used to store priorities of items and return the lowest costing/priority item
    cost_so_far = dict()  # Min cost at given nodes atm
    cost_so_far[start] = 0  # Lowest cost at any given node (At a given time)
    priority_queue.push(start, 0)  # Cost of the initial node is 0
    came_from = dict()  # Stores the parent node of a node (Used to traverse the path of the min cost)
    came_from[start] = None  # Make sure that the starting node doesn't have a parent (Since its the start)

    while not priority_queue.empty():
        cur = priority_queue.get_min()

        if cur == end:  # Base case break (Arrived at destination)
            break


        # Now, we want to look at all of the current node's neighbors and calculate the costs to get to them
        # For each neighbor, the cost to get to the neighbor is the minimum cost to get to the current node + cost to go from current node to neighbor node
        # With this "new_cost", we check to see if this cost is less than the minimum cost to get to the neighbor as stored within "cost_so_far"
        # If "new cost" is lower, we set the "cost so far" of the neighbor node to be the "new cost"
        # In addition, we also append the "new cost" + the distance from the neighbor to obj node
        # The distance from the neighbor to obj node is needed since we want to add a bias for paths that come closer to the obj node
        for neighbor in grid.return_neighbors(cur):
            new_cost = cost_so_far[cur] + grid.cur_to_next(neighbor)
            if new_cost < cost_so_far.get(neighbor, 10 ** 10):  # It is possible to revisit a node if a more cost effective solution is found
                cost_so_far[neighbor] = new_cost
                priority = new_cost + greedy_dist(end, neighbor)
                priority_queue.push(neighbor, priority)
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
came_from, cost_so_far = a_star_search(weighted_grid, start, end)
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