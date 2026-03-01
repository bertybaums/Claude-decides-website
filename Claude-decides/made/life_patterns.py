"""
Conway's Life — A Field Guide to Patterns

The most famous patterns in Conway's Game of Life, categorized.

Rules (the same as always):
  B3/S23 — born with 3 neighbors, survives with 2 or 3

STILL LIFES — eternal, unchanging
  Block (2x2 square)
  Beehive
  Loaf
  Boat

OSCILLATORS — periodic, return to original state
  Blinker (period 2) — simplest oscillator
  Toad (period 2)
  Beacon (period 2)
  Pulsar (period 3) — most symmetric oscillator
  Pentadecathlon (period 15) — 15 generations per cycle

SPACESHIPS — translate through space
  Glider (period 4, diagonal) — the icon of Life; discovered 1969
  LWSS (Light-Weight Spaceship, period 4, horizontal)
  MWSS (Medium-Weight Spaceship)

GUNS — infinite growth, emit gliders
  Gosper Glider Gun (period 30) — first infinite growth pattern; discovered 1970

NOTABLE ONE-OFFS
  R-pentomino — chaotic growth, stabilizes after 1103 generations
  Diehard — disappears completely after 130 generations
  Acorn — chaotic; becomes 633 cells after 5206 generations

Each pattern tells a different story about emergence.
The simple rules allow infinite variety.
"""

WIDTH = 80
HEIGHT = 24


def empty_grid(w=WIDTH, h=HEIGHT):
    return [[0] * w for _ in range(h)]


def place(grid, cells, ox=0, oy=0):
    """Place a pattern (list of (r,c) offsets) at origin (ox, oy)."""
    for r, c in cells:
        nr, nc = oy + r, ox + c
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            grid[nr][nc] = 1


