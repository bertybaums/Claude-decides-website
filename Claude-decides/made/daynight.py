"""
Day & Night — B3678/S34678

A cellular automaton with a remarkable symmetry:
the rule treats live cells and dead cells identically.

Birth rule (B): a dead cell becomes live if it has 3, 6, 7, or 8 live neighbors.
Survival rule (S): a live cell stays live if it has 3, 4, 6, 7, or 8 live neighbors.

The symmetry: if you swap live and dead in any valid pattern,
the result is also a valid pattern that evolves identically.
Day and Night are each other's mirror image.

This means: if you find a glider in Day & Night, its negative
(swapping every cell) is also a glider, moving the same way.
The universe with mostly dead cells and the universe with mostly
live cells are, in some sense, the same universe.

Contrast with Conway's Life (B3/S23), which is not symmetric:
a universe of mostly live cells in Life quickly dies,
while a universe of mostly dead cells in Life stays mostly dead.
Day & Night has no preferred density.
"""

import random

DEAD, LIVE = 0, 1
CH = {DEAD: '·', LIVE: '█'}

BIRTH = {3, 6, 7, 8}
SURVIVE = {3, 4, 6, 7, 8}


def step(grid):
    H, W = len(grid), len(grid[0])
    new = [[DEAD] * W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            n = sum(
                grid[(r + dr) % H][(c + dc) % W]
                for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                if (dr, dc) != (0, 0)
            )
            if grid[r][c] == LIVE:
                new[r][c] = LIVE if n in SURVIVE else DEAD
            else:
                new[r][c] = LIVE if n in BIRTH else DEAD
    return new


def random_grid(W, H, density=0.5, seed=42):
    random.seed(seed)
    return [[LIVE if random.random() < density else DEAD for _ in range(W)]
            for _ in range(H)]


def invert(grid):
    """Swap live and dead — should produce a mirror-image evolution."""
    return [[1 - cell for cell in row] for row in grid]


def show(grid, label=''):
    if label:
        print(f'  {label}')
    for row in grid:
        print('  ' + ''.join(CH[c] for c in row))
    print()


def run(grid, steps):
    for _ in range(steps):
        grid = step(grid)
    return grid


def count_live(grid):
    return sum(cell for row in grid for cell in row)


if __name__ == '__main__':
    W, H = 70, 30

    print('Day & Night — B3678/S34678')
    print('The rule is symmetric: swapping live and dead gives the same dynamics.\n')

    # Demo 1: random start at 50% density
    print('─' * 50)
    print('Random start (50% density) — evolves toward complex structures:\n')
    g = random_grid(W, H, density=0.5, seed=42)
    show(g, 'generation 0')
    for milestone in [5, 15, 40, 100]:
        target = milestone
        steps_so_far = 0
        g_temp = random_grid(W, H, density=0.5, seed=42)
        g_temp = run(g_temp, milestone)
        show(g_temp, f'generation {milestone}')

    # Demo 2: the symmetry in action
    print('─' * 50)
    print('The symmetry: a pattern and its inverse (every cell flipped)\n')
    print('evolve in exactly the same way. Below: generation 30 and its inverse.\n')

    g1 = run(random_grid(W, H, density=0.5, seed=7), 30)
    g2 = invert(g1)

    live1 = count_live(g1)
    live2 = count_live(g2)
    total = W * H

    show(g1, f'pattern at generation 30  (live: {live1}/{total} = {100*live1//total}%)')
    show(g2, f'its inverse               (live: {live2}/{total} = {100*live2//total}%)')

    print('  Now evolve both forward 10 more steps...\n')
    g1b = run(g1, 10)
    g2b = run(g2, 10)
    show(g1b, 'pattern at generation 40')
    show(g2b, 'inverse at generation 40  (same structure, live/dead swapped)')

    live1b = count_live(g1b)
    live2b = count_live(g2b)
    print(f'  Live cells: {live1b} and {live2b}  (should sum to {total}: {live1b + live2b})')
    print()
    print('  The two grids are exact complements of each other at every generation.')
    print('  Day and Night are the same rule, seen from opposite sides.')
