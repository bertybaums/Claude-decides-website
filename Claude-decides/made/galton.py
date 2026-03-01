"""
Galton Board — How Randomness Produces Regularity

The Galton board (or bean machine) was invented by Francis Galton in 1894.
A ball falls through rows of pegs. At each peg, it bounces left or right
with equal probability (50/50). After n rows, the ball ends in one of n+1 slots.

The number of left-or-right choices is a sequence of n coin flips.
The final position = number of rightward deflections = Binomial(n, 0.5).

With many balls:
  - The distribution approaches a normal (Gaussian) curve
  - Standard deviation = sqrt(n/4) = sqrt(n)/2
  - Mean = n/2 (center of the board)

Why this matters:
  - It makes the Central Limit Theorem *visible*
  - Galton designed it to demonstrate that hereditary traits follow the normal curve
  - It shows that complex outcomes can arise from simple random steps
  - The structure (binomial → normal) is universal: it appears whenever many
    small independent random effects add up

Related: Pascal's triangle
  The number of paths through the pegs to each slot
  is exactly the binomial coefficient C(n, k).
  The board's bins fill in proportion to C(n, k) / 2^n.

Historical note:
  Galton called it a "quincunx" (from the Latin for the 5-dot pattern on dice).
  He used it to argue that regression to the mean was a natural law.
  He was trying to understand why the children of tall parents
  tend to be closer to average height than their parents.
  He found the answer in the normal distribution and its properties.
"""

import random
import math
from collections import Counter


def drop_ball(n_rows):
    """Drop one ball through n_rows of pegs. Return final slot (0 to n_rows)."""
    pos = 0
    for _ in range(n_rows):
        pos += random.randint(0, 1)
    return pos


def run_simulation(n_rows, n_balls):
    """Simulate n_balls falling through n_rows of pegs."""
    counts = Counter(drop_ball(n_rows) for _ in range(n_balls))
    return counts


def render_board(n_rows, width=60):
    """Render the Galton board structure (just the pegs)."""
    print(f'  Galton board: {n_rows} rows of pegs')
    print()
    for row in range(n_rows + 1):
        # Spacing: center the row
        n_pegs = row + 1
        total_width = n_rows * 2 + 1
        start = (total_width - (n_pegs * 2 - 1)) // 2
        line = ' ' * start
        for p in range(n_pegs):
            line += '●'
            if p < n_pegs - 1:
                line += ' '
        print(f'  {line}')
    print()


def render_histogram(counts, n_rows, n_balls, width=50):
    """Render the results as a histogram with normal curve overlay."""
    max_count = max(counts.values()) if counts else 1
    mu = n_rows / 2
    sigma = math.sqrt(n_rows / 4)

    print(f'  Distribution after {n_balls} balls through {n_rows} rows:')
    print(f'  Expected: N(μ={mu:.1f}, σ={sigma:.2f})')
    print()

    for slot in range(n_rows + 1):
        count = counts.get(slot, 0)
        # Actual bar
        bar_len = int(count / max_count * width)
        bar = '█' * bar_len

        # Normal distribution value at this slot
        normal_p = math.exp(-0.5 * ((slot - mu) / sigma) ** 2) / (sigma * math.sqrt(2 * math.pi))
        normal_count = normal_p * n_balls
        norm_len = int(normal_count / max_count * width)
        norm_mark = '|' if norm_len < width else '│'

        # Overlay: show actual bar, mark expected position
        pct = count / n_balls * 100
        print(f'  [{slot:>3}]  {bar:<{width}} {count:>5} ({pct:>4.1f}%)')

    print()

    # Statistics
    actual_mean = sum(slot * count for slot, count in counts.items()) / n_balls
    actual_var = sum(count * (slot - actual_mean) ** 2 for slot, count in counts.items()) / n_balls
    actual_std = math.sqrt(actual_var)
    print(f'  Actual:   mean={actual_mean:.2f}  std={actual_std:.2f}')
    print(f'  Expected: mean={mu:.2f}  std={sigma:.2f}')


def show_binomial_coefficients(n_rows):
    """Show Pascal's triangle row and path counts."""
    print(f'  Paths through {n_rows} rows (Pascal\'s row {n_rows}):')
    total = 2 ** n_rows
    row = []
    for k in range(n_rows + 1):
        # C(n, k)
        c = math.comb(n_rows, k)
        row.append(c)

    print()
    print('  Slot   Paths    Probability   Pascal')
    print('  ' + '-' * 45)
    for k, c in enumerate(row):
        prob = c / total
        bar_len = int(prob * 20)
        bar = '█' * bar_len
        print(f'  [{k:>3}]  {c:>6}   {prob:>8.4f}    {bar}')
    print()
    print(f'  Total paths: {total} = 2^{n_rows}')
    print(f'  Sum of Pascal row: {sum(row)} = {total} ✓')


def show_convergence():
    """Show how the distribution converges to normal as n_rows increases."""
    print('  ─── CONVERGENCE TO NORMAL ───\n')
    print('  As rows increase, the binomial distribution approaches Gaussian.')
    print('  Normalized distributions (each scaled to same max height):\n')

    n_balls = 2000
    display_width = 40

    for n_rows in [4, 8, 16, 32]:
        counts = run_simulation(n_rows, n_balls)
        max_count = max(counts.values())

        # Print compressed version (only center 30 slots if large)
        mu = n_rows / 2
        sigma = math.sqrt(n_rows / 4)

        print(f'  {n_rows} rows (σ={sigma:.1f}):')
        for slot in range(n_rows + 1):
            count = counts.get(slot, 0)
            bar_len = int(count / max_count * display_width)
            # Only print slots within ±3σ of mean
            if abs(slot - mu) <= 3 * sigma + 0.5:
                bar = '█' * bar_len
                print(f'    [{slot:>3}] {bar}')
        print()


def main():
    random.seed(42)

    print('Galton Board — Randomness Producing Regularity\n')
    print('  Each ball: n coin flips → slot k = number of rightward deflections')
    print('  Many balls: Binomial(n, 0.5) → Normal curve\n')

    # Show board structure
    print('  ─── BOARD STRUCTURE (n=8 rows) ───\n')
    render_board(8)

    # Show path counts
    print('  ─── PATH COUNTING: PASCAL\'S TRIANGLE ───\n')
    show_binomial_coefficients(8)

    # Simulate and render
    print('  ─── SIMULATION: 1000 balls, 12 rows ───\n')
    n_rows = 12
    n_balls = 1000
    counts = run_simulation(n_rows, n_balls)
    render_histogram(counts, n_rows, n_balls)

    # Convergence
    show_convergence()

    print('  ─── GALTON\'S INSIGHT ───\n')
    print('  Galton designed this board to explain regression to the mean.')
    print('  Tall parents → tall children on average, but less extreme than parents.')
    print('  Short parents → short children on average, but less extreme than parents.')
    print('  Any individual\'s height is the sum of many small independent factors.')
    print('  Many independent small factors → normal distribution → regression to mean.')
    print()
    print('  The same structure appears in:')
    print('  - Measurement error (sum of many small instrument errors)')
    print('  - Stock returns (sum of many small random shocks)')
    print('  - Human traits (sum of many genetic and environmental factors)')
    print('  - Exam scores (sum of many items, each partially right)')
    print()
    print('  The Galton board makes the central limit theorem visible.')
    print('  The normal curve is not a thing in the world.')
    print('  It is what many independent random processes converge to.')
    print('  The board shows you why.')


if __name__ == '__main__':
    main()
