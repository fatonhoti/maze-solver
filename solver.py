from random import choice
from sys import argv, exit

import pygame

# Maze settings
w = 20  # Size of cell
size = 40  # size*size grid
grid = []  # Grid nodes (x,y)
# Dictionary with solved route
#   - solution(x,y) = (x',y') where (x',y') is the previous step.
#   - If you start backtracking from the goal cell (the exit cell of the maze)
#     you will eventually end up at the start of the maze (starting cell)
solution = {}
visited = set()  # Visited nodes (cells)

# Initialize PyGame
pygame.init()
pygame.display.init()
DELAY = 5  # in milliseconds

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


def build_grid(size):
    x = 0
    y = 0
    for _ in range(1, size):
        x = w
        y += w  # Start new row
        for _ in range(1, size):
            pygame.draw.line(screen, WHITE, [x, y + w], [x, y])  # left-border
            pygame.draw.line(screen, WHITE, [x, y], [x + w, y])  # top-border
            pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])  # right-border
            pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])  # bottom-border
            grid.append((x, y))
            x = x + w


def push_up(x, y):
    pygame.draw.rect(screen, BLACK, (x + 1, y - w + 1, w - 1, 2 * w - 1), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(screen, BLACK, (x + 1, y + 1, 2 * w - 1, w - 1), 0)
    pygame.display.update()


def push_down(x, y):
    pygame.draw.rect(screen, BLACK, (x + 1, y + 1, w - 1, 2 * w - 1), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(screen, BLACK, (x - w + 1, y + 1, 2 * w - 1, w - 1), 0)
    pygame.display.update()


def remove_wall(c1, c2):
    x1 = c1[0]
    y1 = c1[1]
    x2 = c2[0]
    y2 = c2[1]
    if x1 == x2 and y2 < y1:
        # Remove top wall
        push_up(x1, y1)
    if x2 > x1 and y1 == y2:
        # Remove right wall
        push_right(x1, y1)
    if x1 == x2 and y2 > y1:
        # Remove bottom wall
        push_down(x1, y1)
    if x2 < x1 and y1 == y2:
        # Remove left wall
        push_left(x1, y1)


def paint_cell(x, y, color, size):
    pygame.draw.rect(
        screen, color, (1 + x + (w - size) // 2, 1 + y + (w - size) // 2, size, size)
    )
    pygame.display.update()


def has_unvisited_neighbours(cell):

    unvisited_neighbours = []
    x = cell[0]
    y = cell[1]

    # Check top neighbour
    if y >= 2 * w and (x, y - w) not in visited:
        unvisited_neighbours.append((x, y - w))

    # Check right neighbour
    if x <= size * w - 2 * w and (x + w, y) not in visited:
        unvisited_neighbours.append((x + w, y))

    # Check down neighbour
    if y <= size * w - 2 * w and (x, y + w) not in visited:
        unvisited_neighbours.append((x, y + w))

    # Check left neighbour
    if x >= 2 * w and (x - w, y) not in visited:
        unvisited_neighbours.append((x - w, y))

    return (unvisited_neighbours, len(unvisited_neighbours) > 0)


def carve_out_maze():

    """
    Uses a "randomized depth-first search" algorithm
    to generate and at the same time solve the maze
    using backtracking.

    see "Iterative implementation" in https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search
    """

    stack = []

    # Choose the top-left corner as the starting cell
    initial_cell = (w, w)

    # Mark it as visited
    visited.add(initial_cell)

    # Push it to the stack
    stack.append(initial_cell)

    # Implement "randomized DFS with backtracking"
    while len(stack) > 0:

        # Pop a cell from the stack and make it the current cell
        c = stack.pop()
        pygame.time.delay(DELAY)

        # Deos the current cell have any unvisited neighbours?
        (neighbours, univisted_neighbour_exists) = has_unvisited_neighbours(c)
        if univisted_neighbour_exists:

            # Push the current sell to the stack
            stack.append(c)

            # Pick one of the nighbours
            neighbour = choice(neighbours)

            # Add step to the solution route
            solution[neighbour] = c[0], c[1]

            # Remove the wall between the current cell and the chosen cell
            remove_wall(c, neighbour)

            # Mark the chosen cell as visited and push it to the stack
            visited.add(neighbour)
            stack.append(neighbour)
        else:
            # The current cell has no unvisited neighbours, start backtracking

            # "flash" a green SQUARE to indicate backtracking
            paint_cell(c[0], c[1], GREEN, size=w - 1)
            pygame.time.delay(DELAY)
            paint_cell(c[0], c[1], BLACK, size=w - 1)


# Plots the route from the exit cell of the maze to the starting cell.
def plot_solution_route(x, y):
    paint_cell(x, y, YELLOW, size=6)
    while (x, y) != (w, w):
        x, y = solution[(x, y)]
        paint_cell(x, y, YELLOW, size=6)
        pygame.time.delay(DELAY)


if __name__ == "__main__":

    if len(argv) > 1:
        size = int(argv[1])
        WIDTH = size * w + w
        HEIGHT = size * w + w
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

    build_grid(size)
    carve_out_maze()
    plot_solution_route(size * w - w, size * w - w)

    ##### PYGAME LOOP #####
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
