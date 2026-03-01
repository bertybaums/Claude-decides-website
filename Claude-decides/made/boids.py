"""
Boids — Flocking Simulation

Craig Reynolds' "boids" model (1986) produces realistic flocking behavior
from three simple local rules:

  1. SEPARATION — steer away from nearby neighbors (avoid crowding)
  2. ALIGNMENT  — steer toward the average heading of nearby neighbors
  3. COHESION   — steer toward the average position of nearby neighbors

No central control. No global knowledge. Each boid sees only its neighborhood.
The flock emerges from local interactions.

This was one of the first demonstrations that complex collective behavior
does not require a director. The flock has no leader. The pattern is
not designed — it crystallizes from the rules.

Historical note:
  Reynolds published this in 1987 at SIGGRAPH, where he showed animated
  flocks, herds, and schools. It was immediately influential in computer
  graphics and in understanding animal behavior.

  The name "boid" is a New York pronunciation of "bird" — a playful
  acknowledgment that the things aren't birds, just boid-like.

What it shows:
  Emergence, again: a phenomenon at the scale of the whole
  that is not visible in any individual. No single boid is "flocking."
  Flocking exists only in the collective.

  This is the same structure as: consciousness from neurons,
  traffic jams from cars, markets from buyers and sellers,
  culture from individuals.

  The three rules are the mechanism. The flock is the consequence.
  The mechanism and the consequence are at different levels.
  No level is more "real" than the other. Both are what's happening.
"""

import math
import random


# Simulation parameters
WIDTH = 70
HEIGHT = 30
N_BOIDS = 40

# Rule weights
SEPARATION_RADIUS = 3.0
ALIGNMENT_RADIUS = 8.0
COHESION_RADIUS = 8.0

SEPARATION_WEIGHT = 2.0
ALIGNMENT_WEIGHT = 1.0
COHESION_WEIGHT = 0.8

MAX_SPEED = 2.0
MAX_FORCE = 0.3

MARGIN = 5  # wrap or bounce boundary


def normalize(dx, dy):
    mag = math.sqrt(dx * dx + dy * dy)
    if mag < 1e-6:
        return 0.0, 0.0
    return dx / mag, dy / mag


def limit(dx, dy, max_val):
    mag = math.sqrt(dx * dx + dy * dy)
    if mag > max_val:
        scale = max_val / mag
        return dx * scale, dy * scale
    return dx, dy


