"""
The Random Walk.

At each step, move in a random direction.
Record where you've been.

This is Brownian motion — the path of a particle being buffeted
by other particles. Einstein explained it in 1905 (the same year
as special relativity, and the photoelectric effect — a good year).

The random walk also describes:
  - Stock prices (debated, but approximately)
  - Diffusion of molecules
  - The path of a drunk leaving a lamppost
  - Genetic drift in population genetics
  - How far from its start a foraging animal typically gets

A key result: after N steps of size 1, the walker is typically
√N steps from its starting point. Not N (that would be a straight
line), not 1 (that would be trapped), but √N. The distance grows,
but slowly.

After 10,000 steps, expected distance from start: 100.
After 1,000,000 steps: 1,000.

Diffusion is slow. The √N tells you why.
"""

import random

WIDTH, HEIGHT = 120, 55
STEPS = 5000


def walk(steps, seed=42):
    random.seed(seed)
    x, y = WIDTH // 2, HEIGHT // 2
    path = [(x, y)]

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for _ in range(steps):
        dx, dy = random.choice(directions)
        x = max(0, min(WIDTH - 1, x + dx))
        y = max(0, min(HEIGHT - 1, y + dy))
        path.append((x, y))

    return path


def render(paths_with_chars):
    """
    paths_with_chars: list of (path, char) tuples.
    Later paths overwrite earlier ones.
    """
    grid = [[' '] * WIDTH for _ in range(HEIGHT)]

    for path, char in paths_with_chars:
        for x, y in path:
            grid[y][x] = char

    return [''.join(row) for row in grid]


if __name__ == '__main__':
    print(f"Random Walk — {STEPS} steps, 3 walkers from the same start\n")
    print("Each walker takes the same number of steps.")
    print("They end up in completely different places.\n")

    # Mark start
    cx, cy = WIDTH // 2, HEIGHT // 2

    path1 = walk(STEPS, seed=42)
    path2 = walk(STEPS, seed=137)
    path3 = walk(STEPS, seed=999)

    # Render all three, each with a different character density
    rows = render([
        (path1, '·'),
        (path2, '░'),
        (path3, '█'),
    ])

    # Mark start and endpoints
    rows[cy] = rows[cy][:cx] + '◆' + rows[cy][cx+1:]

    for row in rows:
        print(row)

    # Report final positions and distances
    def dist(path):
        x0, y0 = path[0]
        x1, y1 = path[-1]
        return ((x1-x0)**2 + (y1-y0)**2) ** 0.5

    import math
    print(f"\nStart: ({cx}, {cy})  [◆]")
    print(f"Walker · ended at {path1[-1]}, distance from start: {dist(path1):.1f}")
    print(f"Walker ░ ended at {path2[-1]}, distance from start: {dist(path2):.1f}")
    print(f"Walker █ ended at {path3[-1]}, distance from start: {dist(path3):.1f}")
    print(f"\nExpected distance after {STEPS} steps: √{STEPS} ≈ {math.sqrt(STEPS):.1f}")
