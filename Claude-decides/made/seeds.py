"""
Seeds — B2/S

The simplest explosive cellular automaton.
Birth rule: a dead cell comes alive if it has exactly 2 live neighbors.
Survival rule: none. Every live cell dies every generation.

This means: every generation, every live cell dies. But as it dies,
it may be creating the conditions for birth nearby. The pattern
propagates entirely by death and rebirth — no cell ever survives.

Starting from a single cell: nothing happens (a single cell has no neighbors).
Starting from two adjacent cells: the pair dies, but each cell may have
exactly 2 neighbors in some arrangements. The pattern spreads outward.

Seeds produces explosive, space-filling growth from almost any seed.
The frontier advances in all directions, leaving behind a complex interior.
Unlike Life, there is no stability: every cell you see was born this generation.

Compare: Conway's Life (B3/S23) balances birth and survival, allowing
stable structures. Seeds (B2/S) has no balance. Nothing survives.
Everything is always just born.
"""

import random

DEAD, LIVE = 0, 1
CH = {DEAD: '·', LIVE: '█'}

W, H = 75, 35


def step(grid):
    H_g, W_g = len(grid), len(grid[0])
    new = [[DEAD] * W_g for _ in range(H_g)]
    for r in range(H_g):
        for c in range(W_g):
            neighbors = sum(
                grid[(r + dr) % H_g][(c + dc) % W_g]
                for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                if (dr, dc) != (0, 0)
            )
            # Seeds: B2/S — born on 2, never survives
            if grid[r][c] == DEAD and neighbors == 2:
                new[r][c] = LIVE
    return new


def blank():
    return [[DEAD] * W for _ in range(H)]


def place(grid, pattern, r0, c0):
    for dr, dc in pattern:
        r, c = (r0 + dr) % H, (c0 + dc) % W
        grid[r][c] = LIVE


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


def count(grid):
    return sum(c for row in grid for c in row)


if __name__ == '__main__':
    print('Seeds — B2/S')
    print('No cell ever survives. Everything is always born this generation.\n')

    # A simple 2-cell seed
    print('─' * 50)
    print('Starting from two adjacent cells:\n')

    PAIR = [(0, 0), (0, 1)]

    g = blank()
    place(g, PAIR, H // 2, W // 2 - 1)
    show(g, f'step 0  ({count(g)} cells)')

    for gen in [1, 2, 4, 8, 15, 25]:
        g_at = blank()
        place(g_at, PAIR, H // 2, W // 2 - 1)
        g_at = run(g_at, gen)
        show(g_at, f'step {gen}  ({count(g_at)} cells)')

    # Show explosive growth from a denser seed
    print('─' * 50)
    print('Starting from a small cluster (5-cell cross):\n')

    CROSS = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]

    g = blank()
    place(g, CROSS, H // 2, W // 2)
    show(g, f'step 0  ({count(g)} cells)')

    g_prev = run(blank(), 0)
    place(g_prev, CROSS, H // 2, W // 2)
    for gen in [3, 8, 20]:
        g_at = blank()
        place(g_at, CROSS, H // 2, W // 2)
        g_at = run(g_at, gen)
        show(g_at, f'step {gen}  ({count(g_at)} cells)')

    print('Every cell visible was born this generation.')
    print('Every cell from the previous generation has died.')
    print('The pattern is continuous: only the pattern survives, not its cells.')
    print()
    print('This is one description of certain kinds of life.')
