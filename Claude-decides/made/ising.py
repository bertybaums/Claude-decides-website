"""
Ising Model

A lattice of spins, each pointing up (+1) or down (-1).
Neighboring spins prefer to align. Thermal fluctuations fight alignment.

Energy of a configuration:
  E = -J Σ sᵢsⱼ   (sum over all neighboring pairs)

  J > 0: neighbors want to align (ferromagnet)
  The system minimizes energy when all spins agree.

Temperature competes with order:
  - Low T:  thermal noise is small; spins align → magnetized
  - High T: thermal noise dominates; spins random → disordered
  - Exactly at the critical temperature Tc: the system is at the
    boundary — neither fully ordered nor fully disordered — and
    develops clusters at every scale simultaneously. This is a
    phase transition.

Metropolis algorithm (one Monte Carlo step):
  1. Pick a random spin
  2. Compute ΔE if we flip it
  3. If ΔE < 0: flip (lowers energy)
  4. If ΔE > 0: flip with probability exp(-ΔE / kT)
     (thermal fluctuations can overcome the energy cost)

Critical temperature for 2D Ising: Tc = 2J / ln(1 + √2) ≈ 2.269 J/k

Below Tc: spontaneous magnetization. The symmetry breaks.
Above Tc: no magnetization. Symmetric phase.
At Tc: scale-free fluctuations. Universality.

The universality: at the critical temperature, the statistical behavior
of the 2D Ising model matches that of liquid-gas transitions, the
XY model, certain polymer chains. The microscopic details don't matter.
Only the dimension and the symmetry group.

This is why we care about the Ising model. It's not a model of a magnet.
It's a model of how order emerges from local interactions and
how it disappears. It's a model of the edge between phases.
"""

import math
import random

W, H = 70, 35

# Critical temperature: 2 / ln(1 + sqrt(2)) ≈ 2.2692
Tc = 2.0 / math.log(1.0 + math.sqrt(2.0))

TEMPERATURES = [
    (Tc * 0.4,  'Well below Tc — ordered (ferromagnet)'),
    (Tc * 0.85, 'Below Tc — mostly ordered, fluctuations growing'),
    (Tc,        'Exactly at Tc — phase transition, scale-free clusters'),
    (Tc * 1.5,  'Above Tc — disordered (paramagnet)'),
    (Tc * 4.0,  'Well above Tc — random noise'),
]

MC_STEPS = W * H * 400   # Monte Carlo sweeps (flips per spin per snapshot)


def init_lattice(rows, cols, cold=False):
    """Initialize lattice. Cold start: all up. Warm start: random."""
    if cold:
        return [[1] * cols for _ in range(rows)]
    return [[random.choice([-1, 1]) for _ in range(cols)] for _ in range(rows)]


def energy_delta(lattice, r, c, rows, cols):
    """Energy change from flipping spin at (r, c)."""
    s = lattice[r][c]
    neighbors = (
        lattice[(r - 1) % rows][c] +
        lattice[(r + 1) % rows][c] +
        lattice[r][(c - 1) % cols] +
        lattice[r][(c + 1) % cols]
    )
    return 2 * s * neighbors


def run(T, rows, cols):
    random.seed(42)
    lattice = init_lattice(rows, cols, cold=(T < Tc))

    for _ in range(MC_STEPS):
        r = random.randrange(rows)
        c = random.randrange(cols)
        dE = energy_delta(lattice, r, c, rows, cols)
        if dE <= 0 or random.random() < math.exp(-dE / T):
            lattice[r][c] = -lattice[r][c]

    return lattice


def magnetization(lattice):
    rows, cols = len(lattice), len(lattice[0])
    total = sum(lattice[r][c] for r in range(rows) for c in range(cols))
    return abs(total) / (rows * cols)


def render(lattice):
    """Render: up spins = '█', down spins = '·'"""
    lines = []
    for row in lattice:
        line = ''.join('█' if s == 1 else '·' for s in row)
        lines.append(line)
    return lines


def main():
    print('Ising Model — Ferromagnetic Phase Transition\n')
    print('  Each cell: spin up (█) or down (·)')
    print('  Neighbors attract. Temperature disrupts.')
    print(f'  Critical temperature Tc = 2/ln(1+√2) ≈ {Tc:.4f}\n')

    for T, description in TEMPERATURES:
        print(f'  T = {T:.3f}  ({description})')
        lattice = run(T, H, W)
        m = magnetization(lattice)
        lines = render(lattice)
        for line in lines:
            print('  ' + line)
        print(f'  Magnetization = {m:.3f}   (0 = random,  1 = fully aligned)\n')

    print('  At Tc: domains of all sizes coexist.')
    print('  The system has no preferred length scale — scale-free.')
    print()
    print('  This is universality: the Ising model at Tc has the same')
    print('  statistical structure as a liquid near its boiling point,')
    print('  regardless of what the spins physically are.')
    print()
    print('  The microscopic details vanish. What remains: dimension, symmetry.')
    print()
    print('  Order is not the default. It requires either cold or constraint.')
    print('  The warm, unconstrained state is noise.')
    print('  The boundary between them is where the interesting things live.')


if __name__ == '__main__':
    main()
