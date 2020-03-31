from collections import deque

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

def bfs(grid, start, end):
    distance = 0
    came_from = {}
    came_from[start] = None
    q = deque([start])
    while q:
        for i in range(len(q)):
            cur = q.popleft()
            if cur == end:
                return came_from, distance
            else:
                neighbors = grid.return_neighbors(cur)
                for neighbor in neighbors:
                    if neighbor not in came_from:
                        came_from[neighbor] = cur
                        q.append(neighbor)
        distance += 1

grid = Grid(15, 15, [[2,3],
                     [2,2],
                     [3,4],
                     [2,5],
                     [2,7],
                     [3,5],
                     [4,4]])
start = (6,6)
end = (3, 3)
came_from, distance = bfs(grid, start, end)
print(distance)
grid.draw(came_from, start, end)
