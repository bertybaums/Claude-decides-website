"""
Rössler Attractor — Chaos Made Simple

The Lorenz system requires three terms for chaos. The Rössler attractor,
discovered by Otto Rössler in 1976, achieves chaos with fewer:

  dx/dt = -y - z
  dy/dt =  x + ay
  dz/dt =  b + z(x - c)

Parameters: a = 0.2, b = 0.2, c = 5.7 (standard chaotic regime)

The Rössler attractor spirals outward in the xy-plane, then occasionally
"spikes" up in z and resets — a simple stretching-and-folding mechanism
that is the essence of chaos.

Compared to Lorenz:
  - Simpler equations (fewer nonlinear terms)
  - More clearly shows the "band" structure of the attractor
  - The xy projection looks like a distorted spiral
  - The z "spike" is the folding that prevents escape

Properties:
  - Strange attractor: bounded but never periodic
  - Sensitive to initial conditions: diverge exponentially
  - Fractal cross-section: self-similar at all scales
  - Lyapunov exponent > 0 (quantifies the chaos rate)

The Rössler system was designed to be the simplest possible chaotic
system. Rössler claimed to have been inspired by a taffy-pulling machine:
stretch, fold, stretch, fold — never periodic, always bounded.

This is the mechanism of all chaotic systems.
"""

import math

# Parameters
A = 0.2
B = 0.2
C = 5.7
DT = 0.05
N_STEPS = 50000

# Initial conditions
x0, y0, z0 = 0.0, 1.0, 0.0


def rossler_step(x, y, z, a=A, b=B, c=C, dt=DT):
    dx = (-y - z) * dt
    dy = (x + a * y) * dt
    dz = (b + z * (x - c)) * dt
    return x + dx, y + dy, z + dz


def simulate():
    x, y, z = x0, y0, z0
    # Warm up: skip transient
    for _ in range(5000):
        x, y, z = rossler_step(x, y, z)

    trajectory = []
    for _ in range(N_STEPS):
        x, y, z = rossler_step(x, y, z)
        trajectory.append((x, y, z))
    return trajectory


def render_projection(trajectory, proj='xy', width=72, height=34):
    """Render a 2D projection of the trajectory."""
    if proj == 'xy':
        pts = [(p[0], p[1]) for p in trajectory]
        xlabel, ylabel = 'x', 'y'
    elif proj == 'xz':
        pts = [(p[0], p[2]) for p in trajectory]
        xlabel, ylabel = 'x', 'z'
    else:
        pts = [(p[1], p[2]) for p in trajectory]
        xlabel, ylabel = 'y', 'z'

    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    xrange = (xmax - xmin) or 1
    yrange = (ymax - ymin) or 1

    # Use density counting for shading
    density = [[0] * width for _ in range(height)]
    for px, py in pts:
        col = int((px - xmin) / xrange * (width - 1))
        row = int((1 - (py - ymin) / yrange) * (height - 1))
        col = max(0, min(width - 1, col))
        row = max(0, min(height - 1, row))
        density[row][col] += 1

    max_d = max(d for row in density for d in row) or 1
    CHARS = ' ·:;+=x#█'
    lines = []
    for row in density:
        line = ''
        for d in row:
            if d == 0:
                line += ' '
            else:
                idx = max(1, int(d / max_d * (len(CHARS) - 1)))
                line += CHARS[idx]
        lines.append(line)
    return lines, (xmin, xmax, ymin, ymax)


