"""
Euler's Formula: e^(iθ) = cos(θ) + i·sin(θ)

Traces the unit circle in the complex plane as θ goes from 0 to 2π.

At each angle θ, e^(iθ) is a point on the unit circle:
  real part: cos(θ)
  imaginary part: sin(θ)

At θ = π, the point is (-1, 0): that's the number -1.
So e^(iπ) = -1, which gives us: e^(iπ) + 1 = 0.

The formula says: the exponential function, when fed an imaginary argument,
produces rotation. Not growth (what e^x usually does) but rotation.
The imaginary axis is the axis of turning.

Below: the full circle, traced as θ increases, with key angles marked.
The circle is the shape of imaginary exponentiation.
"""

import math

W, H = 60, 30
CX, CY = W // 2, H // 2
RADIUS_X = W // 2 - 2
RADIUS_Y = H // 2 - 1


def to_screen(real, imag):
    col = int(CX + real * RADIUS_X)
    row = int(CY - imag * RADIUS_Y)
    return col, row


def main():
    grid = [[' '] * W for _ in range(H)]

    # Draw axes
    for c in range(W):
        grid[CY][c] = '─'
    for r in range(H):
        grid[r][CX] = '│'
    grid[CY][CX] = '┼'

    # Draw the unit circle
    for i in range(400):
        theta = 2 * math.pi * i / 400
        col, row = to_screen(math.cos(theta), math.sin(theta))
        if 0 <= col < W and 0 <= row < H:
            if grid[row][col] == ' ':
                grid[row][col] = '·'

    # Mark the trajectory as θ increases from 0 to 2π
    # Color by how far along (using different chars for quadrants)
    quadrant_chars = ['░', '▒', '▓', '█']
    for i in range(360):
        theta = 2 * math.pi * i / 360
        q = int(i / 90)  # 0-3 for four quadrants
        col, row = to_screen(math.cos(theta), math.sin(theta))
        if 0 <= col < W and 0 <= row < H:
            grid[row][col] = quadrant_chars[q]

    # Mark key special angles
    special = [
        (0,            '1',    '  θ=0: e^0 = 1'),
        (math.pi/2,    'i',    '  θ=π/2: e^(iπ/2) = i'),
        (math.pi,      '-1',   '  θ=π: e^(iπ) = -1  ← Euler\'s identity'),
        (3*math.pi/2,  '-i',   '  θ=3π/2: e^(i3π/2) = -i'),
    ]

    labels = []
    for theta, char, label in special:
        col, row = to_screen(math.cos(theta), math.sin(theta))
        if 0 <= col < W and 0 <= row < H:
            grid[row][col] = '*'
        labels.append((theta, label))

    # Print
    print('Euler\'s Formula: e^(iθ) traces the unit circle\n')
    print('  Axes: real (horizontal) and imaginary (vertical)')
    print('  The circle: e^(iθ) for θ from 0 to 2π')
    print('  ░ = first quadrant (0 to π/2)')
    print('  ▒ = second (π/2 to π)')
    print('  ▓ = third (π to 3π/2)')
    print('  █ = fourth (3π/2 to 2π)')
    print('  * = key angles\n')

    for row in grid:
        print('  ' + ''.join(row))

    print()
    print('  Key points (* markers):')
    for _, label in labels:
        print(f'   {label}')

    print()
    print('  The circle proves the identity:')
    print('  At θ = π, e^(iπ) = cos(π) + i·sin(π) = -1 + 0i = -1')
    print('  Therefore: e^(iπ) + 1 = 0')
    print()
    print('  The formula says: imaginary exponentiation is rotation.')
    print('  Go halfway around the circle: arrive at -1.')
    print('  The five fundamental constants were always related.')
    print('  Euler found the relation.')


if __name__ == '__main__':
    main()
