"""
Barnsley's Fern.

Four affine transformations. Applied randomly, with specific probabilities.
The result: a fern.

Not approximately a fern. Not fern-like. A fern — the specific geometry
of a fern leaf, with fronds, sub-fronds, the main stem, the characteristic
curl at the tip. Produced by four matrix operations.

Michael Barnsley proved in 1988 that natural forms can be encoded
as Iterated Function Systems — small sets of transformations whose
repeated application converges to the shape. The fern is the simplest example.

The transformations:
  f₁ (prob 1%):  maps everything to the stem (a near-vertical line segment)
  f₂ (prob 85%): the main transformation — produces the large-scale fern shape
  f₃ (prob 7%):  produces the right frond
  f₄ (prob 7%):  produces the left frond

At each step, pick a transformation randomly (with the given probabilities).
Apply it to the current point. Plot the point.
After enough iterations, the plotted points form the fern.

This is the strange economy of fractals: the fern is four matrix equations.
The equations ARE the fern, in some deep sense. The fern you see in a forest
is a particular physical instance of something that can be stated in forty numbers.
"""

import random

# Canvas
W, H = 65, 55
N_POINTS = 120000

# Barnsley fern transformations: (a, b, c, d, e, f, probability)
# x_new = a*x + b*y + e
# y_new = c*x + d*y + f
TRANSFORMS = [
    ( 0.00,  0.00,  0.00,  0.16, 0.00, 0.00, 0.01),  # stem
    ( 0.85,  0.04, -0.04,  0.85, 0.00, 1.60, 0.85),  # main body
    ( 0.20, -0.26,  0.23,  0.22, 0.00, 1.60, 0.07),  # right frond
    (-0.15,  0.28,  0.26,  0.24, 0.00, 0.44, 0.07),  # left frond
]


def pick_transform():
    r = random.random()
    cumulative = 0.0
    for *coeffs, prob in TRANSFORMS:
        cumulative += prob
        if r < cumulative:
            return coeffs
    return TRANSFORMS[-1][:-1]


def iterate(n_points):
    x, y = 0.0, 0.0
    points = []
    for _ in range(n_points):
        a, b, c, d, e, f = pick_transform()
        x, y = a * x + b * y + e, c * x + d * y + f
        points.append((x, y))
    return points


def render(points, w=W, h=H):
    # Find bounding box
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    # Add margin
    x_margin = (x_max - x_min) * 0.05
    y_margin = (y_max - y_min) * 0.02
    x_min -= x_margin; x_max += x_margin
    y_min -= y_margin; y_max += y_margin

    grid = [[' '] * w for _ in range(h)]
    for x, y in points:
        col = int((x - x_min) / (x_max - x_min) * (w - 1))
        row = int((y_max - y) / (y_max - y_min) * (h - 1))
        if 0 <= col < w and 0 <= row < h:
            grid[row][col] = '█'

    return grid


if __name__ == '__main__':
    random.seed(42)

    print("Barnsley's Fern — Iterated Function System")
    print("Four matrix transformations. Applied randomly. Result: a fern.\n")

    points = iterate(N_POINTS)
    grid = render(points)

    for row in grid:
        print('  ' + ''.join(row))

    print()
    print(f"  {N_POINTS:,} points. Four transformations. One fern.")
    print()
    print("  The fern is the attractor of this system:")
    print("  the set all trajectories converge to, regardless of starting point.")
    print()
    print("  The fern encodes itself. Start anywhere; arrive at the same shape.")
    print("  This is what it means for something to have a nature.")
