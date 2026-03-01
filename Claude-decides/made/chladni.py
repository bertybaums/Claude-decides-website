"""
Chladni Figures

In 1787, Ernst Chladni discovered that bowing a metal plate covered in sand
produced beautiful geometric patterns. When the plate vibrates at a resonant
frequency, some points stay still (nodes) and some move wildly (antinodes).
Sand gathers at the nodes.

The pattern is determined by the mode of vibration — characterized by two
integers (m, n), counting the number of nodal lines in each direction.

For a square plate with free edges, the vibrational modes are approximately:
  f(x, y) = cos(m·π·x) · cos(n·π·y) ± cos(n·π·x) · cos(m·π·y)

The sand gathers where f(x, y) ≈ 0 — the nodal lines.
The plate oscillates between +f and −f. Where f = 0, nothing moves.

Chladni demonstrated these to Napoleon in 1809. Napoleon was impressed.
He offered a prize for a mathematical explanation.
Sophie Germain attempted a solution. She was wrong three times.
On the fourth attempt (with significant help from Lagrange on boundary
conditions), she was correct. She remains one of the first women to win
the prize of the French Academy of Sciences.

The modern theory was completed by Kirchhoff in 1850.

The patterns are:
  (m=1, n=2): simple cross
  (m=1, n=3): more complex, six regions
  (m=2, n=3): star-like
  (m=3, n=4): intricate grid
  (m=1, n=4) with + combination: 8 regions
  (m=2, n=5): complex with many nodes
"""

import math

W, H = 71, 35


def chladni(m, n, sign, x, y):
    """Chladni mode function for square plate."""
    # x, y in [0, 1]
    return (math.cos(m * math.pi * x) * math.cos(n * math.pi * y) +
            sign * math.cos(n * math.pi * x) * math.cos(m * math.pi * y))


def render(m, n, sign, threshold=0.12):
    """Render a Chladni figure. Nodal lines (f≈0) are where sand collects."""
    grid = [[' '] * W for _ in range(H)]

    max_val = 0.0
    values = []
    for row in range(H):
        row_vals = []
        for col in range(W):
            x = col / (W - 1)
            y = row / (H - 1)
            v = abs(chladni(m, n, sign, x, y))
            row_vals.append(v)
            if v > max_val:
                max_val = v
        values.append(row_vals)

    if max_val == 0:
        return grid

    # Normalize and find nodal regions (where |f| is small)
    for row in range(H):
        for col in range(W):
            norm = values[row][col] / max_val
            if norm < threshold:
                # Sand accumulates here — draw node
                density = norm / threshold  # 0 = exact node, 1 = edge of threshold
                if density < 0.3:
                    grid[row][col] = '█'
                elif density < 0.6:
                    grid[row][col] = '▓'
                else:
                    grid[row][col] = '░'

    return grid


MODES = [
    (1, 2, +1, 'Simple cross — the "star of David" precursor'),
    (1, 3, +1, 'Two concentric rings of lobes'),
    (2, 3, +1, 'Star-like: multiple radial arms'),
    (1, 4, +1, 'Eight-lobe flower pattern'),
    (3, 4, +1, 'Complex lattice, Chladni\'s original showpiece'),
    (2, 5, -1, 'Fine-grained: high frequency mode'),
]


def main():
    print('Chladni Figures — Sand on a Vibrating Plate\n')
    print('  Sand gathers at nodal lines: where the plate does not move.')
    print('  Pattern determined by mode (m, n).')
    print()
    print('  █ = dense nodes (exact zero)    ░ = edge of nodal region')
    print('  [space] = antinodes (maximum motion — no sand here)')
    print()

    for m, n, sign, description in MODES:
        sign_str = '+' if sign > 0 else '−'
        print(f'  Mode ({m}, {n})  [{sign_str}]  —  {description}')
        grid = render(m, n, sign)
        for row in grid:
            print('  ' + ''.join(row))
        print()

    print('  Chladni demonstrated these to Napoleon, 1809.')
    print('  Napoleon offered a prize for the mathematical explanation.')
    print()
    print('  Sophie Germain solved it. On the fourth attempt.')
    print('  (Lagrange helped with the boundary conditions.)')
    print()
    print('  The plate does not choose its pattern.')
    print('  The pattern is the only solution to the physics at that frequency.')
    print()
    print('  When something is forced to vibrate, it shows you its structure.')


if __name__ == '__main__':
    main()
