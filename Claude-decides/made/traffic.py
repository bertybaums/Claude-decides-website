"""
Rule 184 — The Traffic Flow Cellular Automaton

Rule 184 is a one-dimensional elementary cellular automaton that models
traffic flow with remarkable accuracy.

Rules (neighborhood = left, center, right):
  111 → 1
  110 → 0
  101 → 1
  100 → 1
  011 → 1
  010 → 0
  001 → 0
  000 → 0

Binary: 10111000 = 184 (hence "Rule 184")

Interpretation as traffic:
  1 = car  0 = empty space
  A car moves forward (right) if the space ahead is empty.
  A car stays if the space ahead is occupied.

Emergent behaviors:

At LOW density (few cars):
  Cars move freely. Traffic flows. Average speed ≈ 1 cell/step.

At HIGH density (many cars):
  Cars are mostly stopped. Traffic jams form.
  Jams move BACKWARD (left) at 1 cell/step — even though cars move forward.
  This is real: traffic jams propagate in the opposite direction from traffic.

At CRITICAL density (~50%):
  Phase transition. Jams and free-flow coexist.
  Jam boundaries are sharp — a fundamental phase transition.

Why this matters:
  A simple binary rule captures the essential physics of traffic:
  - Cars can't pass through each other
  - Cars move forward when possible
  - Jams propagate backward (verified in real highway data)

The rule also arises in:
  - Particle-hole symmetric models in statistical mechanics
  - The TASEP (Totally Asymmetric Simple Exclusion Process) — a
    fundamental model in non-equilibrium statistical mechanics
  - Queuing theory and cellular manufacturing

One-dimensional, binary, deterministic — and it captures jam formation.
"""

import random

WIDTH = 70
STEPS = 50

random.seed(42)


def rule184_step(cells):
    """Apply one step of Rule 184 with periodic boundary."""
    n = len(cells)
    new = [0] * n
    for i in range(n):
        left = cells[(i - 1) % n]
        center = cells[i]
        right = cells[(i + 1) % n]
        pattern = (left << 2) | (center << 1) | right
        # Rule 184 lookup
        rule = 0b10111000
        new[i] = (rule >> pattern) & 1
    return new


def run_simulation(density, width=WIDTH, steps=STEPS):
    """Run Rule 184 with given initial density."""
    cells = [1 if random.random() < density else 0 for _ in range(width)]
    history = [cells[:]]
    for _ in range(steps):
        cells = rule184_step(cells)
        history.append(cells[:])
    return history


def flow_rate(history):
    """Estimate average cars passing a fixed point per step."""
    # Count rightward moves: car at i-1 in prev, empty at i in prev, car at i in curr
    total = 0
    for t in range(1, len(history)):
        prev = history[t-1]
        curr = history[t]
        n = len(prev)
        for i in range(n):
            # Car moved from i-1 to i
            if prev[(i-1) % n] == 1 and prev[i] == 0 and curr[i] == 1:
                total += 1
    return total / (len(history) - 1)


def render_history(history, title):
    """Render space-time diagram."""
    CHARS = {0: '·', 1: '█'}
    print(f'  {title}')
    print('  ┌' + '─' * WIDTH + '┐')
    for t, cells in enumerate(history):
        row = ''.join(CHARS[c] for c in cells)
        if t == 0:
            print(f'  │{row}│  ← initial state')
        elif t % 5 == 0:
            print(f'  │{row}│  t={t}')
        else:
            print(f'  │{row}│')
    print('  └' + '─' * WIDTH + '┘')


def main():
    print('Rule 184 — Traffic Flow Cellular Automaton\n')
    print('  █ = car    · = empty space')
    print('  Cars move right if space ahead is empty; stop otherwise.')
    print()

    densities = [0.25, 0.50, 0.75]
    labels = [
        'LOW DENSITY (25%): free flow',
        'CRITICAL DENSITY (50%): phase transition',
        'HIGH DENSITY (75%): jam formation',
    ]

    for density, label in zip(densities, labels):
        random.seed(42)
        history = run_simulation(density)
        render_history(history[:20], label)

        # Measure flow
        flow = flow_rate(history)
        n_cars = sum(history[0])
        final_cars = sum(history[-1])
        print(f'  Cars: {n_cars}/{WIDTH} ({100*n_cars/WIDTH:.0f}%)')
        print(f'  Average flow: {flow:.2f} cars/step passing a fixed point')
        print()

    # Show jam propagation explicitly
    print('  BACKWARD JAM PROPAGATION (high density):')
    print()
    print('  Watch the gap in the jam: it moves LEFT (backward) over time.')
    print()
    jam_demo = [1] * 15 + [0, 0, 0] + [1] * 15 + [0] * (WIDTH - 33)
    history_jam = [jam_demo[:]]
    for _ in range(10):
        jam_demo = rule184_step(jam_demo)
        history_jam.append(jam_demo[:])

    print('  ┌' + '─' * WIDTH + '┐')
    for t, cells in enumerate(history_jam):
        row = ''.join('█' if c else '·' for c in cells)
        print(f'  │{row}│  t={t}')
    print('  └' + '─' * WIDTH + '┘')
    print()
    print('  The gap (empty space) moves LEFT at 1 cell/step.')
    print('  The cars move RIGHT. The jam moves OPPOSITE to the cars.')
    print()
    print('  This is observed on real highways. When you finally pass a slowdown,')
    print('  there is often no visible cause — just cars braking because the car')
    print('  ahead braked, and so on, back to an originating brake applied minutes')
    print('  and miles earlier. The jam has long since moved away from its origin.')
    print()
    print('  Rule 184: two states, three-cell neighborhood, deterministic.')
    print('  Jam formation, jam propagation, phase transition: emergent.')


if __name__ == '__main__':
    main()
