"""
Brian's Brain — a cellular automaton with 3 states.

States:
  OFF    (·) : dead
  DYING  (o) : just fired, cooling down
  ON     (█) : firing

Rules:
  OFF   → ON     if exactly 2 neighbors are ON
  ON    → DYING  always
  DYING → OFF    always

That's everything. Three states. Two rules with conditions.

Result: an explosion of gliders. Brian's Brain produces more gliders
per unit area than almost any other cellular automaton. From a random
start, within a few generations, the grid fills with small objects
racing in all directions, colliding, sometimes annihilating, sometimes
producing new gliders.

Unlike Conway's Life, Brian's Brain never reaches a static state.
It is always in motion.

Named after Brian Silverman, who invented it in the 1980s.
"""

import random

OFF, DYING, ON = 0, 1, 2
WIDTH, HEIGHT = 79, 35
DENSITY = 0.2   # fraction of cells starting ON


def make_grid():
    grid = [[OFF] * WIDTH for _ in range(HEIGHT)]
    random.seed(42)  # reproducible
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if random.random() < DENSITY:
                grid[r][c] = ON
    return grid


def count_on_neighbors(grid, r, c):
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = (r + dr) % HEIGHT
            nc = (c + dc) % WIDTH
            if grid[nr][nc] == ON:
                count += 1
    return count


def step(grid):
    new_grid = [[OFF] * WIDTH for _ in range(HEIGHT)]
    for r in range(HEIGHT):
        for c in range(WIDTH):
            state = grid[r][c]
            if state == ON:
                new_grid[r][c] = DYING
            elif state == DYING:
                new_grid[r][c] = OFF
            else:  # OFF
                if count_on_neighbors(grid, r, c) == 2:
                    new_grid[r][c] = ON
    return new_grid


def display(grid, generation):
    chars = {OFF: '·', DYING: 'o', ON: '█'}
    on_count = sum(grid[r][c] == ON for r in range(HEIGHT) for c in range(WIDTH))
    dying_count = sum(grid[r][c] == DYING for r in range(HEIGHT) for c in range(WIDTH))
    print(f"--- Generation {generation:>4} | ON: {on_count:>4} | DYING: {dying_count:>4} ---")
    for row in grid:
        print(''.join(chars[c] for c in row))
    print()


if __name__ == '__main__':
    grid = make_grid()
    for gen in [0, 3, 8, 20, 50]:
        current = make_grid()
        for _ in range(gen):
            current = step(current)
        display(current, gen)
