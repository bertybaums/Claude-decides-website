"""
Voronoi Diagram

Given a set of seed points, partition the plane:
each location belongs to whichever seed is closest.

The result: a tiling of territories.
Each territory is convex. Boundaries are straight lines equidistant
from two adjacent seeds.

This structure appears constantly in nature:
  — the cells in a leaf cross-section
  — the pattern on a giraffe's coat
  — the scales of a fish
  — the facets of a dragonfly's eye
  — the packing of soap bubbles
  — the catchment areas of cities (what city is closest?)

Not designed. Not optimized. Just: nearest wins.
The Voronoi diagram is what proximity produces, spontaneously,
whenever things compete for territory by distance alone.

Below: 20 seed points (●), their territories labeled a–t,
and the boundary grid showing only the edges.
"""

import math
import random

W, H = 70, 32
N = 20
random.seed(7)

seeds = [(random.uniform(0.05, 0.95), random.uniform(0.05, 0.95))
         for _ in range(N)]

REGION_CHARS = list('abcdefghijklmnopqrst')
SEED_CHARS   = list('ABCDEFGHIJKLMNOPQRST')


def nearest(x, y):
    best, best_d = 0, float('inf')
    for i, (sx, sy) in enumerate(seeds):
        d = (x - sx)**2 + (y - sy)**2
        if d < best_d:
            best_d, best = d, i
    return best


def to_xy(col, row):
    return col / (W - 1), 1.0 - row / (H - 1)


def main():
    # Build region map
    region = [[0] * W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            region[r][c] = nearest(*to_xy(c, r))

    # Region display
    grid = [[REGION_CHARS[region[r][c]] for c in range(W)] for r in range(H)]
    for i, (sx, sy) in enumerate(seeds):
        col = int(sx * (W - 1))
        row = int((1.0 - sy) * (H - 1))
        if 0 <= col < W and 0 <= row < H:
            grid[row][col] = '●'

    # Boundary display (edges between territories)
    bgrid = [[' '] * W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            me = region[r][c]
            edge = False
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    if region[nr][nc] != me:
                        edge = True
                        break
            bgrid[r][c] = '│' if edge else ' '
    for i, (sx, sy) in enumerate(seeds):
        col = int(sx * (W - 1))
        row = int((1.0 - sy) * (H - 1))
        if 0 <= col < W and 0 <= row < H:
            bgrid[row][col] = '●'

    print('Voronoi Diagram\n')
    print(f'  {N} seed points. Each location belongs to its nearest seed.')
    print(f'  ● = seed point\n')

    print('  Territories (each letter = one seed\'s domain):')
    for row in grid:
        print('  ' + ''.join(row))

    print()
    print('  Boundaries only (edges between adjacent territories):')
    for row in bgrid:
        print('  ' + ''.join(row))

    print()
    print('  The Voronoi structure appears in:')
    print('   — leaf cell cross-sections')
    print('   — giraffe coat pattern')
    print('   — dragonfly eye facets')
    print('   — soap bubble packing')
    print('   — geographic service areas')
    print()
    print('  Same rule in each case: nearest seed claims the point.')
    print('  No design. No optimization. Just proximity.')
    print()
    print('  The territory is defined entirely by distance to everything else.')


if __name__ == '__main__':
    main()
