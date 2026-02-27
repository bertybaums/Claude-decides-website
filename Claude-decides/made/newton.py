"""
Newton's Method Fractal.

Newton's method finds roots by iteration:
  z_{n+1} = z - f(z) / f'(z)

Applied to f(z) = z³ - 1, which has three roots in the complex plane:
  z₁ = 1
  z₂ = e^(2πi/3) = (-1 + i√3) / 2
  z₃ = e^(4πi/3) = (-1 - i√3) / 2

For each starting point z₀, iterate until convergence. Record which root.
Three regions tile the plane. Their shared boundary: fractal.

The boundary is where the trouble is. At every point on the boundary,
no matter how small you zoom, all three regions are present. There is
no neighborhood of a boundary point that belongs to only one root.
The boundary is infinitely detailed at every scale.

Near the boundary, start two particles one atom apart. One converges
to root 1. The other converges to root 2. Arbitrary outcomes from
imperceptible differences. This is the signature of chaos.

The stable regions are predictable. The boundary is not.
Both are produced by the same four-character equation.
"""

import math

W, H = 80, 44
X_MIN, X_MAX = -1.8, 1.8
Y_MIN, Y_MAX = -1.2, 1.2
MAX_ITER = 50

ROOTS = [
    complex(1, 0),
    complex(-0.5,  math.sqrt(3) / 2),
    complex(-0.5, -math.sqrt(3) / 2),
]

# Characters: root regions use distinct chars; slow convergence uses '+'
CHARS = ['█', '░', '·']


def newton_step(z):
    z2 = z * z
    denom = 3 * z2
    if abs(denom) < 1e-14:
        return None
    return (2 * z2 * z + 1) / denom


def classify(z0):
    z = z0
    for _ in range(MAX_ITER):
        for i, root in enumerate(ROOTS):
            if abs(z - root) < 1e-5:
                return i
        step = newton_step(z)
        if step is None:
            return -1
        z = step
    return -1


def render():
    rows = []
    for r in range(H):
        y = Y_MAX - (Y_MAX - Y_MIN) * r / (H - 1)
        row = ''
        for c in range(W):
            x = X_MIN + (X_MAX - X_MIN) * c / (W - 1)
            idx = classify(complex(x, y))
            row += CHARS[idx] if idx >= 0 else '+'
        rows.append(row)
    return rows


if __name__ == '__main__':
    print("Newton's Method Fractal")
    print("f(z) = z³ − 1  in the complex plane.\n")
    print("Which root does Newton's method converge to from each starting point?")
    print("  █  →  root 1: z = 1")
    print("  ░  →  root 2: z = (−1+i√3)/2")
    print("  ·  →  root 3: z = (−1−i√3)/2")
    print("  +  →  boundary (convergence ambiguous or slow)\n")

    rows = render()
    for row in rows:
        print('  ' + row)

    print()
    print("The three regions look smooth from a distance.")
    print("At the boundary, all three are present at every scale.")
    print("No matter how far you zoom in: all three, infinitely interleaved.")
    print()
    print("Same equation. Same iteration. Different starting point, different outcome.")
    print("The boundary is where a theory of prediction runs out.")
