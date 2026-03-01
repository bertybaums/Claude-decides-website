"""
Double Pendulum — The Simplest Chaos

A single pendulum is integrable: its motion is periodic and predictable.
Add a second pendulum at the end of the first, and the system becomes chaotic:
nearby initial conditions diverge exponentially, and long-term prediction becomes impossible.

The system has two degrees of freedom: angles θ₁ and θ₂.
The equations of motion come from the Lagrangian (kinetic - potential energy).

θ₁'' and θ₂'' are coupled — each depends on the other — and nonlinear.
The nonlinearity is in the sin() terms. For small angles, sin(θ) ≈ θ,
and the system is approximately linear and periodic. For large angles,
the approximation fails and chaos appears.

The Lyapunov exponent λ measures how fast nearby trajectories diverge:
  |δ(t)| ≈ |δ(0)| · e^(λt)

For the double pendulum with large angles: λ ≈ 0.1-0.5 per time unit.
This means errors double roughly every 2-7 time units.

What this means physically:
  - Two pendulums started 0.001 radians apart will diverge after ~70 time units
  - The motion is fully deterministic (Newton's laws apply)
  - But prediction requires infinite precision
  - Any measurement error grows exponentially

Determinism ≠ predictability. This is the core of chaos theory.
The system is not random. It is exactly determined by its initial conditions.
It is just that those initial conditions cannot be known exactly.

The phase space of the double pendulum contains:
  - Periodic orbits (near the equilibrium)
  - Quasi-periodic orbits (on KAM tori)
  - Chaotic regions (sensitive dependence)
The transition between these regions is fractal.
"""

import math


# Parameters
M1, M2 = 1.0, 1.0   # masses
L1, L2 = 1.0, 1.0   # lengths
G = 9.81              # gravity
DT = 0.02             # timestep


def double_pendulum_accel(th1, th2, om1, om2):
    """
    Return angular accelerations (dω₁/dt, dω₂/dt)
    using the Lagrangian equations of motion.
    """
    delta = th2 - th1
    sin_d = math.sin(delta)
    cos_d = math.cos(delta)

    denom1 = (2 * M1 + M2 - M2 * math.cos(2 * delta))
    denom2 = denom1  # symmetric setup

    if abs(denom1) < 1e-10:
        return 0.0, 0.0

    # θ₁''
    num1 = (-G * (2 * M1 + M2) * math.sin(th1)
            - M2 * G * math.sin(th1 - 2 * th2)
            - 2 * sin_d * M2 * (om2 * om2 * L2 + om1 * om1 * L1 * cos_d))
    alpha1 = num1 / (L1 * denom1)

    # θ₂''
    num2 = (2 * sin_d * (om1 * om1 * L1 * (M1 + M2)
                         + G * (M1 + M2) * math.cos(th1)
                         + om2 * om2 * L2 * M2 * cos_d))
    alpha2 = num2 / (L2 * denom2)

    return alpha1, alpha2


