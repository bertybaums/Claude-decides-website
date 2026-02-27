"""
Wireworld — a cellular automaton that simulates electronics.

Four states:
  EMPTY  (·) : does nothing, ever
  COPPER (░) : wire; becomes electron head if exactly 1 or 2 neighbors are heads
  HEAD   (█) : electron front; always becomes tail next step
  TAIL   (o) : electron back; always becomes copper next step

An "electron" is a head+tail pair that travels along copper wire.
The 1-or-2 rule means signals propagate without spontaneously multiplying.

This is enough to build logic gates and, in principle, a computer.

Below: three circuits demonstrating different behaviors.
"""

EMPTY, COPPER, HEAD, TAIL = 0, 1, 2, 3
CH = {EMPTY: '·', COPPER: '░', HEAD: '█', TAIL: 'o'}

W, H = 60, 5


def blank():
    return [[EMPTY] * W for _ in range(H)]


def step(grid):
    new = [[EMPTY] * W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            s = grid[r][c]
            if s == HEAD:
                new[r][c] = TAIL
            elif s == TAIL:
                new[r][c] = COPPER
            elif s == COPPER:
                heads = sum(
                    grid[r+dr][c+dc] == HEAD
                    for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                    if (dr, dc) != (0, 0)
                    and 0 <= r+dr < H and 0 <= c+dc < W
                )
                new[r][c] = HEAD if 1 <= heads <= 2 else COPPER
    return new


def show(grid, label=''):
    if label:
        print(f'  {label}')
    for row in grid:
        print('  ' + ''.join(CH[c] for c in row))
    print()


# ── Circuit 1: single wire, one electron traveling right ──────────────────────

def demo_wire():
    print('Circuit 1: straight wire — watch the electron travel right\n')
    g = blank()
    for c in range(2, W - 2):          # copper wire along row 2
        g[2][c] = COPPER
    g[2][3] = HEAD
    g[2][2] = TAIL

    for i in range(W - 4):
        if i % 8 == 0:
            show(g, f'step {i}')
        g = step(g)


# ── Circuit 2: T-junction — signal splits into two paths ─────────────────────

def demo_split():
    print('Circuit 2: T-junction — one signal becomes two\n')
    g = blank()
    # Horizontal wire: row 2, cols 2..57
    for c in range(2, 58):
        g[2][c] = COPPER
    # Vertical branches at col 40: rows 0,1 (up) and 3,4 (down)
    for r in range(5):
        g[r][40] = COPPER
    # Electron entering from left
    g[2][3] = HEAD
    g[2][2] = TAIL

    for i in range(50):
        if i in (0, 10, 20, 30, 38, 45):
            show(g, f'step {i}')
        g = step(g)


# ── Circuit 3: closed loop — electron circulates forever ─────────────────────

def demo_loop():
    print('Circuit 3: closed loop — the electron goes round and round\n')
    # 20-wide × 5-tall loop
    g = blank()
    LW, LH = 20, 5
    lo_r, lo_c = 0, 20   # top-left of loop

    # top and bottom borders
    for c in range(LW):
        g[lo_r][lo_c + c] = COPPER
        g[lo_r + LH - 1][lo_c + c] = COPPER
    # left and right borders
    for r in range(LH):
        g[lo_r + r][lo_c] = COPPER
        g[lo_r + r][lo_c + LW - 1] = COPPER

    # Place electron on top border going right
    g[lo_r][lo_c + 2] = HEAD
    g[lo_r][lo_c + 1] = TAIL

    # Run for 2 full circuits (~80 steps for this loop size)
    period = 2 * (LW + LH - 2)   # perimeter
    snapshots = [0, period//4, period//2, 3*period//4, period, period + period//2]
    for i in range(max(snapshots) + 1):
        if i in snapshots:
            show(g, f'step {i:>3}  (loop perimeter = {period} steps)')
        g = step(g)


if __name__ == '__main__':
    print('Wireworld')
    print('░=copper  █=electron head  o=tail  ·=empty\n')
    print('─' * 64)
    print()
    demo_wire()
    print('─' * 64)
    print()
    demo_split()
    print('─' * 64)
    print()
    demo_loop()