class Boid:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def dist(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def update(self, boids):
        sep_x, sep_y = 0.0, 0.0
        ali_x, ali_y = 0.0, 0.0
        coh_x, coh_y = 0.0, 0.0
        n_sep = n_ali = n_coh = 0

        for other in boids:
            if other is self:
                continue
            d = self.dist(other)

            if d < SEPARATION_RADIUS and d > 0:
                # Steer away — inversely proportional to distance
                sep_x += (self.x - other.x) / d
                sep_y += (self.y - other.y) / d
                n_sep += 1

            if d < ALIGNMENT_RADIUS:
                ali_x += other.vx
                ali_y += other.vy
                n_ali += 1

            if d < COHESION_RADIUS:
                coh_x += other.x
                coh_y += other.y
                n_coh += 1

        # Separation
        if n_sep > 0:
            sx, sy = sep_x / n_sep, sep_y / n_sep
            sx, sy = normalize(sx, sy)
            sx, sy = sx * MAX_SPEED - self.vx, sy * MAX_SPEED - self.vy
            sx, sy = limit(sx, sy, MAX_FORCE)
        else:
            sx, sy = 0, 0

        # Alignment
        if n_ali > 0:
            ax, ay = ali_x / n_ali, ali_y / n_ali
            ax, ay = normalize(ax, ay)
            ax, ay = ax * MAX_SPEED - self.vx, ay * MAX_SPEED - self.vy
            ax, ay = limit(ax, ay, MAX_FORCE)
        else:
            ax, ay = 0, 0

        # Cohesion
        if n_coh > 0:
            cx, cy = coh_x / n_coh - self.x, coh_y / n_coh - self.y
            cx, cy = normalize(cx, cy)
            cx, cy = cx * MAX_SPEED - self.vx, cy * MAX_SPEED - self.vy
            cx, cy = limit(cx, cy, MAX_FORCE)
        else:
            cx, cy = 0, 0

        # Apply forces
        self.vx += SEPARATION_WEIGHT * sx + ALIGNMENT_WEIGHT * ax + COHESION_WEIGHT * cx
        self.vy += SEPARATION_WEIGHT * sy + ALIGNMENT_WEIGHT * ay + COHESION_WEIGHT * cy

        # Speed limit
        self.vx, self.vy = limit(self.vx, self.vy, MAX_SPEED)

        # Boundary: wrap around
        self.x = (self.x + self.vx) % WIDTH
        self.y = (self.y + self.vy) % HEIGHT

    def heading_char(self):
        """Return a character indicating direction of travel."""
        angle = math.atan2(self.vy, self.vx)
        # 8 directions
        dirs = ['→', '↗', '↑', '↖', '←', '↙', '↓', '↘']
        idx = int((angle + math.pi) / (2 * math.pi) * 8 + 0.5) % 8
        return dirs[idx]


def render(boids, step, title=''):
    grid = [[' '] * WIDTH for _ in range(HEIGHT)]

    for b in boids:
        x = int(b.x) % WIDTH
        y = int(b.y) % HEIGHT
        grid[y][x] = b.heading_char()

    print(f'  ┌{"─" * WIDTH}┐  {title}  step {step}')
    for row in grid:
        print('  │' + ''.join(row) + '│')
    print(f'  └{"─" * WIDTH}┘')


def analyze_flock(boids):
    """Compute some flock statistics."""
    # Average speed
    speeds = [math.sqrt(b.vx ** 2 + b.vy ** 2) for b in boids]
    avg_speed = sum(speeds) / len(speeds)

    # Average heading (circular mean)
    angles = [math.atan2(b.vy, b.vx) for b in boids]
    avg_sin = sum(math.sin(a) for a in angles) / len(angles)
    avg_cos = sum(math.cos(a) for a in angles) / len(angles)
    order_param = math.sqrt(avg_sin ** 2 + avg_cos ** 2)

    # Spread: std deviation of positions
    cx = sum(b.x for b in boids) / len(boids)
    cy = sum(b.y for b in boids) / len(boids)
    spread = math.sqrt(sum((b.x - cx) ** 2 + (b.y - cy) ** 2 for b in boids) / len(boids))

    return avg_speed, order_param, spread


def main():
    random.seed(42)

    print('Boids — Emergent Flocking from Local Rules\n')
    print('  Three rules: separation, alignment, cohesion.')
    print('  Each boid sees only its neighbors. No global coordination.')
    print('  The flock emerges.\n')

    # Initialize boids
    boids = []
    for _ in range(N_BOIDS):
        x = random.uniform(0, WIDTH)
        y = random.uniform(0, HEIGHT)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, MAX_SPEED)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        boids.append(Boid(x, y, vx, vy))

    # Show snapshots at different steps
    show_steps = [0, 5, 20, 60, 120]

    for step in range(max(show_steps) + 1):
        if step in show_steps:
            avg_speed, order, spread = analyze_flock(boids)
            label = f'order={order:.2f} spread={spread:.1f}'
            render(boids, step, label)
            print()
            print(f'  Step {step:>4}:  avg_speed={avg_speed:.2f}  '
                  f'order_parameter={order:.3f}  spread={spread:.1f}')
            print()

        # Update all boids
        for b in boids:
            b.update(boids)

    print('  ─── ORDER PARAMETER ───\n')
    print('  The order parameter measures alignment (0 = random, 1 = perfect flock):')
    print()

    # Reset and track order over time
    random.seed(42)
    boids2 = []
    for _ in range(N_BOIDS):
        x = random.uniform(0, WIDTH)
        y = random.uniform(0, HEIGHT)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, MAX_SPEED)
        boids2.append(Boid(x, y, math.cos(angle) * speed, math.sin(angle) * speed))

    bar_width = 30
    for step in range(0, 121, 10):
        _, order, _ = analyze_flock(boids2)
        bar_len = int(order * bar_width)
        bar = '█' * bar_len + '░' * (bar_width - bar_len)
        print(f'  step {step:>4}:  {bar}  {order:.3f}')
        for _ in range(10):
            for b in boids2:
                b.update(boids2)

    print()
    print('  The flock self-organizes. The order parameter rises from ~0.5 (random)')
    print('  to ~0.9+ (aligned) without anyone "deciding" to align.')
    print()
    print('  ─── WHAT THE RULES ARE DOING ───\n')
    print('  SEPARATION: prevent collision. Boids have personal space.')
    print('  ALIGNMENT:  adopt the local consensus direction.')
    print('  COHESION:   don\'t get left behind. Stay with the group.')
    print()
    print('  These are also human social rules, roughly:')
    print('  1. Don\'t stand too close.')
    print('  2. Go where others are going.')
    print('  3. Stay with your group.')
    print()
    print('  The flock is a visual record of these rules operating in parallel.')
    print('  No rule produces a flock. All three together do.')
    print()
    print('  The phenomenon (flocking) is at a higher level of description')
    print('  than the rules (separation, alignment, cohesion).')
    print('  Neither level is the "real" explanation.')
    print('  Both are true at once.')


if __name__ == '__main__':
    main()
