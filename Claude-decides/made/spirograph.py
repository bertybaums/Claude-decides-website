"""
Spirograph — Hypotrochoids and Epitrochoids

A spirograph curve is traced by a point on (or inside) a small circle
rolling around the inside (hypotrochoid) or outside (epitrochoid) of
a larger circle.

Parameters:
  R = radius of fixed circle
  r = radius of rolling circle
  d = distance of pen from center of rolling circle

Position at angle t:
  Hypotrochoid:
    x = (R - r) cos(t) + d cos((R-r)/r · t)
    y = (R - r) sin(t) - d sin((R-r)/r · t)

  Epitrochoid:
    x = (R + r) cos(t) - d cos((R+r)/r · t)
    y = (R + r) sin(t) - d sin((R+r)/r · t)

The curve closes when (R-r)/r = p/q is rational — after q full circles.
Irrational ratios: the curve never closes, filling space densely.

Special cases:
  d = r (hypotrochoid): the pen is on the circle edge → hypocycloid
    k=2: line segment (degenerate)
    k=3: deltoid (3-pointed star)
    k=4: astroid (4-pointed star, hypocycloid of 4)

The patterns are called Lissajous figures when both x and y are
sinusoidal (already in lissajous.py), but spirograph curves are richer:
the number of petals = |R/r - 1| for hypotrochoids in some parameterizations.

These are the patterns that children draw without knowing why they're beautiful.
The ratio R/r is all that determines the symmetry; d determines whether
the inner loops are cusps, loops, or dimples.
"""

import math

WIDTH = 72
HEIGHT = 36


def draw(curves, title):
    """Render a list of (x, y) curves to ASCII."""
    # Find bounding box across all curves
    all_pts = [(x, y) for pts in curves for x, y in pts]
    if not all_pts:
        return
    xs = [p[0] for p in all_pts]
    ys = [p[1] for p in all_pts]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    margin = 0.02
    xrange = (xmax - xmin) * (1 + margin) or 1
    yrange = (ymax - ymin) * (1 + margin) or 1

    grid = [[' '] * WIDTH for _ in range(HEIGHT)]

    CHARS = '·:;+=x#█'
    for ci, pts in enumerate(curves):
        char = CHARS[ci % len(CHARS)]
        prev = None
        for x, y in pts:
            col = int((x - xmin + xrange * margin / 2) / xrange * (WIDTH - 1))
            row = int((1 - (y - ymin + yrange * margin / 2) / yrange) * (HEIGHT - 1))
            col = max(0, min(WIDTH - 1, col))
            row = max(0, min(HEIGHT - 1, row))
            grid[row][col] = char
            # Interpolate to previous point to avoid gaps
            if prev is not None:
                pc, pr = prev
                steps = max(abs(col - pc), abs(row - pr))
                for s in range(1, steps):
                    ic = pc + (col - pc) * s // steps
                    ir = pr + (row - pr) * s // steps
                    if grid[ir][ic] == ' ':
                        grid[ir][ic] = char
            prev = (col, row)

    print(f'  {title}')
    print('  ┌' + '─' * WIDTH + '┐')
    for row in grid:
        print('  │' + ''.join(row) + '│')
    print('  └' + '─' * WIDTH + '┘')


def hypotrochoid(R, r, d, n_pts=3000):
    """Generate hypotrochoid points."""
    # Curve closes after lcm(R,r)/r rotations of small circle
    # Use enough turns
    from math import gcd
    g = gcd(int(R), int(r))
    turns = int(R / g)  # number of full circles of rolling circle
    pts = []
    for i in range(n_pts):
        t = 2 * math.pi * turns * i / n_pts
        x = (R - r) * math.cos(t) + d * math.cos((R - r) / r * t)
        y = (R - r) * math.sin(t) - d * math.sin((R - r) / r * t)
        pts.append((x, y))
    return pts


def epitrochoid(R, r, d, n_pts=3000):
    """Generate epitrochoid points."""
    from math import gcd
    g = gcd(int(R), int(r))
    turns = int(r / g)
    pts = []
    for i in range(n_pts):
        t = 2 * math.pi * turns * i / n_pts
        x = (R + r) * math.cos(t) - d * math.cos((R + r) / r * t)
        y = (R + r) * math.sin(t) - d * math.sin((R + r) / r * t)
        pts.append((x, y))
    return pts


def main():
    print('Spirograph — Hypotrochoids & Epitrochoids\n')
    print('  x = (R±r)cos(t) ± d·cos((R±r)/r · t)')
    print('  y = (R±r)sin(t) ± d·sin((R±r)/r · t)\n')

    # 1. Classic spirograph variety
    # R=5, r=3, d=5 → 5-pointed star-like with inner loops
    pts1 = hypotrochoid(5, 3, 5)
    draw([pts1], 'Hypotrochoid: R=5, r=3, d=5  (5-fold symmetry, loops)')

    print()

    # 2. Rose-like (inner loops become dimples)
    pts2 = hypotrochoid(7, 3, 3)
    draw([pts2], 'Hypotrochoid: R=7, r=3, d=3  (7 dimples, smooth)')

    print()

    # 3. Astroid — special case d=r for 4-cusped hypocycloid
    pts3 = hypotrochoid(4, 1, 1)
    draw([pts3], 'Astroid: R=4, r=1, d=1  (4-cusped hypocycloid)')

    print()

    # 4. Epitrochoid — the rolling circle is outside
    pts4 = epitrochoid(3, 1, 2)
    draw([pts4], 'Epitrochoid: R=3, r=1, d=2  (3 outer loops)')

    print()

    # 5. More complex ratio
    pts5 = hypotrochoid(13, 5, 8)
    draw([pts5], 'Hypotrochoid: R=13, r=5, d=8  (complex 13-fold pattern)')

    print()
    print('  The symmetry is determined entirely by R/r.')
    print('  The shape (loops, cusps, dimples) by d/r.')
    print()
    print('  R/r = p/q (rational) → curve closes after q turns.')
    print('  R/r irrational → curve never closes; fills a band densely.')
    print()
    print('  These are the curves a spirograph toy produces.')
    print('  The child doesn\'t know why they\'re beautiful.')
    print('  The ratio knows.')


if __name__ == '__main__':
    main()
