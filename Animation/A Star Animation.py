import pygame
import sys
import heapq
import time

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw(self):
        self.screen.fill((255, 255, 255))


class Grid:
    def __init__(self, w, h, block_w, start, end):
        pygame.font.init()  # Initiate module
        self.w = w
        self.h = h
        self.block_w = block_w
        self.visited = {}
        self.frontier = {}
        self.walls = {}
        self.weights = {}
        self.path = []  # The path from start to end for the shortest path (Should only be present during path reconstruction)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)  # Set up font
        self.start = start
        self.end = end

    def in_bounds(self, pos):  # Check to see if the position is within the outer-most boundaries of the Grid
        x, y = pos
        return 0 <= x <= self.w - 1 and 0 <= y <= self.h - 1

    def passable(self, pos):  # Check to see if there is a wall at the given location
        return pos not in self.walls

    def cur_to_next(self, to_node):
        # Finds the cost to move into a given node (If there is no specified weight, we default to 1)
        # The default to 1 is very useful when not all weights are specified
        return self.weights.get(to_node, 1)

    def return_neighbors(self, pos):  # Return the unfiltered neighbors
        x, y = pos
        neighbors = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        neighbors = filter(self.passable, neighbors)
        neighbors = filter(self.in_bounds, neighbors)
        return neighbors

    def draw_path(self, path):
        for x, y in path:
            weighted_grid.path.append((x, y))
            pygame.draw.rect(screen.screen, (0,0,0), (x * self.block_w, y * self.block_w, self.block_w, self.block_w))
            pygame.display.update()
            clock.tick(20)

    def draw(self):
        # Draw visited
        for x, y in self.visited.keys():
            pygame.draw.rect(screen.screen, (180, 100,200),
                             (x * self.block_w, y * self.block_w, self.block_w, self.block_w))

        # Draw frontier
        for x, y in self.frontier.keys():
            pygame.draw.rect(screen.screen, (10, 50, 255),
                             (x * self.block_w, y * self.block_w, self.block_w, self.block_w))

        # Draw start
        x, y = self.start
        pygame.draw.rect(screen.screen, (0, 255, 0), (x * self.block_w, y *self.block_w, self.block_w, self.block_w))

        # Draw end
        x, y = self.end
        pygame.draw.rect(screen.screen, (0, 255, 0), (x * self.block_w, y *self.block_w, self.block_w, self.block_w))

        # Draw path
        for x, y in self.path:
            pygame.draw.rect(screen.screen, (0, 0, 0),
                             (x * self.block_w, y * self.block_w, self.block_w, self.block_w))

        # Draw walls
        for x, y in self.walls.keys():
            pygame.draw.rect(screen.screen, (200, 200, 255),
                             (x * self.block_w, y * self.block_w, self.block_w, self.block_w))

        # Draw weights
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) not in self.walls:  # We don't draw the cost for walls since they are unpassable
                    cost_txt = self.font.render(str(self.weights.get((x, y), 1)), False, (255, 100, 100))
                    screen.screen.blit(cost_txt, (x * self.block_w + 16, y * self.block_w + 2))

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

def draw_everything():
    screen.draw()
    weighted_grid.draw()
    pygame.display.update()
    clock.tick(24)  # Fps (Don't know why/how it does it)

def a_star_search(grid, start, end):
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

        weighted_grid.visited[cur] = True
        try: del weighted_grid.frontier[cur]
        except KeyError: pass

        if cur == end:
            break

        for neighbor in grid.return_neighbors(cur):
            new_cost = cost_so_far[cur] + grid.cur_to_next(neighbor)
            if new_cost < cost_so_far.get(neighbor, 10 ** 10):  # It is possible to revisit a node if a more cost effective solution is found
                cost_so_far[neighbor] = new_cost
                priority = new_cost + greedy_dist(end, neighbor)
                priority_queue.push(neighbor, priority)
                weighted_grid.frontier[neighbor] = True
                came_from[neighbor] = cur
        draw_everything()

    return came_from, cost_so_far


def reconstruct_path(came_from, start, end):
    current = end
    path = []
    while current != start:
        path.append(current)
        try:
            current = came_from[current]
        except KeyError:
            print("No Path Solution")
            return "No Path Solution"

    path.append(start)
    return path

# Create basic info
end = (6, 8)
start = (16,14)
weighted_grid = Grid(20, 15, 45, start, end)
# Walls present on the grid
weighted_grid.walls = {loc: 1 for loc in [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8), (1,3), (2,3),(0, 3), (7, 4),
(8, 4),
(9, 4),(6, 4),
(4, 3),
(3, 3),(7, 10),
(6, 10),
(5, 10),
(4, 9),
(8, 9),
(9, 8),
(10, 7),
(5, 11),
(5, 12),
(5, 13),
(5, 14)]}
# Weights for nodes on grid (If weight not specified, weight is assumed to be 1)
weighted_grid.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6),
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6),
                                       (5, 7), (5, 8), (6, 2), (6, 3),
                                       (6, 4), (6, 5), (6, 6), (6, 7),
                                       (7, 3), (7, 4), (7, 5), (1,3), (2,3), (0,3)]}
screen = Screen(1000, 900)
clock = pygame.time.Clock()


# Begin the animation and traversal
def draw_traverse_animate():
    global weighted_grid
    weighted_grid.visited = {}
    weighted_grid.frontier = {}
    weighted_grid.path = []
    weighted_grid.frontier[start] = True
    came_from, cost_so_far = a_star_search(weighted_grid, weighted_grid.start, weighted_grid.end)  # Do animation and traversal up to the endpoint
    path = reconstruct_path(came_from, weighted_grid.start, weighted_grid.end)  # Reconstruct the path from the end to start
    if path == "No Path Solution":
        time.sleep(10 ** 4)
    weighted_grid.draw_path(path)  # Draw the path
    print(path)
    print("Done")
    print("Min Cost =", cost_so_far[end])
    weighted_grid.draw_path(path)
    while True:
        screen.draw()
        weighted_grid.draw()
        # Check inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x = x // weighted_grid.block_w
                y = y // weighted_grid.block_w
                print("Addition", "({}, {})".format(x, y))
                if (x, y) in weighted_grid.walls:
                    del weighted_grid.walls[(x, y)]
                else:
                    weighted_grid.walls[(x, y)] = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    draw_traverse_animate()

        pygame.display.update()
        clock.tick(70)  # Fps (Don't know why/how it does it)

draw_traverse_animate()

