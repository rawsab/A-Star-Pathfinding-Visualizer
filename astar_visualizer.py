# By Rawsab Said

import pygame
import math
from queue import PriorityQueue
from maze_generator import generate_maze

# Width and height of window
WIDTH = 800
HEIGHT = 640

# Calculating number of rows required
COLS = 50
CELL_SIZE = WIDTH // COLS
ROWS = HEIGHT // CELL_SIZE

# Setting up PyGame window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm Visualizer - Rawsab Said")

# Defining colours to use
RED = (210, 65, 85)
GREEN = (80, 180, 50)
WHITE = (230, 230, 240)
BLACK = (20, 25, 30)
PURPLE = (100, 20, 240)
GREY = (200, 200, 220)
GREYBLUE = (160, 170, 190)
DARKGREYBLUE = (130, 140, 160)


# Creating a class for a cell (squares on the grid)
class Cell:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.visited = False
        self.parent = None
        self.g = math.inf
        self.f = math.inf

    def get_pos(self):
        return self.row, self.col

    # Functions to change cell roles:

    def is_wall(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE
        self.visited = False
        self.parent = None
        self.g = math.inf
        self.f = math.inf

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = RED

    def make_barrier(self):
        self.color = BLACK

    def make_open(self):
        self.color = DARKGREYBLUE

    def make_closed(self):
        self.color = GREYBLUE

    def make_path(self):
        self.color = PURPLE

    def draw(self):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < len(grid) - 1 and not grid[self.row + 1][self.col].is_wall():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < len(grid[0]) - 1 and not grid[self.row][self.col + 1].is_wall():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i, j, gap)
            grid[i].append(cell)
    return grid


def draw_grid(rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(WIN, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(WIN, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    WIN.fill(WHITE)

    for row in grid:
        for cell in row:
            cell.draw()

    draw_grid(rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def h(p1, p2):
    """Manhattan distance heuristic"""
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def get_distance(cell1, cell2):
    """Euclidean distance between two cells"""
    x1, y1 = cell1.get_pos()
    x2, y2 = cell2.get_pos()
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {cell: math.inf for row in grid for cell in row}
    g_score[start] = 0

    f_score = {cell: math.inf for row in grid for cell in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + get_distance(current, neighbor)

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


print()
print("Welcome to my A* Pathfinding Visualizer!")
print("~ Rawsab Said")
print()


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    print("GENERATING NEW MAZE")
                    newmaze = generate_maze(40, 50)
                    for row in range(50):
                        for col in range(40):
                            cell = grid[row][col]
                            if cell != end and cell != start:
                                if newmaze[row][col] == 1:
                                    cell.make_barrier()
                                elif newmaze[row][col] == 0:
                                    cell.reset()

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]
                if not start and cell != end:
                    start = cell
                    start.make_start()

                elif not end and cell != start:
                    end = cell
                    end.make_end()

                elif cell != end and cell != start:
                    cell.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]
                cell.reset()
                if cell == start:
                    start = None
                elif cell == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_RETURN:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

        pygame.display.update()

    pygame.quit()


running = True

while running:
    main(WIN, WIDTH)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Update the display
    pygame.display.flip()

    # Clean up
    pygame.quit()
