"""
Koch Snowflake

Start with an equilateral triangle.
For each edge: replace the middle third with a triangular bump.
Repeat.

Iteration 0: triangle.     Perimeter: 3s.
Iteration 1: star.         Perimeter: 4s.
Iteration 2: snowflake.    Perimeter: (4/3)² · 3s  ≈  5.33s.
Iteration 3: ...           Perimeter: (4/3)³ · 3s  ≈  7.11s.
Iteration n: ...           Perimeter: 3s · (4/3)ⁿ  →  ∞

Each iteration multiplies the perimeter by 4/3.
After infinitely many iterations: infinite perimeter.

The area? Each bump adds a triangle. The areas form a geometric series
that converges. The snowflake has finite area. Bounded. Traceable by eye.
But the edge never stops — it has infinite length, infinite detail.

A shape you can fill a bucket from, but never fence.
"""

import math

W, H = 75, 30


def make_grid():
    return [[' '] * W for _ in range(H)]


def draw_line(grid, x1, y1, x2, y2, char):
    # x, y in [0,1] space, mapped to grid with aspect correction
    # Characters are ~2x taller than wide, so stretch y by 0.5
    steps = max(int(abs(x2-x1) * W * 4), int(abs(y2-y1) * H * 4), 2)
    for i in range(steps):
        t = i / (steps - 1)
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        col = int(round(x * (W - 1)))
        row = int(round((1.0 - y) * (H - 1)))
        if 0 <= col < W and 0 <= row < H:
            grid[row][col] = char


def koch_curve(n, x1, y1, x2, y2, grid, char):
    """Draw Koch curve of depth n from (x1,y1) to (x2,y2)."""
    if n == 0:
        draw_line(grid, x1, y1, x2, y2, char)
        return

    dx, dy = x2 - x1, y2 - y1

    # Trisection
    ax, ay = x1 + dx/3,   y1 + dy/3
    bx, by = x1 + 2*dx/3, y1 + 2*dy/3

    # Peak of equilateral bump (rotated 60° outward)
    # Outward = left perpendicular for CW traversal = rotate (dx/3, dy/3) by +60°
    s, c = math.sin(math.pi/3), math.cos(math.pi/3)
    ex, ey = bx - ax, by - ay          # vector a→b
    px = ax + c*ex - s*ey
    py = ay + s*ex + c*ey

    koch_curve(n-1, x1, y1, ax, ay, grid, char)
    koch_curve(n-1, ax, ay, px, py, grid, char)
    koch_curve(n-1, px, py, bx, by, grid, char)
    koch_curve(n-1, bx, by, x2, y2, grid, char)


def snowflake(n):
    grid = make_grid()
    char = ['·', '░', '▒', '▓', '█'][min(n, 4)]

    # Equilateral triangle centered, pointing up
    # In [0,1] coords, y is stretched by 2 for aspect (chars are 2:1 h:w)
    # Place the snowflake to fill most of the grid
    cx = 0.5
    cy = 0.48     # slightly above center (the snowflake is wider than tall in chars)

    # Circumradius: limited by width (x range 0..1 → W cols)
    # and height (y range → H rows, but chars are 2x taller)
    # Effective height in [0,1] units = H / (W * 2) * W = H/2 / W * W
    # R so the bottom vertices fit: cy - R/2 > 0.05
    # and top fits: cy + R < 0.98
    # and sides fit: cx ± R*sqrt(3)/2 * W/H * 0.5 < W → R*0.866 < 0.45
    # With aspect correction (y is 2x taller than x in physical units):
    R = 0.40      # in [0,1] units for x
    Ry = R * 0.5  # y extent (halved for aspect)

    vT  = (cx,                          cy + Ry)
    vBL = (cx - R * math.sqrt(3)/2,     cy - Ry/2)
    vBR = (cx + R * math.sqrt(3)/2,     cy - Ry/2)

    # Edges go clockwise (T→BL→BR→T) so bumps go outward (left of direction)
    koch_curve(n, *vT, *vBL,  grid, char)
    koch_curve(n, *vBL, *vBR, grid, char)
    koch_curve(n, *vBR, *vT,  grid, char)

    return grid


def perimeter(n):
    return 3 * (4/3)**n


def main():
    print('Koch Snowflake\n')
    print('  Each iteration: replace middle third of every edge with a bump.')
    print('  Perimeter × 4/3 each step.  Area converges.\n')

    for n in range(5):
        grid = snowflake(n)
        p = perimeter(n)
        seg_count = 3 * (4**n)
        print(f'  Iteration {n}  |  {seg_count:4d} segments  |  perimeter = {p:.3f}s')
        for row in grid:
            print('  ' + ''.join(row))
        print()

    print('  Perimeter after n iterations:  3 · (4/3)ⁿ · s  →  ∞')
    print()
    print('  Area after n iterations converges to:  (2/5)√3 s²')
    print('  (adding 1/9th of the previous addition each time)')
    print()
    print('  The snowflake fits in a circle.')
    print('  Its edge grows without bound.')
    print()
    print('  You can fill it. You cannot trace it.')


if __name__ == '__main__':
    main()