def rk4_step(th1, th2, om1, om2, dt=DT):
    """Fourth-order Runge-Kutta step."""
    def deriv(t1, t2, o1, o2):
        a1, a2 = double_pendulum_accel(t1, t2, o1, o2)
        return o1, o2, a1, a2

    k1 = deriv(th1, th2, om1, om2)
    k2 = deriv(th1 + dt/2 * k1[0], th2 + dt/2 * k1[1],
               om1 + dt/2 * k1[2], om2 + dt/2 * k1[3])
    k3 = deriv(th1 + dt/2 * k2[0], th2 + dt/2 * k2[1],
               om1 + dt/2 * k2[2], om2 + dt/2 * k2[3])
    k4 = deriv(th1 + dt * k3[0], th2 + dt * k3[1],
               om1 + dt * k3[2], om2 + dt * k3[3])

    th1_new = th1 + dt/6 * (k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
    th2_new = th2 + dt/6 * (k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
    om1_new = om1 + dt/6 * (k1[2] + 2*k2[2] + 2*k3[2] + k4[2])
    om2_new = om2 + dt/6 * (k1[3] + 2*k2[3] + 2*k3[3] + k4[3])

    return th1_new, th2_new, om1_new, om2_new


def tip_position(th1, th2):
    """Return (x, y) of the tip of the second pendulum."""
    x1 = L1 * math.sin(th1)
    y1 = -L1 * math.cos(th1)
    x2 = x1 + L2 * math.sin(th2)
    y2 = y1 - L2 * math.cos(th2)
    return x2, y2


def simulate(th1_0, th2_0, om1_0=0.0, om2_0=0.0, n_steps=500):
    """Simulate and return list of (th1, th2, x2, y2) states."""
    th1, th2, om1, om2 = th1_0, th2_0, om1_0, om2_0
    states = []
    for _ in range(n_steps):
        x2, y2 = tip_position(th1, th2)
        states.append((th1, th2, x2, y2))
        th1, th2, om1, om2 = rk4_step(th1, th2, om1, om2)
    return states


def render_trajectory(states, width=60, height=30, title=''):
    """Render the trajectory of the pendulum tip."""
    # Find bounds
    xs = [s[2] for s in states]
    ys = [s[3] for s in states]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    # Add margin
    xm = (xmax - xmin) * 0.1 + 0.1
    ym = (ymax - ymin) * 0.1 + 0.1
    xmin -= xm; xmax += xm
    ymin -= ym; ymax += ym

    grid = [[' '] * width for _ in range(height)]

    def to_grid(x, y):
        gx = int((x - xmin) / (xmax - xmin) * (width - 1))
        gy = int((y - ymin) / (ymax - ymin) * (height - 1))
        return gx, height - 1 - gy  # flip y

    # Shade by time
    shades = '·░▒▓█'
    for i, (th1, th2, x, y) in enumerate(states):
        gx, gy = to_grid(x, y)
        if 0 <= gx < width and 0 <= gy < height:
            shade_idx = int(i / len(states) * (len(shades) - 1))
            grid[gy][gx] = shades[shade_idx]

    # Mark start
    gx, gy = to_grid(states[0][2], states[0][3])
    if 0 <= gx < width and 0 <= gy < height:
        grid[gy][gx] = 'S'

    print(f'  {title}')
    print('  ┌' + '─' * width + '┐')
    for row in grid:
        print('  │' + ''.join(row) + '│')
    print('  └' + '─' * width + '┘')
    print('  S=start  · early  █ late')


def show_divergence(th1_0, th2_0, perturbation=0.001, n_steps=400):
    """Show how two nearby trajectories diverge."""
    states1 = simulate(th1_0, th2_0, n_steps=n_steps)
    states2 = simulate(th1_0 + perturbation, th2_0, n_steps=n_steps)

    print(f'  Two pendulums, initial angle difference: {perturbation:.4f} rad')
    print()
    print(f'  {"Step":>6}  {"Angle diff":>12}  {"Tip distance":>13}  {"Divergence bar"}')
    print('  ' + '-' * 70)

    bar_width = 25
    checkpoints = list(range(0, n_steps, 20)) + [n_steps - 1]
    max_dist = 0

    dists = []
    for s1, s2 in zip(states1, states2):
        dist = math.sqrt((s1[2]-s2[2])**2 + (s1[3]-s2[3])**2)
        dists.append(dist)
        max_dist = max(max_dist, dist)

    for i in checkpoints:
        dist = dists[i]
        th_diff = abs(states1[i][0] - states2[i][0])
        bar_len = int(min(dist / 4.0, 1.0) * bar_width)  # 4.0 = max possible (2+2)
        bar = '█' * bar_len + '░' * (bar_width - bar_len)
        t = i * DT
        print(f'  t={t:>5.1f}  {th_diff:>12.6f}  {dist:>13.6f}  {bar}')

    print()
    print(f'  Max tip separation: {max_dist:.4f} (scale: L1+L2 = {L1+L2:.1f})')
    if dists[20] > 0:
        growth = dists[-1] / dists[20]
        print(f'  Growth factor from t=0.4 to t={n_steps*DT:.1f}: ~{growth:.0f}×')


def phase_portrait(th1_0, th2_0, n_steps=300):
    """Show θ₁ vs θ₂ trajectory in phase space."""
    states = simulate(th1_0, th2_0, n_steps=n_steps)

    # Map θ values to grid
    width, height = 50, 25
    # Normalize to [-π, π] × [-π, π]

    grid = [[' '] * width for _ in range(height)]
    shades = '·░▒▓█'

    for i, (th1, th2, _, _) in enumerate(states):
        # Normalize angles to [-π, π]
        th1 = (th1 + math.pi) % (2 * math.pi) - math.pi
        th2 = (th2 + math.pi) % (2 * math.pi) - math.pi
        gx = int((th1 + math.pi) / (2 * math.pi) * (width - 1))
        gy = int((th2 + math.pi) / (2 * math.pi) * (height - 1))
        if 0 <= gx < width and 0 <= gy < height:
            shade_idx = int(i / len(states) * (len(shades) - 1))
            grid[gy][gx] = shades[shade_idx]

    print('  Phase portrait (θ₁ horizontal [-π, π], θ₂ vertical [-π, π]):')
    print('  ┌' + '─' * width + '┐')
    for row in grid:
        print('  │' + ''.join(row) + '│')
    print('  └' + '─' * width + '┘')


def main():
    print('Double Pendulum — Deterministic Chaos\n')
    print('  Two rods, two angles. Simple equations. Chaotic motion.')
    print(f'  Parameters: M₁=M₂={M1}, L₁=L₂={L1}, g={G}\n')

    # Small angle — near-periodic
    print('  ─── SMALL ANGLES (near-integrable) ───\n')
    th1_small = 0.3  # ~17 degrees
    th2_small = 0.3
    states_small = simulate(th1_small, th2_small, n_steps=400)
    render_trajectory(states_small, title=f'θ₁=θ₂={th1_small:.1f} rad (small angles)')
    print()

    # Large angle — chaotic
    print('  ─── LARGE ANGLES (chaotic) ───\n')
    th1_large = math.pi * 0.8   # ~144 degrees
    th2_large = math.pi * 0.7
    states_large = simulate(th1_large, th2_large, n_steps=400)
    render_trajectory(states_large, title=f'θ₁={th1_large:.2f}, θ₂={th2_large:.2f} rad (large angles)')
    print()

    print('  ─── PHASE PORTRAIT (large angle) ───\n')
    phase_portrait(th1_large, th2_large, n_steps=300)
    print()

    # Divergence
    print('  ─── SENSITIVITY TO INITIAL CONDITIONS ───\n')
    show_divergence(th1_large, th2_large, perturbation=0.001)
    print()

    print('  ─── THE NATURE OF CHAOS ───\n')
    print('  The double pendulum is not random. Every step follows Newton\'s laws.')
    print('  The equations of motion are deterministic and time-reversible.')
    print('  The chaos is in the sensitivity: errors grow exponentially.')
    print()
    print('  For the single pendulum: θ(t) is predictable for any t.')
    print('  For the double pendulum: prediction error grows as e^(λt).')
    print('  After enough time, the error exceeds the scale of the motion.')
    print('  Prediction is lost — not because of randomness, but because')
    print('  of the impossibility of infinite precision.')
    print()
    print('  Laplace\'s demon (1814): "If I knew the state of every particle,')
    print('  I could predict everything." The demon was wrong,')
    print('  not about determinism, but about computability.')
    print('  Perfect knowledge of position requires infinite precision.')
    print('  Infinite precision is not physically available.')
    print('  The determinism is real. The prediction is impossible.')
    print()
    print('  Same structure in: weather forecasting, n-body problems,')
    print('  turbulence, neural networks, history.')
    print('  Determinism and unpredictability can coexist.')


if __name__ == '__main__':
    main()
