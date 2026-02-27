"""
The Mandelbrot set.

For each point c in the complex plane, iterate z → z² + c from z=0.
If |z| stays bounded forever, c is in the set.
We approximate "forever" with 256 iterations.

The boundary of the set is infinitely detailed — zoom in anywhere
and there's more structure, forever. Self-similar but not identical.

The whole thing emerges from z² + c.
"""

WIDTH = 120
HEIGHT = 40
MAX_ITER = 64

# Viewport: real axis [-2.5, 1.0], imaginary axis [-1.2, 1.2]
RE_MIN, RE_MAX = -2.5, 1.0
IM_MIN, IM_MAX = -1.2, 1.2

# Characters ordered by visual density — the set itself gets █,
# nearby points get dense chars, escapees get sparse ones
CHARS = ' ·:;+=xX$&#█'


def mandelbrot(c):
    z = 0
    for i in range(MAX_ITER):
        if abs(z) > 2:
            return i
        z = z * z + c
    return MAX_ITER


def render():
    rows = []
    for row in range(HEIGHT):
        line = []
        im = IM_MAX - (row / HEIGHT) * (IM_MAX - IM_MIN)
        for col in range(WIDTH):
            re = RE_MIN + (col / WIDTH) * (RE_MAX - RE_MIN)
            c = complex(re, im)
            n = mandelbrot(c)
            idx = int((n / MAX_ITER) * (len(CHARS) - 1))
            line.append(CHARS[idx])
        rows.append(''.join(line))
    return rows


if __name__ == '__main__':
    for row in render():
        print(row)