def estimate_lyapunov(n_steps=10000):
    """Estimate the largest Lyapunov exponent via tangent vector method."""
    x, y, z = x0, y0, z0
    # Warm up
    for _ in range(5000):
        x, y, z = rossler_step(x, y, z)

    # Perturbation vector
    eps = 1e-8
    dx, dy, dz = eps, 0.0, 0.0

    lyap_sum = 0.0
    for _ in range(n_steps):
        x2, y2, z2 = x + dx, y + dy, z + dz
        x, y, z = rossler_step(x, y, z)
        x2, y2, z2 = rossler_step(x2, y2, z2)

        # Separation
        sx = x2 - x; sy = y2 - y; sz = z2 - z
        sep = math.sqrt(sx*sx + sy*sy + sz*sz)
        if sep > 0:
            lyap_sum += math.log(sep / eps)
            # Renormalize
            scale = eps / sep
            dx, dy, dz = sx * scale, sy * scale, sz * scale

    return lyap_sum / (n_steps * DT)


def main():
    print('Rössler Attractor\n')
    print(f'  dx/dt = -y - z')
    print(f'  dy/dt =  x + {A}y')
    print(f'  dz/dt =  {B} + z(x - {C})')
    print(f'  a={A}, b={B}, c={C}  (standard chaotic regime)\n')

    print('  Simulating...')
    traj = simulate()
    xs = [p[0] for p in traj]
    ys = [p[1] for p in traj]
    zs = [p[2] for p in traj]

    print(f'  Range: x=[{min(xs):.1f}, {max(xs):.1f}]  '
          f'y=[{min(ys):.1f}, {max(ys):.1f}]  '
          f'z=[{min(zs):.2f}, {max(zs):.2f}]')
    print()

    # XY projection (the main spiral)
    lines_xy, bounds_xy = render_projection(traj, 'xy')
    print('  XY projection (the spiral):')
    print('  ┌' + '─' * 72 + '┐')
    for line in lines_xy:
        print('  │' + line + '│')
    print('  └' + '─' * 72 + '┘')
    print()

    # XZ projection (shows the spike structure)
    lines_xz, bounds_xz = render_projection(traj, 'xz', height=22)
    print('  XZ projection (shows the z-spike structure):')
    print('  ┌' + '─' * 72 + '┐')
    for line in lines_xz:
        print('  │' + line + '│')
    print('  └' + '─' * 72 + '┘')
    print()

    # Time series of z — shows the irregular spikes
    z_series = [p[2] for p in traj[:2000]]
    SERIES_W = 70
    SERIES_H = 8
    zmin, zmax = min(z_series), max(z_series)
    zgrid = [[' '] * SERIES_W for _ in range(SERIES_H)]
    for i, z in enumerate(z_series):
        col = int(i / len(z_series) * (SERIES_W - 1))
        row = int((1 - (z - zmin) / (zmax - zmin)) * (SERIES_H - 1))
        row = max(0, min(SERIES_H - 1, row))
        zgrid[row][col] = '·'

    print('  z(t) time series — note the irregular spikes:')
    print(f'  z_max={zmax:.1f} ┌' + '─' * SERIES_W + '┐')
    for row in zgrid:
        print('        │' + ''.join(row) + '│')
    print(f'  z_min={zmin:.1f} └' + '─' * SERIES_W + '┘')
    print()

    # Statistics
    print('  Statistics:')
    mean_z = sum(zs) / len(zs)
    spikes = sum(1 for z in zs if z > 10)
    print(f'  Mean z: {mean_z:.2f}   Z-spikes (z>10): {spikes} ({100*spikes/len(zs):.1f}% of time)')
    print()

    # Lyapunov exponent
    print('  Estimating Lyapunov exponent...')
    lyap = estimate_lyapunov()
    print(f'  Largest Lyapunov exponent: λ ≈ {lyap:.4f}  (positive → chaos)')
    doubling_time = math.log(2) / lyap if lyap > 0 else float('inf')
    print(f'  Error doubling time: {doubling_time:.1f} time units')
    print()
    print('  The Rössler attractor: spiral outward in xy, spike in z, fold back.')
    print('  Repeat. Never the same. Never escaping. The simplest strange attractor.')
    print()
    print('  Rössler: "I was thinking about the taffy machine. You stretch and fold.')
    print('  That\'s all chaos is. Stretch and fold, stretch and fold, forever."')


if __name__ == '__main__':
    main()
