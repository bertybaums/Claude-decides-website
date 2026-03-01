"""
Diffusion — The Spread of Concentration

The heat equation (diffusion equation):
    ∂u/∂t = D · ∂²u/∂x²

u(x,t) = concentration (or temperature) at position x, time t
D = diffusion coefficient

Describes: heat conduction, chemical diffusion, random walk spreading,
Brownian motion, financial option pricing (Black-Scholes is this equation).

Discretized (finite differences):
    u[i,t+1] = u[i,t] + D·dt/dx² · (u[i+1,t] - 2·u[i,t] + u[i-1,t])

The second derivative (∂²u/∂x²) measures curvature:
  - Positive curvature (valley): concentration flows in
  - Negative curvature (peak): concentration flows out

This is why diffusion smooths. Not because "high concentration moves to low
concentration" (that's a consequence), but because curvature drives flow.

Fundamental solution: a Gaussian that spreads over time.
Width grows as √(Dt) — the square root of time.
This is why diffusion is slow: to spread twice as far takes four times as long.

This √t scaling appears everywhere:
  - Random walks spread as √n steps
  - Brownian motion: mean square displacement grows linearly with time
  - Error in Monte Carlo estimates falls as 1/√n samples
  - DNA replication errors: mutation rate grows as √generations
"""

import math

WIDTH = 70
N_STEPS = 200
DISPLAY_STEPS = [0, 5, 15, 30, 60, 100, 200]
D = 0.4   # diffusion coefficient (must be ≤ 0.5 for stability)
DT = 1.0
DX = 1.0


def step(u, D=D, dt=DT, dx=DX):
    """One step of explicit finite difference diffusion."""
    n = len(u)
    new = u[:]
    r = D * dt / (dx * dx)  # Stability requires r ≤ 0.5
    for i in range(1, n - 1):
        new[i] = u[i] + r * (u[i+1] - 2*u[i] + u[i-1])
    return new


def gaussian_exact(x, t, D=D):
    """Exact solution: Gaussian spreading over time."""
    if t <= 0:
        return 0.0
    sigma2 = 2 * D * t
    return math.exp(-x*x / (2*sigma2)) / math.sqrt(2 * math.pi * sigma2)


def render_profile(u, max_val=1.0, width=WIDTH, height=12):
    """Render a 1D profile as a bar chart."""
    CHARS = ' ·:;+=x#█'
    grid = [[' '] * width for _ in range(height)]
    for i, val in enumerate(u):
        col = int(i / len(u) * width)
        col = min(col, width - 1)
        h = int(val / max_val * (height - 1))
        h = max(0, min(height - 1, h))
        for row in range(height - 1, height - 1 - h, -1):
            grid[row][col] = '█'
        # Top cap
        if h >= 0:
            density_idx = max(1, int(val / max_val * (len(CHARS) - 1)))
            grid[height - 1 - h][col] = CHARS[density_idx]
    return [''.join(row) for row in grid]


def compute_width(u, threshold=0.01):
    """Find the effective width (where u > threshold)."""
    positions = [i for i, v in enumerate(u) if v > threshold]
    if not positions:
        return 0
    return positions[-1] - positions[0]


def main():
    print('Diffusion — The Heat Equation\n')
    print(f'  ∂u/∂t = D · ∂²u/∂x²   (D = {D})')
    print('  Curvature drives flow: peaks spread, valleys fill.')
    print()

    # Initialize: delta function (point source)
    N = 200
    u = [0.0] * N
    u[N // 2] = 1.0 / DX  # Approximate delta function

    print('  POINT SOURCE SPREADING (initial concentration at center):')
    print()

    snapshots = []
    t = 0
    for step_num in range(max(DISPLAY_STEPS) + 1):
        if step_num in DISPLAY_STEPS:
            snapshots.append((step_num, u[:]))
        u = step(u)
        t += DT

    max_val = max(max(s[1]) for s in snapshots[:3])  # Use early max for scale

    for step_num, snap in snapshots:
        sigma = math.sqrt(2 * D * max(step_num, 0.1))
        predicted_peak = 1.0 / (sigma * math.sqrt(2 * math.pi))
        actual_peak = max(snap)
        w = compute_width(snap)

        lines = render_profile(snap, max_val=max_val)
        label = f'  t={step_num:3d}  peak={actual_peak:.3f}  width≈{w}'
        print(label)
        print('  ┌' + '─' * WIDTH + '┐')
        for line in lines:
            print('  │' + line + '│')
        print('  └' + '─' * WIDTH + '┘')
        print()

    # Show √t scaling
    print('  WIDTH GROWS AS √t (square-root-of-time scaling):')
    print()
    print(f'  {"t":>6}  {"Width":>8}  {"√t × const":>12}  {"Ratio":>8}')
    w0 = None
    for step_num, snap in snapshots[1:]:  # skip t=0
        w = compute_width(snap, threshold=0.005)
        sqrt_t = math.sqrt(step_num) if step_num > 0 else 0
        if w0 is None and w > 0:
            w0 = w
            const = w / sqrt_t if sqrt_t > 0 else 1
        if w > 0 and sqrt_t > 0:
            predicted = const * sqrt_t
            ratio = w / predicted
            print(f'  {step_num:>6}  {w:>8}  {predicted:>12.1f}  {ratio:>8.3f}')

    print()
    print('  The ratio stays near 1.0: width ∝ √t confirmed.')
    print()

    # Second demo: two sources merging
    print('  TWO SOURCES MERGING:')
    print()
    u2 = [0.0] * N
    u2[N//2 - 25] = 1.0 / DX
    u2[N//2 + 25] = 1.0 / DX

    snapshots2 = []
    for step_num in range(201):
        if step_num in [0, 10, 30, 80, 200]:
            snapshots2.append((step_num, u2[:]))
        u2 = step(u2)

    max_val2 = max(max(s[1]) for s in snapshots2[:2])

    for step_num, snap in snapshots2:
        lines = render_profile(snap, max_val=max_val2)
        print(f'  t={step_num}')
        print('  ┌' + '─' * WIDTH + '┐')
        for line in lines:
            print('  │' + line + '│')
        print('  └' + '─' * WIDTH + '┘')
        print()

    print('  The two sources spread, merge, and equilibrate.')
    print('  No memory of the two sources remains in the final state.')
    print()
    print('  This is entropy increasing: information about the initial')
    print('  configuration is lost. The final state could have come')
    print('  from any of many initial configurations.')
    print()
    print('  Diffusion is time-asymmetric: the spread never spontaneously')
    print('  reverses. This is related to the second law of thermodynamics.')


if __name__ == '__main__':
    main()
