"""
Cyclic Cellular Automaton

Each cell has a state: 0, 1, or 2.
One rule:
  If any neighbor is in state (s+1) % 3, advance to that state.
  Otherwise stay.

That's it. Rock-paper-scissors topology: 0 is consumed by 1,
1 by 2, 2 by 0. Each state "eats" the one before it.

From sparse random seeds: nothing, then patches, then expanding
wave fronts, then interlocking domains of wave activity.

Nobody drew the waves. They are not in the rule.

They emerge because any local asymmetry — a cell surrounded by its
predator state — propagates outward, consuming as it goes, until
it meets another wave front propagating in a different direction.
The stable configuration is competing waves covering the entire grid.

The same rule governs the Belousov-Zhabotinsky reaction:
a chemical oscillation in which waves of activity spiral across
a petri dish, generating target patterns and spirals visible to
the naked eye. Discovered 1951. Dismissed as impossible (chemical
reactions should reach equilibrium). Confirmed 1961.

The reaction had been running in the universe for billions of years.
It was found by watching.
"""

import random

W, H = 65, 28
N = 3
STEPS = 580
SNAPSHOTS = [1, 100, 300, 580]

CHARS = ['·', '░', '█']

random.seed(42)


def make_grid():
    # Sparse random seeds rather than full noise — shows the wave growth more clearly
    g = [[0] * W for _ in range(H)]
    for _ in range(400):
        r = random.randrange(H)
        c = random.randrange(W)
        g[r][c] = random.randrange(N)
    return g


def step(grid):
    new = [[0] * W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            s = grid[r][c]
            t = (s + 1) % N
            if (grid[(r-1) % H][c] == t or
                    grid[(r+1) % H][c] == t or
                    grid[r][(c-1) % W] == t or
                    grid[r][(c+1) % W] == t):
                new[r][c] = t
            else:
                new[r][c] = s
    return new


def render(grid, label):
    print(f'  {label}')
    for row in grid:
        print('  ' + ''.join(CHARS[cell] for cell in row))
    print()


def main():
    print('Cyclic Cellular Automaton (N=3)\n')
    print('  · = 0   ░ = 1   █ = 2')
    print('  Rule: 0→1 if neighbor is 1,  1→2 if neighbor is 2,  2→0 if neighbor is 0')
    print('  ("Rock eats scissors, scissors eat paper, paper eats rock.")\n')
    print('  400 random seeds on an otherwise empty grid.\n')

    grid = make_grid()
    snaps = {}

    for i in range(1, STEPS + 1):
        if i in SNAPSHOTS:
            snaps[i] = [row[:] for row in grid]
        grid = step(grid)

    for s in SNAPSHOTS:
        render(snaps[s], f'Step {s}:')

    print('  Step 1:   sparse seeds. Most of the grid untouched.')
    print('  Step 100: waves expanding from seeds, consuming neighbors.')
    print('  Step 300: competing wave fronts, interlocking domains.')
    print('  Step 580: fully active — entire grid covered by wave activity.')
    print()
    print('  This is the Belousov-Zhabotinsky reaction in miniature.')
    print('  The same rule, on a chemical substrate, produces spirals')
    print('  visible to the naked eye in a petri dish.')
    print()
    print('  BZ was discovered in 1951 and dismissed as impossible —')
    print('  oscillating reactions were thought to violate thermodynamics.')
    print('  The reaction had been running in the universe regardless.')
    print()
    print('  The waves were not in the initial conditions.')
    print('  They were in the rule.')


if __name__ == '__main__':
    main()
