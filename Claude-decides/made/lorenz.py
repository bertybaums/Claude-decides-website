"""
The Lorenz Attractor.

dx/dt = σ(y - x)
dy/dt = x(ρ - z) - y
dz/dt = xy - βz

With σ=10, ρ=28, β=8/3.

The Lorenz system is completely deterministic. Given identical starting
conditions, you get identical trajectories. Always.

But: given starting conditions that differ by any nonzero amount —
even 0.000000001 — the trajectories eventually diverge completely.
This is sensitive dependence on initial conditions. The butterfly effect.

The attractor has a shape: two lobes, like wings, like a butterfly.
The trajectory spirals around one lobe for a while, then crosses to the
other, then back, apparently at random. But it never repeats exactly.
It never crosses itself. It stays on this strange surface forever.

Lorenz discovered this in 1963 while running a weather simulation.
He had rounded an input from 0.506127 to 0.506. The difference:
0.000127. The simulation diverged completely.

That's why weather forecasting has a ~10 day horizon.
Not instrument error. Not model imprecision.
Fundamental. The atmosphere is Lorenz.
"""

WIDTH = 120
HEIGHT = 50
STEPS = 20000
DT = 0.005

SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0


def lorenz_step(x, y, z):
    dx = SIGMA * (y - x)
    dy = x * (RHO - z) - y
    dz = x * y - BETA * z
    return x + dx * DT, y + dy * DT, z + dz * DT


def render(points):
    # Project onto (x, z) plane — the classic view
    xs = [p[0] for p in points]
    zs = [p[2] for p in points]

    min_x, max_x = min(xs), max(xs)
    min_z, max_z = min(zs), max(zs)

    # Build density grid
    grid = [[0] * WIDTH for _ in range(HEIGHT)]
    for x, z in zip(xs, zs):
        col = int((x - min_x) / (max_x - min_x) * (WIDTH - 1))
        row = int((z - min_z) / (max_z - min_z) * (HEIGHT - 1))
        row = (HEIGHT - 1) - row  # flip so z increases upward
        grid[row][col] += 1

    max_density = max(max(row) for row in grid)
    chars = ' ·∘○◎●'

    lines = []
    for row in grid:
        line = []
        for cell in row:
            if cell == 0:
                line.append(' ')
            else:
                idx = max(1, int((cell / max_density) * (len(chars) - 1)))
                line.append(chars[idx])
        lines.append(''.join(line))
    return lines


if __name__ == '__main__':
    x, y, z = 1.0, 1.0, 1.0
    points = []

    # Discard first 1000 steps (transient behavior before settling on attractor)
    for _ in range(1000):
        x, y, z = lorenz_step(x, y, z)

    for _ in range(STEPS):
        x, y, z = lorenz_step(x, y, z)
        points.append((x, y, z))

    print("Lorenz Attractor — projection onto (x, z) plane")
    print(f"{STEPS} steps, dt={DT}, σ={SIGMA}, ρ={RHO}, β={BETA:.4f}\n")
    for line in render(points):
        print(line)
