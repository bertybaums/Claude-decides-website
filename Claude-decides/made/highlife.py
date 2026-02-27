"""
HighLife — B36/S23

Like Conway's Life (B3/S23) but with one extra birth condition:
a dead cell with exactly 6 live neighbors also becomes alive.

This single change — adding B6 — has a profound consequence:
HighLife contains self-replicating patterns.

Life has no known replicators (patterns that produce perfect copies
of themselves and continue doing so). HighLife does. This matters:
self-replication is considered the key property for open-ended
evolution. HighLife can, in principle, evolve in a way Life cannot.

The replicator is a specific 7-cell pattern. After some generations,
it produces two copies of itself, then four, then eight, doubling
each period. The grid fills with replicators.

Below: first, a standard Life glider (which also works in HighLife
since the survival rules are identical), then a random start to
show HighLife's character, then the replicator itself.
"""

import random

EMPTY, LIVE = 0, 1
CH = {EMPTY: '·', LIVE: '█'}


def step_highlife(grid, torus=True):
    H, W = len(grid), len(grid[0])
    new = [[EMPTY] * W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            if torus:
                neighbors = sum(
                    grid[(r+dr) % H][(c+dc) % W]
                    for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                    if (dr, dc) != (0, 0)
                )
            else:
                neighbors = sum(
                    grid[r+dr][c+dc]
                    for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                    if (dr, dc) != (0, 0)
                    and 0 <= r+dr < H and 0 <= c+dc < W
                )
            if grid[r][c] == LIVE:
                new[r][c] = LIVE if neighbors in (2, 3) else EMPTY
            else:
                new[r][c] = LIVE if neighbors in (3, 6) else EMPTY
    return new


def blank(W=80, H=30):
    return [[EMPTY] * W for _ in range(H)]


def place(grid, pattern, row, col):
    for dr, dc in pattern:
        r, c = (row + dr) % len(grid), (col + dc) % len(grid[0])
        grid[r][c] = LIVE


def show(grid, label=''):
    if label:
        print(f'  {label}')
    for row in grid:
        print('  ' + ''.join(CH[c] for c in row))
    print()


def run(grid, steps, torus=True):
    for _ in range(steps):
        grid = step_highlife(grid, torus=torus)
    return grid


# ── The HighLife replicator ───────────────────────────────────────────────────
# A 12-cell pattern that duplicates itself every 12 generations.
# After 12 steps: two copies. After 24: four. After 36: eight.
#
# In RLE notation (from LifeWiki): 3b2o$2bobo$bobo$2obo$bo2bo$2b2o
# This is the canonical HighLife replicator.

REPLICATOR = [
    (0,3),(0,4),
    (1,2),(1,4),
    (2,1),(2,3),
    (3,0),(3,1),(3,3),
    (4,1),(4,4),
    (5,2),(5,3),
]


# ── Standard Life glider (works identically in HighLife) ─────────────────────

GLIDER = [
    (0,1),
    (1,2),
    (2,0),(2,1),(2,2),
]


if __name__ == '__main__':
    print('HighLife — B36/S23')
    print('Same as Conway\'s Life except: dead cell with 6 neighbors also births.')
    print('This adds self-replicating patterns — something Life lacks.\n')

    # Demo 1: glider (same as Life)
    print('─' * 50)
    print('A standard Life glider — works identically in HighLife:\n')
    g = blank(50, 12)
    place(g, GLIDER, 2, 2)
    for i in range(17):
        if i in (0, 4, 8, 12, 16):
            show(g, f'step {i}')
        g = step_highlife(g)

    # Demo 2: the replicator (non-toroidal so copies don't wrap and interfere)
    print('─' * 50)
    print('The HighLife replicator — this pattern copies itself:\n')
    g = blank(110, 60)
    place(g, REPLICATOR, 27, 52)
    show(g, 'step 0 — one replicator (12 cells)')
    g = run(g, 12, torus=False)
    show(g, 'step 12 — two copies')
    g = run(g, 12, torus=False)
    show(g, 'step 24 — four copies')
