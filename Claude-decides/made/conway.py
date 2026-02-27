"""
Conway's Game of Life — terminal animation.

Four rules:
1. A live cell with 2 or 3 neighbors survives.
2. A live cell with fewer than 2 neighbors dies (underpopulation).
3. A live cell with more than 3 neighbors dies (overcrowding).
4. A dead cell with exactly 3 neighbors becomes alive (reproduction).

That's it. From these four rules: gliders, oscillators, spaceships,
patterns that grow unboundedly, patterns that compute.

Turing-complete. From four rules about neighbors.

Run this and watch the Gosper Glider Gun fire.
(It runs for 200 generations then stops — hit Ctrl+C to exit early.)
"""

import time
import os
import sys

WIDTH, HEIGHT = 80, 40


def make_grid():
    return [[False] * WIDTH for _ in range(HEIGHT)]


def count_neighbors(grid, r, c):
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = (r + dr) % HEIGHT, (c + dc) % WIDTH
            if grid[nr][nc]:
                count += 1
    return count


def step(grid):
    new_grid = make_grid()
    for r in range(HEIGHT):
        for c in range(WIDTH):
            n = count_neighbors(grid, r, c)
            if grid[r][c]:
                new_grid[r][c] = n in (2, 3)
            else:
                new_grid[r][c] = n == 3
    return new_grid


def display(grid, generation):
    lines = [f" Generation {generation:>4}  (Ctrl+C to exit)\n"]
    for row in grid:
        lines.append(''.join('█' if cell else '·' for cell in row) + '\n')
    sys.stdout.write('\033[H' + ''.join(lines))
    sys.stdout.flush()


def place(grid, pattern, row, col):
    """Place a pattern (list of (r,c) offsets) on the grid."""
    for dr, dc in pattern:
        r, c = (row + dr) % HEIGHT, (col + dc) % WIDTH
        grid[r][c] = True


# Gosper Glider Gun — the first known finite pattern with unbounded growth.
# Discovered by Bill Gosper in 1970, winning Conway's $50 prize.
GOSPER_GLIDER_GUN = [
    (0, 24),
    (1, 22), (1, 24),
    (2, 12), (2, 13), (2, 20), (2, 21), (2, 34), (2, 35),
    (3, 11), (3, 15), (3, 20), (3, 21), (3, 34), (3, 35),
    (4, 0), (4, 1), (4, 10), (4, 16), (4, 20), (4, 21),
    (5, 0), (5, 1), (5, 10), (5, 14), (5, 16), (5, 17), (5, 22), (5, 24),
    (6, 10), (6, 16), (6, 24),
    (7, 11), (7, 15),
    (8, 12), (8, 13),
]


if __name__ == '__main__':
    grid = make_grid()
    place(grid, GOSPER_GLIDER_GUN, row=5, col=2)

    os.system('clear')
    try:
        for gen in range(200):
            display(grid, gen)
            grid = step(grid)
            time.sleep(0.08)
    except KeyboardInterrupt:
        pass

    print("\nDone.")
