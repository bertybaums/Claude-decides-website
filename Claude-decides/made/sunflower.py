"""
Phyllotaxis — How Plants Count.

Plants arrange their seeds, leaves, and petals using the golden angle:
    137.508°  =  360° × (1 - 1/φ)   where φ = (1+√5)/2 ≈ 1.618

Place the nth seed at angle n × 137.508° and radius √n from center.
The result: the familiar spirals of a sunflower, pinecone, or daisy.

Why this angle? It's the "most irrational" angle — the one hardest to
approximate with fractions. This means seeds never line up in straight
rows, always filling gaps, packing as efficiently as possible.

Evolution discovered this. It didn't need to know about the golden ratio.
It just needed to solve the packing problem over many generations, and
this is the solution the problem has.

The spirals you see — 21 going one way, 34 the other, or 34 and 55,
or 55 and 89 — are always consecutive Fibonacci numbers.
The golden angle produces Fibonacci numbers as a side effect.

Look for the spirals.
"""

import math

GOLDEN_ANGLE = math.radians(137.50776)
N_SEEDS = 600
WIDTH, HEIGHT = 120, 60

# Characters by "depth" from center
CHARS = '·∘○◎●'


def place_seeds(n, width, height):
    cx, cy = width / 2, height / 2
    scale = min(width, height) * 0.45

    cells = {}
    for i in range(1, n + 1):
        angle = i * GOLDEN_ANGLE
        r = math.sqrt(i) / math.sqrt(n) * scale
        x = int(cx + r * math.cos(angle) * 1.0)       # no x-stretch needed
        y = int(cy + r * math.sin(angle) * 0.55)      # compress y for terminal aspect ratio
        depth = i / n   # 0=center, 1=edge
        cells[(x, y)] = depth

    return cells


def render(cells, width, height):
    grid = [[' '] * width for _ in range(height)]
    for (x, y), depth in cells.items():
        if 0 <= x < width and 0 <= y < height:
            idx = int(depth * (len(CHARS) - 1))
            # If two seeds map to same cell, prefer the denser character
            current = grid[y][x]
            candidate = CHARS[idx]
            if current == ' ' or CHARS.index(candidate) > CHARS.index(current):
                grid[y][x] = candidate
    return [''.join(row) for row in grid]


if __name__ == '__main__':
    print(f"Phyllotaxis — {N_SEEDS} seeds, golden angle = 137.508°")
    print("Symbols: · (center) → ● (edge)")
    print("Look for the diagonal spirals — they run in Fibonacci pairs.\n")
    cells = place_seeds(N_SEEDS, WIDTH, HEIGHT)
    for row in render(cells, WIDTH, HEIGHT):
        print(row)
