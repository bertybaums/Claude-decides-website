"""
The Chaos Game: Sierpinski Triangle from Pure Randomness

Rules:
  1. Pick three vertices of a triangle: A, B, C.
  2. Start at a random point.
  3. Repeat:
       - Choose one of the three vertices at random.
       - Move halfway from your current position to that vertex.
       - Mark the new position.

That's it. Two lines of logic. No triangle built into the rules.

After a few points, the result is the Sierpinski triangle —
a fractal with infinitely nested structure, composed of three
copies of itself at every scale.

The triangle does not appear in the rules.
It appears in the iteration of the rules.

Nobody designed the Sierpinski triangle into the chaos game.
It is what the rules imply, revealed by running them.

This is emergence in its purest form: the pattern is not in
the description. The description is just: pick randomly, move halfway.
The pattern is what the description does.
"""

import random

W, H = 75, 38

# Three vertices of a triangle (in [0,1] coordinates)
VERTICES = [
    (0.5,  1.0),   # top
    (0.0,  0.0),   # bottom-left
    (1.0,  0.0),   # bottom-right
]

POINTS = 50_000
random.seed(7)


def to_screen(x, y):
    col = int(x * (W - 1))
    row = int((1.0 - y) * (H - 1))
    return col, row


def main():
    grid = [[False] * W for _ in range(H)]

    # Start anywhere
    px, py = 0.5, 0.5

    # Warm up (first few points don't lie on the attractor)
    for _ in range(20):
        vx, vy = random.choice(VERTICES)
        px = (px + vx) / 2
        py = (py + vy) / 2

    # Generate and plot
    for _ in range(POINTS):
        vx, vy = random.choice(VERTICES)
        px = (px + vx) / 2
        py = (py + vy) / 2
        col, row = to_screen(px, py)
        if 0 <= col < W and 0 <= row < H:
            grid[row][col] = True

    print("The Chaos Game — Sierpinski Triangle\n")
    print(f"  {POINTS:,} points plotted.")
    print("  Each point: pick a random vertex, move halfway.\n")

    for row in grid:
        print("  " + "".join("*" if cell else " " for cell in row))

    print()
    print("  The Sierpinski triangle:")
    print("  - Three copies of itself at every scale")
    print("  - Fractal dimension ≈ 1.585 (between a line and a plane)")
    print("  - Area = 0. Perimeter = infinite.")
    print()
    print("  The rules contain none of this.")
    print("  They say only: choose randomly, move halfway.")
    print()
    print("  The triangle is what the rules are.")
    print("  The rules are not what the triangle is.")
    print()
    print("  The description and the thing are the same size.")
    print("  But the description fits in two sentences.")
    print("  The thing doesn't.")


if __name__ == "__main__":
    main()
