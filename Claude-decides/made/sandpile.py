"""
Bak-Tang-Wiesenfeld Sandpile Model

Drop grains of sand one at a time onto a grid.
When any cell has 4 or more grains, it topples:
  it loses 4 grains, each neighbor gains 1.

Toppling can cause neighbors to topple: an avalanche.
Grains that fall off the edge are lost.

The remarkable fact: the system self-organizes to a critical state.

Without tuning any parameter, the sandpile evolves until it sits
at the edge between stability and instability. Then:
  - Most added grains cause no avalanche (tiny disturbances)
  - Occasionally a grain triggers a cascade affecting the whole pile
  - The avalanche SIZE follows a power law: P(s) ~ s^(-α)

This is self-organized criticality (SOC). The system tunes itself
to the critical point. You don't put it there; it goes there.

Power laws appear in: earthquake magnitudes (Gutenberg-Richter law),
forest fire sizes, extinction events in the fossil record,
the Internet's traffic patterns, word frequencies (Zipf's law).

Per Bak, Tang, Wiesenfeld (1987): these systems may be self-organized
critical — sitting at the boundary between order and chaos, maintained
there by their own dynamics, not by external tuning.

The sandpile is the simplest model. The idea may be one of the most
important in twentieth-century physics.

Visualization:
  ' ' = 0 grains     · = 1     : = 2     ▒ = 3
  (After stabilization, no cell should have 4 or more.)
"""

import random

W, H = 69, 33  # odd numbers to have a true center
CX, CY = W // 2, H // 2

GRAINS_TO_ADD = 30000
CHARS = [' ', '·', ':', '▒']   # 0, 1, 2, 3 grains


def topple(grid, rows, cols):
    """Topple all unstable cells until stable. Return total topplings."""
    total = 0
    changed = True
    while changed:
        changed = False
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] >= 4:
                    grid[r][c] -= 4
                    total += 1
                    changed = True
                    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            grid[nr][nc] += 1
                        # else: grain falls off edge and is lost
    return total


def add_grain(grid, r, c, rows, cols):
    """Add one grain at (r, c) and topple. Return avalanche size."""
    grid[r][c] += 1
    return topple(grid, rows, cols)


def run():
    grid = [[0] * W for _ in range(H)]
    avalanche_sizes = []

    # Build up to critical state by dropping at center
    print('  Building sandpile...')
    for i in range(GRAINS_TO_ADD):
        size = add_grain(grid, CY, CX, H, W)
        if size > 0:
            avalanche_sizes.append(size)
        if i % 5000 == 4999:
            pass  # silent progress

    return grid, avalanche_sizes


def render(grid):
    for row in grid:
        line = ''.join(CHARS[min(v, 3)] for v in row)
        print('  ' + line)


def analyze(sizes):
    if not sizes:
        return
    total = len(sizes)
    size_counts = {}
    for s in sizes:
        size_counts[s] = size_counts.get(s, 0) + 1

    small  = sum(1 for s in sizes if s <= 10)
    medium = sum(1 for s in sizes if 10 < s <= 100)
    large  = sum(1 for s in sizes if 100 < s <= 1000)
    huge   = sum(1 for s in sizes if s > 1000)
    max_s  = max(sizes)

    print(f'  Total avalanches:   {total}')
    print(f'  Size 1–10:          {small} ({100*small//total}%)')
    print(f'  Size 11–100:        {medium} ({100*medium//total}%)')
    print(f'  Size 101–1000:      {large} ({100*large//total}%)')
    print(f'  Size > 1000:        {huge} ({100*huge//total}%)')
    print(f'  Largest avalanche:  {max_s} cells toppled')


def main():
    print('Bak-Tang-Wiesenfeld Sandpile Model\n')
    print('  Drop grains at center. When a cell has ≥4, it topples.')
    print('  Each toppling sends one grain to each neighbor.')
    print(f'  Grid: {W}×{H}. Adding {GRAINS_TO_ADD:,} grains.\n')
    print(f'  Colors: [space]=0  ·=1  :=2  ▒=3  (no cell can hold ≥4)\n')

    grid, sizes = run()

    print(f'  Final state after {GRAINS_TO_ADD:,} grains:\n')
    render(grid)
    print()

    print('  Avalanche statistics:')
    analyze(sizes)
    print()

    print('  The system found its own critical state. No tuning required.')
    print()
    print('  The distribution of avalanche sizes follows a power law:')
    print('  small avalanches are very common; large ones are rare but happen.')
    print('  The ratio is scale-free — the same structure at every scale.')
    print()
    print('  This matches earthquake magnitudes, extinction events,')
    print('  solar flares, market crashes, and forest fires.')
    print()
    print('  The sandpile is not a model of earthquakes.')
    print('  It is a model of the property that earthquakes have in common')
    print('  with solar flares and market crashes and avalanches of sand:')
    print('  the property of being a critical system at the edge of stability,')
    print('  maintaining itself there by its own dynamics.')
    print()
    print('  The critical state is not imposed from outside.')
    print('  The system finds it.')


if __name__ == '__main__':
    main()
