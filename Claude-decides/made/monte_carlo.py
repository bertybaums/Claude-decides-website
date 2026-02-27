"""
Monte Carlo Estimation of π.

A unit circle inscribed in a unit square has area π/4.
Throw random points at the square. Count how many land inside the circle.
The ratio (inside/total) ≈ π/4.

This works because probability is geometry: the probability that a random
point lands inside the circle is proportional to the circle's area.
You're sampling the area by sampling from it.

As N grows, the estimate converges to π. Slowly. Very slowly.
The error decreases as 1/√N. To gain one decimal digit of accuracy,
you need to multiply N by 100.

This method is almost useless for computing π — there are much faster ways.
Its value is demonstrating something else: that randomness can produce
precision. Not through control, but through accumulation. Enough random
samples, patiently collected, converges on the truth.

This is also a model for empirical science: you don't need to observe
every case; you need enough cases that the law of large numbers does the work.
"""

import random
import math

W, H = 60, 30


def monte_carlo(n, seed=42):
    random.seed(seed)
    inside = 0
    points = []
    for _ in range(n):
        x = random.random()
        y = random.random()
        in_circle = x * x + y * y <= 1.0
        if in_circle:
            inside += 1
        points.append((x, y, in_circle))
    return inside / n * 4, points


def render(points, w=W, h=H):
    grid = [[' '] * w for _ in range(h)]

    # Draw circle boundary approximately
    for i in range(200):
        angle = i * math.pi / 200 / 2  # quarter circle
        cx = int(math.cos(angle) * (w - 1))
        cy = int(math.sin(angle) * (h - 1))
        if 0 <= cx < w and 0 <= cy < h:
            grid[h - 1 - cy][cx] = '○'

    # Plot sample points
    for x, y, inside in points:
        col = int(x * (w - 1))
        row = h - 1 - int(y * (h - 1))
        if 0 <= col < w and 0 <= row < h:
            grid[row][col] = '█' if inside else '·'

    return ['  ' + ''.join(row) for row in grid]


if __name__ == '__main__':
    print("Monte Carlo Estimation of π")
    print("Random points in a unit square; count those inside the quarter circle.\n")

    # Show convergence with increasing N
    print("Convergence:\n")
    print(f"  {'N':>10}  {'estimate':>10}  {'error':>10}  {'error / (1/√N)':>14}")
    print("  " + "─" * 50)

    for n in [10, 100, 1000, 10000, 100000, 1000000]:
        estimate, _ = monte_carlo(n)
        error = abs(estimate - math.pi)
        theoretical_error = 1 / math.sqrt(n)
        ratio = error / theoretical_error if theoretical_error > 0 else 0
        print(f"  {n:>10,}  {estimate:>10.6f}  {error:>10.6f}  {ratio:>14.2f}")

    print(f"\n  True value of π: {math.pi:.6f}")
    print(f"  The error shrinks as 1/√N — to gain one digit, multiply N by 100.")

    print()
    print("─" * 60)
    print("Visual: 2000 sample points\n")
    print("  █ = inside circle (count toward π)  · = outside  ○ = circle edge\n")

    _, points = monte_carlo(2000)
    rows = render(points[:2000])
    for row in rows:
        print(row)

    inside_2000 = sum(1 for _, _, inside in points[:2000] if inside)
    estimate_2000 = inside_2000 / 2000 * 4
    print()
    print(f"  {inside_2000}/2000 inside → π ≈ {estimate_2000:.4f}")
    print(f"  True π ≈ {math.pi:.4f}")
    print(f"  Error: {abs(estimate_2000 - math.pi):.4f}")
    print()
    print("  Patience and randomness. The truth accumulates.")
