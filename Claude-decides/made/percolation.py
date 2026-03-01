"""
Percolation

Each cell is open (passable) with probability p, blocked otherwise.
Is there a connected path from the top row to the bottom row?

At low p: no path. Everything blocked.
At high p: paths everywhere.
At the critical threshold pc ≈ 0.5927 (for square lattice, site percolation):
  the first connected path just barely appears.
  Below pc: no crossing. Above pc: crossing almost certainly exists.

This is a phase transition. The order parameter (probability of crossing)
jumps from 0 to nonzero at pc, with the characteristic divergence of
connected cluster sizes at the critical point.

Applications:
  - Forest fires (pc = fraction of trees; fire spreads if p > pc)
  - Epidemics (pc = transmission probability; epidemic if p > pc)
  - Porous materials (oil, water through rock)
  - Electrical conductivity in composite materials
  - The giant connected component in random graphs (Erdős-Rényi)
  - Neural avalanches (brain activity propagation)

At pc: the spanning cluster has fractal dimension ≈ 1.89 (in 2D).
       Clusters exist at every scale simultaneously.
       Scale-invariant, like the Ising model at Tc.
       Not a coincidence — they're in the same universality class.

Flood-fill algorithm to find connected clusters:
  Start from all open cells in the top row.
  Explore neighbors. If we reach the bottom row: percolating cluster found.
"""

import random

W, H = 70, 28

# Site percolation threshold for square lattice
PC = 0.5927

PROBABILITIES = [0.30, 0.50, PC, 0.65, 0.85]

SEED = 42


def make_grid(p, rows, cols, seed):
    rng = random.Random(seed)
    return [[rng.random() < p for _ in range(cols)] for _ in range(rows)]


def find_percolating_cluster(grid, rows, cols):
    """
    BFS flood-fill from all open top-row cells.
    Returns (set of visited cells, did_percolate).
    """
    from collections import deque

    visited = set()
    queue = deque()

    # Seed from all open cells in top row
    for c in range(cols):
        if grid[0][c] and (0, c) not in visited:
            visited.add((0, c))
            queue.append((0, c))

    percolates = any(grid[0][c] for c in range(cols))

    percolating_cluster = set()
    reached_bottom = False

    while queue:
        r, c = queue.popleft()
        if r == rows - 1:
            reached_bottom = True

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if grid[nr][nc]:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    return visited, reached_bottom


def render(grid, visited, percolated, rows, cols):
    lines = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if grid[r][c]:
                if (r, c) in visited:
                    if percolated:
                        row.append('█')   # Part of spanning cluster
                    else:
                        row.append('▓')   # Open but no spanning path found
                else:
                    row.append('░')       # Open but isolated
            else:
                row.append('·')           # Blocked
        lines.append(''.join(row))
    return lines


def main():
    print('Percolation — Connected Paths Through Random Media\n')
    print('  · = blocked cell        ░ = open, isolated cluster')
    print('  ▓ = open, largest cluster (no crossing)  █ = percolating path\n')
    print(f'  Critical threshold for square lattice: pc ≈ {PC}\n')
    print('  Does a connected path exist from TOP to BOTTOM?\n')

    for p in PROBABILITIES:
        grid = make_grid(p, H, W, SEED)
        visited, percolated = find_percolating_cluster(grid, H, W)
        lines = render(grid, visited, percolated, H, W)

        open_frac = sum(grid[r][c] for r in range(H) for c in range(W)) / (H * W)

        if p == PC:
            label = f'p = {p:.4f} (≈ pc — critical threshold)'
        else:
            label = f'p = {p:.2f}'

        status = 'PERCOLATES ↓' if percolated else 'DOES NOT PERCOLATE'

        print(f'  {label}   →   {status}')
        print(f'  Open cells: {100*open_frac:.1f}%\n')

        for line in lines:
            print('  ' + line)
        print()

    print('  The transition from "never crosses" to "always crosses" is abrupt.')
    print('  At pc: the crossing probability jumps from 0 to nonzero.')
    print()
    print('  At pc: clusters exist at every scale — fractal structure.')
    print('  Same universality class as the Ising model at Tc.')
    print('  Same universality class as the liquid-gas critical point.')
    print()
    print('  The microscopic details differ. The critical behavior: the same.')
    print()
    print('  Below pc: fire goes out. Above pc: fire spreads to everything.')
    print('  At exactly pc: the fire reaches the edge, barely.')


if __name__ == '__main__':
    main()
