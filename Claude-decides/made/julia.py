"""
Julia Sets.

For a complex number c, the Julia set J(c) is the boundary between
starting points z₀ that iterate to infinity under z → z² + c,
and those that stay bounded.

Every c gives a different Julia set. Most are fractal.
Some are connected (c inside the Mandelbrot set); some are totally
disconnected dust (c outside). The Mandelbrot set is the map of
which c values give connected Julia sets.

Three very different Julia sets below:
  c = -0.7 + 0.27i     — a connected, spiral-rich set
  c = -0.4 + 0.6i      — another connected form; looks like a sea horse
  c = 0.285 + 0.01i    — a beautiful connected set near the Mandelbrot boundary
"""

W, H = 75, 38
DENSITY = '·:+%█'  # characters from light to dark, by iteration count
MAX_ITER = 80


def julia_point(z0, c, max_iter):
    z = z0
    for i in range(max_iter):
        if abs(z) > 2.0:
            return i
        z = z * z + c
    return max_iter


def render_julia(c, x_min, x_max, y_min, y_max, w=W, h=H):
    rows = []
    for row in range(h):
        y = y_max - (y_max - y_min) * row / (h - 1)
        line = ''
        for col in range(w):
            x = x_min + (x_max - x_min) * col / (w - 1)
            z0 = complex(x, y)
            iters = julia_point(z0, c, MAX_ITER)
            if iters == MAX_ITER:
                line += '█'
            else:
                idx = int(iters / MAX_ITER * (len(DENSITY) - 1))
                line += DENSITY[idx]
        rows.append(line)
    return rows


if __name__ == '__main__':
    cases = [
        (
            complex(-0.7, 0.27),
            (-1.6, 1.6, -0.9, 0.9),
            'c = -0.7 + 0.27i  — spiral arms, connected',
        ),
        (
            complex(-0.4, 0.6),
            (-1.5, 1.5, -0.9, 0.9),
            'c = -0.4 + 0.6i  — dendritic, connected',
        ),
        (
            complex(0.285, 0.01),
            (-1.5, 1.5, -0.85, 0.85),
            'c = 0.285 + 0.01i  — near Mandelbrot boundary, intricate',
        ),
    ]

    print("Julia Sets — z → z² + c")
    print("Each value of c produces a different fractal boundary.\n")
    print(f"  █ = bounded (in the set)  · : + % = escape speed\n")

    for c, (x_min, x_max, y_min, y_max), label in cases:
        print('─' * 50)
        print(f'  {label}\n')
        rows = render_julia(c, x_min, x_max, y_min, y_max)
        for row in rows:
            print('  ' + row)
        print()

    print('─' * 50)
    print('The Mandelbrot set (earlier in this collection) is the map of')
    print('which values of c produce connected Julia sets.')
    print()
    print('Each point in the Mandelbrot set contains, in its parameter,')
    print('a whole Julia set — a different one for every c.')
    print()
    print('One fractal contains infinitely many different fractals.')
    print('They are related the way a recipe is related to the dish:')
    print('the Mandelbrot set organizes what is possible;')
    print('the Julia sets are what actually happens.')
