"""
Fourier Series: Building a Square Wave from Sines

A square wave alternates between +1 and -1.
It has sharp corners — discontinuities at every half-period.
A sine wave is smooth — no discontinuities at all.

Can you build a square wave from sine waves?

Answer: almost. The Fourier series for a square wave is:

  f(x) = (4/π) * [ sin(x)/1 + sin(3x)/3 + sin(5x)/5 + sin(7x)/7 + ... ]

Only odd harmonics. Each one weaker than the last by its harmonic number.

With enough terms, the sum approaches the square wave — except
at the discontinuities, where a small overshoot persists no matter
how many terms you add. About 9% of the jump, always. Forever.

This is the Gibbs phenomenon: an infinite sum that converges
everywhere except at the one place you most care about.

The square wave is the limit. The limit is never reached.

---

Below: the square wave approximated by 1, 3, 7, 15, and 31 harmonics.
Watch the corners sharpen and the Gibbs spikes form.
"""

import math

W = 80       # columns per row
H = 9        # rows per waveform
HARMONICS = [1, 3, 7, 15, 31]
SAMPLES = 800


def square_wave(x):
    """The target: +1 for 0 < x < π, -1 for π < x < 2π."""
    return 1.0 if (x % (2 * math.pi)) < math.pi else -1.0


def fourier_approx(x, n_harmonics):
    """Sum of first n_harmonics odd-harmonic terms."""
    total = 0.0
    for k in range(1, n_harmonics + 1):
        term = 2 * k - 1          # 1, 3, 5, 7, ...
        total += math.sin(term * x) / term
    return (4 / math.pi) * total


def render_wave(values, label):
    """Render a waveform as ASCII art."""
    grid = [[' '] * W for _ in range(H)]

    # Draw the zero line
    mid = H // 2
    for c in range(W):
        grid[mid][c] = '─'

    # Plot the waveform
    for i, v in enumerate(values):
        col = int(i / len(values) * W)
        row = int((1.0 - v) / 2.0 * (H - 1))
        row = max(0, min(H - 1, row))
        if 0 <= col < W:
            grid[row][col] = '·' if grid[row][col] == ' ' else '│'

    # Also draw the ideal square wave faintly
    for i in range(len(values)):
        col = int(i / len(values) * W)
        x = 2 * math.pi * i / len(values)
        sv = square_wave(x)
        srow = int((1.0 - sv) / 2.0 * (H - 1))
        srow = max(0, min(H - 1, srow))
        if 0 <= col < W and grid[srow][col] == ' ':
            grid[srow][col] = '▪'

    print(f'  {label}')
    for row in grid:
        print('  ' + ''.join(row))
    print()


def main():
    xs = [2 * math.pi * i / SAMPLES for i in range(SAMPLES)]
    ideal = [square_wave(x) for x in xs]

    print('Fourier Series: Square Wave from Sines\n')
    print('  f(x) = (4/π) · [ sin(x)/1 + sin(3x)/3 + sin(5x)/5 + ... ]\n')
    print('  · = Fourier approximation   ▪ = target square wave\n')

    for n in HARMONICS:
        values = [fourier_approx(x, n) for x in xs]
        term_str = 'term' if n == 1 else 'terms'
        render_wave(values, f'{n} odd-harmonic {term_str}')

    # Show error at the jump
    print('  Error at the discontinuity (Gibbs phenomenon):')
    print()
    print('  No matter how many terms you add, a spike persists')
    print('  at each jump: roughly 9% of the step height, always.')
    print()
    for n in HARMONICS:
        # The overshoot occurs just before x=π
        # Sample near x = π - ε
        best_max = max(fourier_approx(math.pi * i / 1000, n) for i in range(1, 1000))
        overshoot = (best_max - 1.0) / 2.0 * 100
        bar = '█' * int(overshoot / 0.5)
        print(f'  {n:>2} harmonics  overshoot: {overshoot:4.1f}%  {bar}')

    print()
    print('  The square wave is the limit of the Fourier series.')
    print('  The limit is never reached at the discontinuity.')
    print()
    print('  A timbre is a Fourier series in time.')
    print('  The sharpness of a clarinet vs. a flute is in the harmonic mix.')
    print('  A square wave sounds like a clarinet (odd harmonics dominate).')
    print('  A sawtooth like a violin (all harmonics).')
    print()
    print('  The overtone series is not decoration.')
    print('  It is the sound.')


if __name__ == '__main__':
    main()
