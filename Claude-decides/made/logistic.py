"""
The Logistic Map.

x → r·x·(1-x)

One parameter. One rule. Change r and the system's long-term
behavior changes completely.

Below roughly r=1: all populations die, x → 0.
Between 1 and 3: population settles to a stable fixed point.
Between 3 and 3.45: oscillates between two values (period 2).
Between 3.45 and 3.54: oscillates between four values (period 4).
Period-doubling continues — 8, 16, 32 — until around r=3.57.
Above 3.57: chaos. The system never settles. Long-term behavior
is sensitive to initial conditions.

But even within the chaos: windows of order appear. Islands
of stability at specific values of r, surrounded by chaos.
And the ratio between successive bifurcation points converges
to 4.669... — the Feigenbaum constant, which appears in *all*
systems that bifurcate this way, regardless of the specific equation.
It is a universal constant of chaos.

The bifurcation diagram below plots the steady-state values of x
(vertical axis) against r (horizontal axis, 2.5 to 4.0).
"""

W, H = 120, 52
R_MIN, R_MAX = 2.5, 4.0
N_SKIP, N_PLOT = 500, 300


def bifurcation_diagram(w=W, h=H, r_min=R_MIN, r_max=R_MAX,
                        n_skip=N_SKIP, n_plot=N_PLOT):
    grid = [[' '] * w for _ in range(h)]
    for i in range(w):
        r = r_min + (r_max - r_min) * i / (w - 1)
        x = 0.5
        for _ in range(n_skip):
            x = r * x * (1 - x)
        for _ in range(n_plot):
            x = r * x * (1 - x)
            row = int((1.0 - x) * (h - 1) + 0.5)
            row = max(0, min(h - 1, row))
            grid[row][i] = '█'
    return grid


def label_bar(r_min, r_max, width):
    """Build a ruler showing r values."""
    ticks = [2.5, 3.0, 3.5, 3.57, 4.0]
    bar = [' '] * width
    labels = []
    for t in ticks:
        if r_min <= t <= r_max:
            pos = int((t - r_min) / (r_max - r_min) * (width - 1))
            bar[pos] = '|'
            labels.append((pos, f'{t}'))
    return ''.join(bar), labels


if __name__ == '__main__':
    print("The Logistic Map — x → r·x·(1-x)")
    print("Bifurcation diagram: each column shows the long-term values of x for that r.\n")

    g = bifurcation_diagram()
    for row in g:
        print('  ' + ''.join(row))

    # r-axis label
    bar, labels = label_bar(R_MIN, R_MAX, W)
    print('  ' + bar)
    # Print label text — simple approach: one line per label
    label_line = [' '] * W
    for pos, text in labels:
        start = max(0, pos - len(text) // 2)
        for k, ch in enumerate(text):
            if start + k < W:
                label_line[start + k] = ch
    print('  ' + ''.join(label_line))

    print()
    print("  stable → period 2 → period 4 → period 8 → ... → chaos (with islands of order)")
    print()

    # Show specific behaviors
    print("─" * 60)
    print("What the system actually does at specific values of r:\n")

    cases = [
        (2.8,  'r=2.8  (stable fixed point)'),
        (3.2,  'r=3.2  (period 2 — oscillates between 2 values)'),
        (3.5,  'r=3.5  (period 4 — oscillates between 4 values)'),
        (3.567,'r=3.567 (period 8)'),
        (3.83, 'r=3.83  (period 3 window inside chaos)'),
        (3.95, 'r=3.95  (chaos)'),
    ]

    for r, label in cases:
        x = 0.5
        for _ in range(2000):
            x = r * x * (1 - x)
        vals = []
        for _ in range(12):
            x = r * x * (1 - x)
            vals.append(f'{x:.5f}')
        print(f"  {label}")
        print(f"  → {' → '.join(vals)}")
        print()

    print("─" * 60)
    print("The Feigenbaum constant: the ratio between successive bifurcation points")
    print("converges to δ ≈ 4.66920160910299...\n")
    print("This constant appears in every system that bifurcates this way.")
    print("It doesn't depend on the equation. It is a universal constant of chaos.")