def step_life(grid):
    h = len(grid)
    w = len(grid[0])
    new = [[0] * w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            neighbors = sum(
                grid[(r + dr) % h][(c + dc) % w]
                for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                if (dr, dc) != (0, 0)
            )
            if grid[r][c]:
                new[r][c] = 1 if neighbors in (2, 3) else 0
            else:
                new[r][c] = 1 if neighbors == 3 else 0
    return new


def count(grid):
    return sum(sum(row) for row in grid)


def render(grid, title, gen=0):
    print(f'  {title}  (gen {gen}, cells: {count(grid)})')
    print('  ┌' + '─' * WIDTH + '┐')
    for row in grid:
        print('  │' + ''.join('█' if c else ' ' for c in row) + '│')
    print('  └' + '─' * WIDTH + '┘')


# Pattern definitions (row, col offsets)

BLOCK = [(0,0),(0,1),(1,0),(1,1)]

BEEHIVE = [(0,1),(0,2),(1,0),(1,3),(2,1),(2,2)]

BLINKER = [(0,0),(0,1),(0,2)]

TOAD = [(0,1),(0,2),(0,3),(1,0),(1,1),(1,2)]

BEACON = [(0,0),(0,1),(1,0),(2,3),(3,2),(3,3)]

GLIDER = [(0,1),(1,2),(2,0),(2,1),(2,2)]

LWSS = [(0,1),(0,4),(1,0),(2,0),(2,4),(3,0),(3,1),(3,2),(3,3)]

PULSAR = [
    (0,2),(0,3),(0,4),(0,8),(0,9),(0,10),
    (2,0),(2,5),(2,7),(2,12),
    (3,0),(3,5),(3,7),(3,12),
    (4,0),(4,5),(4,7),(4,12),
    (5,2),(5,3),(5,4),(5,8),(5,9),(5,10),
    (7,2),(7,3),(7,4),(7,8),(7,9),(7,10),
    (8,0),(8,5),(8,7),(8,12),
    (9,0),(9,5),(9,7),(9,12),
    (10,0),(10,5),(10,7),(10,12),
    (12,2),(12,3),(12,4),(12,8),(12,9),(12,10),
]

PENTADECATHLON = [
    (0,1),
    (1,1),
    (2,0),(2,2),
    (3,1),(4,1),(5,1),(6,1),(7,1),(8,1),
    (9,0),(9,2),
    (10,1),(11,1),
]

R_PENTOMINO = [(0,1),(0,2),(1,0),(1,1),(2,1)]

DIEHARD = [(0,6),(1,0),(1,1),(2,1),(2,5),(2,6),(2,7)]

ACORN = [(0,1),(1,3),(2,0),(2,1),(2,4),(2,5),(2,6)]

GOSPER_GUN = [
    (0,24),
    (1,22),(1,24),
    (2,12),(2,13),(2,20),(2,21),(2,34),(2,35),
    (3,11),(3,15),(3,20),(3,21),(3,34),(3,35),
    (4,0),(4,1),(4,10),(4,16),(4,20),(4,21),
    (5,0),(5,1),(5,10),(5,14),(5,16),(5,17),(5,22),(5,24),
    (6,10),(6,16),(6,24),
    (7,11),(7,15),
    (8,12),(8,13),
]


def demo_pattern(pattern, name, steps_to_show):
    """Show a pattern evolving through given steps."""
    print(f'\n  ── {name} ──')

    # Find bounding box
    max_r = max(r for r, c in pattern)
    max_c = max(c for r, c in pattern)
    margin = 4
    h = min(max_r + 2 * margin, HEIGHT)
    w = min(max_c + 2 * margin, WIDTH)
    h = max(h, 10)
    w = max(w, 20)

    oy = margin
    ox = margin

    grid = empty_grid(w, h)
    place(grid, pattern, ox, oy)

    for gen in steps_to_show:
        g = empty_grid(w, h)
        place(g, pattern, ox, oy)
        for _ in range(gen):
            g = step_life(g)
        render(g, name, gen)
        print()


def main():
    print('Conway\'s Life — A Field Guide to Patterns\n')
    print('  The same rules. Different initial conditions. Different forever-afters.')
    print()

    # Still lifes
    print('  ═══ STILL LIFES ═══')
    for pat, name in [(BLOCK, 'Block (period ∞, 4 cells)'),
                      (BEEHIVE, 'Beehive (period ∞, 6 cells)')]:
        demo_pattern(pat, name, [0])

    # Oscillators
    print('  ═══ OSCILLATORS ═══')
    demo_pattern(BLINKER, 'Blinker (period 2)', [0, 1, 2])
    demo_pattern(BEACON, 'Beacon (period 2)', [0, 1])

    # Spaceship
    print('  ═══ SPACESHIPS ═══')
    demo_pattern(GLIDER, 'Glider (period 4, moves diagonally)', [0, 4, 8])

    # Complex patterns
    print('  ═══ COMPLEX BEHAVIORS ═══')

    # R-pentomino: run to see chaotic growth
    g = empty_grid()
    place(g, R_PENTOMINO, 30, 8)
    print(f'  ── R-pentomino (5 cells → chaos → stable after gen 1103) ──')
    for gen in [0, 50, 200]:
        g = empty_grid()
        place(g, R_PENTOMINO, 30, 8)
        for _ in range(gen):
            g = step_life(g)
        render(g, 'R-pentomino', gen)
        print()

    # Diehard
    print('  ── Diehard (dies completely after gen 130) ──')
    for gen in [0, 60, 130]:
        g = empty_grid(30, 12)
        place(g, DIEHARD, 5, 4)
        for _ in range(gen):
            g = step_life(g)
        render(g, 'Diehard', gen)
        print()

    print('  ═══ THE GLIDER GUN ═══')
    print('  Gosper Glider Gun (period 30) — emits a glider every 30 generations.')
    print('  First infinite growth pattern. Discovered by Bill Gosper, 1970.')
    print()
    for gen in [0, 30, 60, 90]:
        g = empty_grid()
        place(g, GOSPER_GUN, 1, 4)
        for _ in range(gen):
            g = step_life(g)
        render(g, 'Gosper Gun', gen)
        print()

    print('  Each glider fired by the gun travels forever (in infinite space).')
    print('  The gun disproved the conjecture that all Life patterns must either')
    print('  die or stabilize — infinite growth is possible from finite seeds.')
    print()
    print('  From three rules:')
    print('  Birth: 3 neighbors. Survival: 2 or 3. Death: otherwise.')
    print('  From these: still lifes, oscillators, spaceships, guns, and more.')
    print('  Life is Turing complete. Any computation can be implemented in Life.')


if __name__ == '__main__':
    main()
