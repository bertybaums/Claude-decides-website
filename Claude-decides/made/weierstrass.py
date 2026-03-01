"""
Weierstrass Function

f(x) = Σ aⁿ · cos(bⁿ · π · x),   n = 0, 1, 2, ...

where a = 0.85, b = 7  (ab ≈ 5.95 > 1 + 3π/2 ≈ 5.71 ✓)

This function is:
  — continuous everywhere  (no breaks, no jumps, you can draw it)
  — differentiable nowhere (at every point, the slope is undefined)

Before Weierstrass (1872), mathematicians assumed that a continuous
function must be smooth "almost everywhere" — that continuity and
differentiability were nearly the same thing. He shocked everyone by
producing a function that is continuous everywhere and smooth nowhere.

The function is a sum of cosines at increasing frequencies (×b each term)
and decreasing amplitudes (×a each term). Each term adds faster oscillations
on top of slower ones. At the limit, the oscillations are infinitely fast at
every scale — the function has no tangent anywhere.

Below: partial sums with 1, 2, 3, 5, and 10 terms.
Each new term adds finer and finer roughness.
At 10 terms, the additional terms are too fine to see at this resolution.
The function continues adding structure below our visual threshold.
"""

import math

a = 0.85
b = 7
W = 78
H = 13
SAMPLES = W * 4


def f(x, n_terms):
    return sum(a**n * math.cos(b**n * math.pi * x) for n in range(n_terms))


def plot(n_terms):
    xs = [i / (SAMPLES - 1) * 2 for i in range(SAMPLES)]  # x in [0, 2]
    ys = [f(x, n_terms) for x in xs]

    y_min, y_max = min(ys), max(ys)
    y_range = y_max - y_min or 1.0

    grid = [[' '] * W for _ in range(H)]

    # Zero line
    zero_row = int((y_max - 0) / y_range * (H - 1))
    zero_row = max(0, min(H - 1, zero_row))
    for c in range(W):
        grid[zero_row][c] = '─'

    # Plot the function
    prev_row = None
    for i in range(SAMPLES):
        col = int(i / SAMPLES * W)
        col = min(W - 1, col)
        y = ys[i]
        row = int((y_max - y) / y_range * (H - 1))
        row = max(0, min(H - 1, row))

        grid[row][col] = '·'

        # Connect to previous point vertically if gap
        if prev_row is not None and abs(row - prev_row) > 1:
            for r in range(min(row, prev_row) + 1, max(row, prev_row)):
                if 0 <= r < H:
                    grid[r][col] = '│'
        prev_row = row

    return grid, y_min, y_max


def main():
    print('Weierstrass Function:  f(x) = Σ aⁿ·cos(bⁿπx)')
    print(f'  a = {a},  b = {b},  x ∈ [0, 2]\n')
    print('  Continuous everywhere.  Differentiable nowhere.\n')

    for n_terms in [1, 2, 3, 5, 10]:
        grid, y_min, y_max = plot(n_terms)
        term_word = 'term' if n_terms == 1 else 'terms'
        freqs = [f'b^{n}π = {b**n}π' for n in range(min(n_terms, 3))]
        print(f'  {n_terms} {term_word}   (highest frequency: {b**(n_terms-1)}π)')
        for row in grid:
            print('  ' + ''.join(row))
        print()

    print('  After 3 terms, each new term oscillates too fast to see here.')
    print('  The function keeps adding roughness at finer and finer scales.')
    print()
    print('  Weierstrass (1872): continuous everywhere, differentiable nowhere.')
    print('  The mathematical community considered this pathological.')
    print('  Hermite called it "a lamentable evil."')
    print()
    print('  Later: it was found that "most" continuous functions')
    print('  share this property. The smooth functions are the exception.')
    print()
    print('  The monster was the normal case.')


if __name__ == '__main__':
    main()
