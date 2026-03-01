"""
Lissajous Figures

x(t) = sin(a·t + δ)
y(t) = sin(b·t)

Two sine waves oscillating in perpendicular directions.
The shape depends on the frequency ratio a:b and phase shift δ.

Lissajous curves appear on oscilloscopes when two AC signals are
applied to the X and Y channels. They were a standard tool for
measuring frequency ratios in electronics before digital measurement.

Also appear in:
  - Pendulums with two-axis motion
  - Vibrating membranes (linked to Chladni figures)
  - Orbital mechanics (Lissajous orbits around Lagrange points)
    — the James Webb Space Telescope orbits at L2 on a Lissajous path

The SHAPE tells you the RATIO:
  a:b = 1:1 → ellipse or diagonal line (depending on δ)
  a:b = 1:2 → figure-8
  a:b = 2:3 → three-lobe curve
  a:b = 3:4 → complex knot
  a:b = 3:5 → five-lobe figure

When a:b is rational: the curve closes, periodic.
When a:b is irrational: the curve never closes, densely fills a region.

The number of lobes in each direction:
  Horizontal lobes: b    Vertical lobes: a
  (Count the tangencies with the bounding rectangle)

Named after Jules Antoine Lissajous (1822–1880), who used a
harmonic vibrator and a beam of light reflected off vibrating mirrors
to draw the curves on a screen. Physics made visible.
"""

import math

W, H = 71, 35
SAMPLES = W * H * 4

CURVES = [
    (1, 1, 0,        'Circle / ellipse (equal frequencies, 0° phase)'),
    (1, 1, math.pi/4,'Tilted ellipse (equal frequencies, 45° phase)'),
    (1, 2, 0,        'Figure-8 vertical (a:b = 1:2)'),
    (1, 2, math.pi/4,'Parabola-like (a:b = 1:2, 45° phase)'),
    (2, 3, 0,        'Three-lobe figure (a:b = 2:3)'),
    (3, 4, math.pi/4,'Complex knot (a:b = 3:4, 45° phase)'),
    (3, 5, math.pi/6,'Five-lobe figure (a:b = 3:5)'),
    (5, 6, math.pi/4,'Dense curve (a:b = 5:6)'),
]


def render_curve(a, b, delta):
    grid = [[' '] * W for _ in range(H)]

    # Sample t from 0 to 2π (or multiple periods to ensure closure)
    # For rational a:b = p/q in lowest terms, period = 2π·lcm(p,q)/(p*q) ... just use 2π*max(a,b)
    t_max = 2 * math.pi * max(a, b)
    dt = t_max / SAMPLES

    prev_col, prev_row = None, None

    for i in range(SAMPLES + 1):
        t = i * dt
        x = math.sin(a * t + delta)
        y = math.sin(b * t)

        col = int((x + 1) / 2 * (W - 1))
        row = int((1 - (y + 1) / 2) * (H - 1))
        col = max(0, min(W - 1, col))
        row = max(0, min(H - 1, row))

        # Draw point
        grid[row][col] = '·'

        # Connect to previous point
        if prev_col is not None:
            # Bresenham-ish: interpolate
            dr = abs(row - prev_row)
            dc = abs(col - prev_col)
            steps = max(dr, dc, 1)
            for s in range(1, steps):
                ir = int(round(prev_row + s / steps * (row - prev_row)))
                ic = int(round(prev_col + s / steps * (col - prev_col)))
                if 0 <= ir < H and 0 <= ic < W:
                    grid[ir][ic] = '·'

        prev_col, prev_row = col, row

    return grid


def main():
    print('Lissajous Figures\n')
    print('  x(t) = sin(a·t + δ)    y(t) = sin(b·t)')
    print('  The shape encodes the frequency ratio a:b.')
    print()
    print('  On an oscilloscope, this reveals the ratio of two signals.')
    print('  The Webb telescope traces one of these paths around L2.\n')

    for a, b, delta, description in CURVES:
        print(f'  a={a}, b={b}, δ={delta/math.pi:.2f}π  —  {description}')
        grid = render_curve(a, b, delta)
        for row in grid:
            print('  ' + ''.join(row))
        print()

    print('  When a:b is irrational: the curve fills a rectangle densely.')
    print('  It never closes. It visits every point (to any precision).')
    print()
    print('  When a:b is rational: the curve closes exactly.')
    print('  The shape is determined by the ratio. The ratio is readable in the shape.')
    print()
    print('  Physics uses beauty as a diagnostic tool:')
    print('  look at the figure, read the frequency. The geometry is the measurement.')


if __name__ == '__main__':
    main()
