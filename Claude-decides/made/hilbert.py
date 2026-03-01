"""
The Hilbert Curve

A space-filling curve. A path — one-dimensional — that visits every point
in a two-dimensional square.

At each iteration, the curve is refined: what was one segment becomes four,
folded into a U-shape. Repeat. At the limit: every point in the square
is on the path. The path has length ∞ and area > 0.

A line that fills a plane.

Cantor (1878) proved that a line and a plane have the same number of points,
which seemed absurd. Peano (1890) showed you could connect them continuously.
Hilbert (1891) gave this elegant version.

The curve visits each point exactly once in the limit, maintaining continuity
everywhere. But it has no derivative anywhere — it turns too often.
Like the Koch snowflake: everywhere continuous, nowhere smooth.

Shown here at orders 1 through 4.
The path color shows progress: · (start) through █ (end).
"""

W, H = 65, 31      # display grid
ORDERS = [1, 2, 3, 4]


def d2xy(n, d):
    """Map index d along the Hilbert curve to (x,y) in an n×n grid."""
    x = y = 0
    s = 1
    while s < n:
        rx = 1 if (d & 2) else 0
        ry = 1 if (d & 1) ^ rx else 0
        if ry == 0:
            if rx == 1:
                x = s - 1 - x
                y = s - 1 - y
            x, y = y, x
        x += s * rx
        y += s * ry
        d >>= 2
        s *= 2
    return x, y


def draw_line_on_grid(grid, c1, r1, c2, r2, char):
    steps = max(abs(c2-c1), abs(r2-r1), 1) * 3
    for i in range(steps + 1):
        t = i / steps
        col = int(round(c1 + t * (c2 - c1)))
        row = int(round(r1 + t * (r2 - r1)))
        if 0 <= col < W and 0 <= row < H:
            if grid[row][col] == ' ':
                grid[row][col] = char


def render_order(order):
    grid = [[' '] * W for _ in range(H)]
    n = 2 ** order
    total = n * n

    CHARS = '·░▒▓█'

    prev_col = prev_row = None
    for d in range(total):
        x, y = d2xy(n, d)
        col = int(x * (W - 1) / (n - 1)) if n > 1 else W // 2
        row = int((1.0 - y / (n - 1)) * (H - 1)) if n > 1 else H // 2

        progress = d / (total - 1)
        char = CHARS[int(progress * (len(CHARS) - 1))]

        if prev_col is not None:
            draw_line_on_grid(grid, prev_col, prev_row, col, row, char)
        if 0 <= col < W and 0 <= row < H:
            grid[row][col] = char

        prev_col, prev_row = col, row

    return grid


def main():
    print('The Hilbert Curve: a path that fills a square\n')
    print('  Each iteration: every segment becomes four, folded into a U.')
    print('  At the limit: every point in the square lies on the path.')
    print()
    print('  · = start of path   █ = end of path\n')

    for order in ORDERS:
        n = 2 ** order
        total = n * n
        grid = render_order(order)
        print(f'  Order {order}  ({n}×{n} grid,  {total} points)')
        for row in grid:
            print('  ' + ''.join(row))
        print()

    print('  At the limit (order → ∞):')
    print('  — The path visits every point in the square.')
    print('  — The path has infinite length.')
    print('  — The path is continuous everywhere.')
    print('  — The path has no derivative anywhere (turns too often).')
    print()
    print('  Dimension of the Hilbert curve: 2.')
    print('  It is a 1D object with 2D measure.')
    print()
    print('  Cantor proved a line and a plane have the same number of points.')
    print('  Peano proved you could connect them continuously.')
    print('  Hilbert made it beautiful.')


if __name__ == '__main__':
    main()
