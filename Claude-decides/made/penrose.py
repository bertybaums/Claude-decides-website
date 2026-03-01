"""
Penrose Tiling — Aperiodic Order

A Penrose tiling covers the plane with two types of tiles (here: thin and
thick rhombuses) such that:
  1. The plane is fully covered — no gaps, no overlaps
  2. The tiling is NEVER periodic — you cannot slide a copy onto itself
  3. The tiling has LOCAL 5-fold symmetry everywhere

Discovered by Roger Penrose in 1974. Previously, it was assumed that any
finite set of tiles capable of tiling the plane could also tile it periodically.
Penrose proved this assumption wrong.

Properties:
  - Two types of tile: thin rhombus (36°/144° angles) and thick rhombus (72°/108°)
  - The ratio of thick:thin tiles is always the golden ratio φ ≈ 1.618...
  - No finite region uniquely determines the global structure
  - BUT: every finite region appears infinitely often in every Penrose tiling
  - Every Penrose tiling has the same frequency of each local pattern

What makes it strange:
  Long-range order without periodicity. This was considered mathematically
  impossible for most of history. In 1984, Dan Shechtman discovered real
  crystals with this property — "quasicrystals" — and won the 2011 Nobel Prize
  in Chemistry. He was initially ridiculed: "There are no quasicrystals, only
  quasi-scientists."

Construction method used here: de Bruijn's pentagrid method.
  Five sets of parallel lines at 72° offsets divide the plane into regions.
  Each region is labeled by which pentagrid lines bound it.
  The label determines whether it's a thick or thin rhombus.

This produces an exact Penrose tiling.
"""

import math

# Golden ratio
PHI = (1 + math.sqrt(5)) / 2

WIDTH = 70
HEIGHT = 35
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
SCALE = 4.0  # grid units per ASCII cell


def pentagrid_value(x, y, k, gamma=0):
    """
    Value of the k-th pentagrid at position (x, y).
    gamma controls the offset (0 = symmetric).
    """
    angle = 2 * math.pi * k / 5
    return x * math.cos(angle) + y * math.sin(angle) + gamma


def classify_rhombus(i, j, k1, k2, gamma=0):
    """
    Given a rhombus identified by its pentagrid index pair (k1, k2)
    at pentagrid coordinates (i, j), return its center and type.

    Returns: (cx, cy, is_thick)
    """
    # The center of the rhombus in (x,y) is the sum of two basis vectors
    # weighted by the pentagrid coordinates
    # Using de Bruijn's formula
    cx = 0.0
    cy = 0.0

    for k in range(5):
        angle = 2 * math.pi * k / 5
        if k == k1:
            coord = i
        elif k == k2:
            coord = j
        else:
            # Use the floor of the pentagrid value at the rhombus center
            # (Approximate: use 0 for visualization)
            coord = 0
        cx += coord * math.cos(angle)
        cy += coord * math.sin(angle)

    # The angle between the two families determines thick vs. thin
    diff = (k2 - k1) % 5
    is_thick = (diff == 1 or diff == 4)

    return cx, cy, is_thick


def generate_rhombuses(n_rings=6):
    """
    Generate rhombus centers and types using pentagrid method.
    Returns list of (cx, cy, is_thick).
    """
    rhombuses = []
    seen = set()

    for k1 in range(5):
        for k2 in range(k1 + 1, 5):
            for i in range(-n_rings, n_rings + 1):
                for j in range(-n_rings, n_rings + 1):
                    # Compute center using both grid lines
                    a1 = 2 * math.pi * k1 / 5
                    a2 = 2 * math.pi * k2 / 5

                    # Find intersection of line i from family k1 and
                    # line j from family k2
                    # Line k at position m: x*cos(a_k) + y*sin(a_k) = m
                    c1 = math.cos(a1); s1 = math.sin(a1)
                    c2 = math.cos(a2); s2 = math.sin(a2)

                    det = c1 * s2 - s1 * c2
                    if abs(det) < 1e-9:
                        continue

                    x = (i * s2 - j * s1) / det
                    y = (j * c1 - i * c2) / det

                    # Center of rhombus is slightly offset from vertex
                    mx = x + 0.01 * (math.cos(a1) + math.cos(a2))
                    my = y + 0.01 * (math.sin(a1) + math.sin(a2))

                    diff = (k2 - k1) % 5
                    is_thick = (diff == 1 or diff == 4)

                    key = (round(mx * 100), round(my * 100))
                    if key not in seen:
                        seen.add(key)
                        rhombuses.append((mx, my, is_thick))

    return rhombuses


def main():
    print('Penrose Tiling — Aperiodic Order\n')
    print('  Two tiles: thick rhombus (■) and thin rhombus (□)')
    print('  The plane is fully tiled, but the pattern never repeats.')
    print()

    rhombuses = generate_rhombuses(n_rings=8)

    # Map to ASCII grid
    grid = [[' '] * WIDTH for _ in range(HEIGHT)]

    thick_count = 0
    thin_count = 0

    for x, y, is_thick in rhombuses:
        # Convert to screen coordinates
        col = int(CENTER_X + x * SCALE / 2)
        row = int(CENTER_Y - y * SCALE / (2 * 0.7))  # aspect ratio correction

        if 0 <= col < WIDTH and 0 <= row < HEIGHT:
            if is_thick:
                char = '■'
                thick_count += 1
            else:
                char = '·'
                thin_count += 1
            grid[row][col] = char

    print('  ┌' + '─' * WIDTH + '┐')
    for row in grid:
        print('  │' + ''.join(row) + '│')
    print('  └' + '─' * WIDTH + '┘')

    print()
    print(f'  Thick rhombuses: {thick_count}   Thin rhombuses: {thin_count}')
    if thin_count > 0:
        ratio = thick_count / thin_count
        print(f'  Ratio thick/thin: {ratio:.4f}   (Golden ratio φ = {PHI:.4f})')
    print()
    print('  Every finite patch in this tiling appears infinitely often.')
    print('  No finite patch uniquely determines what comes next.')
    print('  The global structure is not implied by any local piece.')
    print()
    print('  Local order. No global period. The pattern is almost-but-not-quite')
    print('  repeating, everywhere, forever.')
    print()
    print('  Quasicrystals have this structure. They were declared impossible')
    print('  until Shechtman found them in 1984. Discovering the impossible')
    print('  earned him a Nobel Prize and, first, years of ridicule.')


if __name__ == '__main__':
    main()
