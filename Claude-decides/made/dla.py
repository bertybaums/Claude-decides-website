"""
Diffusion-Limited Aggregation (DLA)

A particle is released at a random point on the boundary.
It walks randomly — Brownian motion — until it either:
  - Touches the growing cluster: it sticks and becomes part of the cluster
  - Wanders too far from the cluster: it is released and a new one starts

Starting from a single seed particle at the center,
this process produces branching, fractal structures:
coral, lightning, river deltas, frost on glass, mineral dendrites.

Why branches?

The tips of the cluster reach out into empty space and are
more likely to be hit by incoming particles than the interior
(which is shadowed by the tips). The tips grow; the interior doesn't.
This feedback — tips attract tips — produces branching at every scale.

The resulting structure is a fractal with dimension ≈ 1.71
(between a line and a plane — denser than a line, sparser than a solid).

Real-world DLA and DLA-like processes:
  - Zinc crystals grown from solution
  - Lightning channels (dielectric breakdown)
  - River delta formation
  - Snowflake dendrite growth
  - Bacterial colony growth under certain conditions

The branching is not programmed in. It emerges from:
  random walks + aggregation + geometric shadowing.
"""

import random
import math

W, H = 71, 35
CX, CY = W // 2, H // 2
MAX_PARTICLES = 800
ASPECT = 2.0  # chars are ~2x taller than wide

# Radius at which we release new particles (and abandon lost ones)
R_RELEASE_FACTOR = 1.1
R_KILL_FACTOR = 1.5

# Characters to show depth of attachment order
CHARS = '·:;+=xX$#@█'


def dist(x, y):
    # Aspect-correct distance (account for terminal char proportions)
    return math.sqrt(((x - CX) / 1.0) ** 2 + ((y - CY) / ASPECT) ** 2)


def neighbors(x, y):
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]


def run():
    grid = {}        # (x, y) -> particle number (order it was deposited)
    occupied = set() # just the coordinates for fast lookup

    # Seed particle at center
    occupied.add((CX, CY))
    grid[(CX, CY)] = 0

    r_cluster = 1.0   # current cluster radius

    for i in range(1, MAX_PARTICLES + 1):
        # Release radius: just outside the current cluster
        r_release = r_cluster * R_RELEASE_FACTOR + 2
        r_kill = r_cluster * R_KILL_FACTOR + 5

        # Random point on a circle at r_release
        theta = random.uniform(0, 2 * math.pi)
        px = int(CX + r_release * math.cos(theta))
        py = int(CY + r_release * math.sin(theta) * ASPECT)

        # Random walk until stick or die
        stuck = False
        for _ in range(100000):
            # Check if adjacent to cluster
            for nx, ny in neighbors(px, py):
                if (nx, ny) in occupied:
                    # Stick here
                    if 0 <= px < W and 0 <= py < H:
                        occupied.add((px, py))
                        grid[(px, py)] = i
                        d = dist(px, py)
                        if d > r_cluster:
                            r_cluster = d
                    stuck = True
                    break

            if stuck:
                break

            # Random step
            dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
            px += dx
            py += dy

            # Kill if too far
            if dist(px, py) > r_kill:
                break

    return grid


def render(grid, total):
    canvas = [[' '] * W for _ in range(H)]

    for (x, y), order in grid.items():
        if 0 <= x < W and 0 <= y < H:
            # Color by order: early (center) = dense chars, late (tips) = lighter
            progress = order / total
            idx = int(progress * (len(CHARS) - 1))
            canvas[y][x] = CHARS[idx]

    for row in canvas:
        print('  ' + ''.join(row))


def main():
    print('Diffusion-Limited Aggregation\n')
    print('  Particles random-walk until they touch the growing cluster.')
    print('  Tips grow fastest: they intercept walkers before the interior can.')
    print('  Result: branching at every scale — fractal dimension ≈ 1.71.\n')
    print('  · = first particles deposited (center)    █ = most recent (tips)\n')
    print('  Growing...')

    grid = run()

    print(f'  {len(grid)} particles deposited.\n')
    render(grid, MAX_PARTICLES)

    print()
    print('  Why the branches? The tips are exposed; the interior is shadowed.')
    print('  Particles reach the tips before they can diffuse to the interior.')
    print('  The shape amplifies itself — each tip makes the next tip more likely.')
    print()
    print('  Lightning works the same way: the leader tip is most exposed,')
    print('  so the next discharge follows it. The branch is the path.')
    print()
    print('  This is not lightning deciding to branch.')
    print('  Branching is the only thing that can happen here.')


if __name__ == '__main__':
    main()
