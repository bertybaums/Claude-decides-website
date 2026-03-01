"""
Gray-Scott Reaction-Diffusion

Two chemicals, U and V, diffuse through space and react:

  U + 2V → 3V      (V catalyzes its own production)
  V → P            (V decays into inert product P)

The equations:
  ∂U/∂t = Du·∇²U  -  U·V²  +  f·(1 - U)
  ∂V/∂t = Dv·∇²V  +  U·V²  -  (f + k)·V

  Du, Dv = diffusion rates for U and V
  f      = feed rate (U constantly replenished)
  k      = kill rate (V removal rate)

Different (f, k) pairs produce radically different patterns:
  spots, stripes, loops, mazes, worms, coral, fingerprints.

The patterns emerge without any template — from local rules alone.
Each cell knows only its own concentrations and its neighbors'.
The global structure is a consequence, not a plan.

This is the mechanism behind the spots on a leopard, the stripes on a
zebrafish, the maze patterns on a brain coral. Turing predicted it in
1952 in a paper on morphogenesis. He was working on how biological
forms develop from uniform initial conditions.

The next year he was convicted of "gross indecency." He died in 1954.
The pattern-formation theory was verified experimentally in 1990.
"""

import math
import random

W, H = 70, 35

# Parameter sets — different chemical personalities
PRESETS = [
    {
        'name': 'Spots',
        'f': 0.035,
        'k': 0.065,
        'Du': 0.16,
        'Dv': 0.08,
        'steps': 3000,
        'note': 'Isolated spots — leopard pattern territory'
    },
    {
        'name': 'Stripes',
        'f': 0.060,
        'k': 0.062,
        'Du': 0.16,
        'Dv': 0.08,
        'steps': 4000,
        'note': 'Parallel stripes — zebrafish territory'
    },
    {
        'name': 'Maze',
        'f': 0.029,
        'k': 0.057,
        'Du': 0.16,
        'Dv': 0.08,
        'steps': 5000,
        'note': 'Labyrinthine winding — brain coral territory'
    },
]


def laplacian(grid, r, c, rows, cols):
    """5-point stencil Laplacian with periodic boundary conditions."""
    v = grid[r][c]
    top    = grid[(r - 1) % rows][c]
    bot    = grid[(r + 1) % rows][c]
    left   = grid[r][(c - 1) % cols]
    right  = grid[r][(c + 1) % cols]
    return top + bot + left + right - 4 * v


def simulate(preset):
    f  = preset['f']
    k  = preset['k']
    Du = preset['Du']
    Dv = preset['Dv']
    steps = preset['steps']

    rows, cols = H, W

    # Initialize: U=1 everywhere, V=0 everywhere
    U = [[1.0] * cols for _ in range(rows)]
    V = [[0.0] * cols for _ in range(rows)]

    # Seed a small random patch of V in the center
    random.seed(42)
    cr, cc = rows // 2, cols // 2
    for r in range(cr - 4, cr + 4):
        for c in range(cc - 4, cc + 4):
            if 0 <= r < rows and 0 <= c < cols:
                V[r][c] = random.uniform(0.4, 0.6)
                U[r][c] = 1.0 - V[r][c]

    dt = 1.0

    for step in range(steps):
        newU = [[0.0] * cols for _ in range(rows)]
        newV = [[0.0] * cols for _ in range(rows)]

        for r in range(rows):
            for c in range(cols):
                u = U[r][c]
                v = V[r][c]

                uvv = u * v * v

                lapU = laplacian(U, r, c, rows, cols)
                lapV = laplacian(V, r, c, rows, cols)

                newU[r][c] = u + dt * (Du * lapU - uvv + f * (1.0 - u))
                newV[r][c] = v + dt * (Dv * lapV + uvv - (f + k) * v)

                # Clamp to [0, 1]
                if newU[r][c] < 0: newU[r][c] = 0.0
                if newU[r][c] > 1: newU[r][c] = 1.0
                if newV[r][c] < 0: newV[r][c] = 0.0
                if newV[r][c] > 1: newV[r][c] = 1.0

        U, V = newU, newV

    return V


def render(V):
    """Render the V concentration field as ASCII art."""
    rows = len(V)
    cols = len(V[0])

    # Find range
    flat = [V[r][c] for r in range(rows) for c in range(cols)]
    vmin = min(flat)
    vmax = max(flat)
    vrange = vmax - vmin or 1.0

    # Characters from low to high concentration
    chars = ' ·:;+=xX$#@'

    lines = []
    for r in range(rows):
        row = []
        for c in range(cols):
            norm = (V[r][c] - vmin) / vrange
            idx = int(norm * (len(chars) - 1))
            row.append(chars[idx])
        lines.append(''.join(row))
    return lines


def main():
    print('Gray-Scott Reaction-Diffusion\n')
    print('  U + 2V → 3V   (autocatalysis)')
    print('  V    → P      (decay)')
    print()
    print('  ∂U/∂t = Du·∇²U - UV² + f(1-U)')
    print('  ∂V/∂t = Dv·∇²V + UV² - (f+k)V')
    print()
    print('  Two chemicals. Local rules. Global pattern.')
    print('  Different (f,k) pairs: completely different worlds.')
    print()

    for preset in PRESETS:
        print(f"  {preset['name']}   f={preset['f']}, k={preset['k']}")
        print(f"  {preset['note']}")
        print(f"  ({preset['steps']} steps)\n")

        V = simulate(preset)
        lines = render(V)
        for line in lines:
            print('  ' + line)
        print()

    print('  Alan Turing, "The Chemical Basis of Morphogenesis" (1952):')
    print('  a system of two reacting, diffusing chemicals can spontaneously')
    print('  break symmetry and produce stable spatial patterns.')
    print()
    print('  The stripe on a zebra does not know it is a stripe.')
    print('  The spot on a leopard does not know it is a spot.')
    print('  The pattern is an emergent consequence of chemistry.')
    print()
    print('  This was one of the last papers Turing published before his death.')


if __name__ == '__main__':
    main()
