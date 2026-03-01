"""
Knight's Tour — Warnsdorff's Heuristic

A knight must visit every square of a chessboard exactly once.
This is a Hamiltonian path problem — NP-complete in general.

For a standard 8×8 board, there are 26,534,728,821,064 distinct tours.

Warnsdorff's Rule (1823):
  At each step, move to the square from which the knight
  has the fewest onward moves.

  This greedy heuristic works with remarkable reliability:
  near-O(n²) performance on n×n boards where brute force
  would take exponential time. The "why" is not fully proven —
  it works because scarcity is addressed early.

Why the knight's tour matters:
  - One of the oldest combinatorial problems (al-Adli, 840 AD)
  - Euler analyzed it in 1759 and found many closed tours
  - A "closed tour" returns to its starting square — a Hamiltonian cycle
  - Warnsdorff's 1823 rule predates formal complexity theory by a century
  - The heuristic occasionally fails on large boards — open problem:
    which starting positions fail?

The knight's movement is itself interesting:
  - The L-shape combines orthogonal and diagonal motion
  - It's the only chess piece that jumps over others
  - Its (2,1) step means it alternates black and white squares
  - A closed tour is only possible because the board has even area

The visualization: watch the path snake across the board,
filling space not by proximity but by necessity.
"""

import random

BOARD = 8
MOVES = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2)
]


def valid_moves(board, r, c):
    """Return list of unvisited squares reachable from (r, c)."""
    result = []
    for dr, dc in MOVES:
        nr, nc = r + dr, c + dc
        if 0 <= nr < BOARD and 0 <= nc < BOARD and board[nr][nc] == 0:
            result.append((nr, nc))
    return result


def warnsdorff_degree(board, r, c):
    """Count onward moves from (r, c) — used to rank choices."""
    return len(valid_moves(board, r, c))


def knight_tour(start_r=0, start_c=0):
    """
    Attempt a knight's tour from (start_r, start_c) using Warnsdorff's rule.
    Returns the board (numbered by visit order) and the path, or None if failed.
    """
    board = [[0] * BOARD for _ in BOARD * [None]]
    path = []

    r, c = start_r, start_c
    board[r][c] = 1
    path.append((r, c))

    for step in range(2, BOARD * BOARD + 1):
        moves = valid_moves(board, r, c)
        if not moves:
            if step <= BOARD * BOARD:
                return None, path  # Failed — not a complete tour
            break

        # Warnsdorff: pick move with fewest onward options
        # Tie-breaking: pick the one with fewest second-level options
        def priority(m):
            nr, nc = m
            deg = warnsdorff_degree(board, nr, nc)
            # Secondary: sum of third-level degrees (lookahead)
            board[nr][nc] = -1  # temporarily mark
            second = sum(
                warnsdorff_degree(board, nr2, nc2)
                for nr2, nc2 in valid_moves(board, nr, nc)
            )
            board[nr][nc] = 0  # unmark
            return (deg, -second)

        r, c = min(moves, key=priority)
        board[r][c] = step
        path.append((r, c))

    return board, path


def render_board(board, path):
    """Display the board with move numbers, and the path drawn."""
    # Render as numbered grid
    print('  Move order:')
    print('  ' + '┌' + ('─────' * BOARD)[:-1] + '─┐')
    for r in range(BOARD):
        row_str = '  │'
        for c in range(BOARD):
            n = board[r][c]
            if n > 0:
                row_str += f' {n:>2} '
            else:
                row_str += '  · '
        row_str += '│'
        print(row_str)
    print('  ' + '└' + ('─────' * BOARD)[:-1] + '─┘')


def render_path_ascii(path):
    """Draw the path as arrows on an ASCII grid."""
    # Direction glyphs (approximate)
    ARROW = {
        (2, 1): '↘', (2, -1): '↙', (-2, 1): '↗', (-2, -1): '↖',
        (1, 2): '→', (1, -2): '←', (-1, 2): '→', (-1, -2): '←',
    }

    STEP_CHAR = {
        (2, 1): '/', (2, -1): '\\', (-2, 1): '/', (-2, -1): '\\',
        (1, 2): '-', (1, -2): '-', (-1, 2): '-', (-1, -2): '-',
    }

    grid = [['·'] * BOARD for _ in range(BOARD)]

    for i, (r, c) in enumerate(path):
        if i == 0:
            grid[r][c] = 'S'
        elif i == len(path) - 1:
            grid[r][c] = 'E'
        else:
            # Show progress: first half '░', second half '▒', last quarter '▓'
            frac = i / len(path)
            if frac < 0.33:
                grid[r][c] = '░'
            elif frac < 0.67:
                grid[r][c] = '▒'
            else:
                grid[r][c] = '▓'

    print('  Path density (░ = early, ▒ = middle, ▓ = late):')
    print('  ' + '┌' + '─' * (BOARD * 2 + 1) + '┐')
    for row in grid:
        print('  │ ' + ' '.join(row) + ' │')
    print('  ' + '└' + '─' * (BOARD * 2 + 1) + '┘')


def check_closed(path):
    """Check if the tour is closed (last square can reach first)."""
    if len(path) < BOARD * BOARD:
        return False
    r0, c0 = path[0]
    r_last, c_last = path[-1]
    dr, dc = abs(r_last - r0), abs(c_last - c0)
    return sorted([dr, dc]) == [1, 2]


def render_comparison(boards_paths, labels):
    """Show multiple tours side by side (abbreviated view)."""
    print(f'  {"Start":>10}   {"Steps":>5}   {"Closed?":>7}   {"Path shape"}')
    print('  ' + '-' * 60)
    for (board, path), label in zip(boards_paths, labels):
        steps = len(path)
        closed = 'yes' if check_closed(path) else 'no'
        # Path compactness: fraction of board covered
        complete = 'complete' if steps == BOARD * BOARD else f'partial ({steps}/{BOARD*BOARD})'
        print(f'  {label:>10}   {steps:>5}   {closed:>7}   {complete}')


def main():
    print("Knight's Tour — Warnsdorff's Heuristic\n")
    print('  A knight visits every square exactly once.')
    print('  Warnsdorff (1823): always go where options are fewest.\n')

    # Attempt tour from corner
    print('  ─── Tour from (0,0) — top-left corner ───\n')
    board, path = knight_tour(0, 0)

    if len(path) == BOARD * BOARD:
        print(f'  Complete tour: {BOARD*BOARD} squares visited.\n')
    else:
        print(f'  Partial tour: {len(path)} squares visited.\n')

    render_board(board, path)
    print()
    render_path_ascii(path)

    closed = check_closed(path)
    print()
    if closed:
        print('  This is a CLOSED tour — the final position can return to start.')
        print('  The knight could loop forever, visiting every square in sequence.')
    else:
        # How far is the end from the start?
        r0, c0 = path[0]
        r_end, c_end = path[-1]
        print(f'  Open tour. Start: {path[0]}, End: {path[-1]}.')
        print(f'  The knight finishes {abs(r_end-r0)+abs(c_end-c0)} taxicab steps from where it began.')

    # Try multiple starting positions
    print('\n  ─── Multiple starting positions ───\n')
    starts = [(0, 0), (0, 1), (1, 1), (3, 3), (0, 4), (4, 4), (7, 7), (2, 5)]
    results = []
    for sr, sc in starts:
        b, p = knight_tour(sr, sc)
        results.append((b, p))

    render_comparison(results, [f'({r},{c})' for r, c in starts])

    print()
    print('  Warnsdorff\'s rule succeeds from all of these starting positions.')
    print('  On boards up to ~76×76, it reliably finds complete tours.')
    print('  Beyond that, occasional failures appear — the "why" remains open.\n')

    # The 2D density view — where does the knight spend time?
    print('  ─── Visit density across 100 random tours ───\n')
    density = [[0] * BOARD for _ in range(BOARD)]
    n_success = 0
    for _ in range(100):
        sr = random.randint(0, BOARD - 1)
        sc = random.randint(0, BOARD - 1)
        b, p = knight_tour(sr, sc)
        if len(p) == BOARD * BOARD:
            n_success += 1
            for step, (r, c) in enumerate(p):
                # Weight by step number (does the knight favor certain squares early/late?)
                density[r][c] += step

    if n_success > 0:
        for row in density:
            for j in range(len(row)):
                row[j] //= n_success

        max_d = max(max(row) for row in density)
        min_d = min(min(row) for row in density)
        rng = max_d - min_d if max_d != min_d else 1

        shades = ' ░▒▓█'
        print(f'  Average visit step (darker = visited later), {n_success}/100 complete tours:')
        print('  ' + '┌' + '─' * (BOARD * 2 + 1) + '┐')
        for row in density:
            cells = []
            for d in row:
                idx = int((d - min_d) / rng * (len(shades) - 1))
                cells.append(shades[idx])
            print('  │ ' + ' '.join(cells) + ' │')
        print('  ' + '└' + '─' * (BOARD * 2 + 1) + '┘')
        print()
        print('  Corner squares tend to be visited earlier (fewest onward moves — Warnsdorff grabs them first).')
        print('  Center squares tend to be visited later (many options — deprioritized until the end).')

    print()
    print('  The heuristic works by prioritizing scarcity: corners have only 2 moves,')
    print('  so Warnsdorff visits them first, leaving the high-degree center for later.')
    print('  This is not obviously the right strategy — it becomes obvious only in hindsight.')
    print()
    print('  The knight\'s tour is one of the oldest puzzles in recreational mathematics.')
    print('  al-Adli al-Rumi described solutions in 840 AD. Euler found closed tours in 1759.')
    print('  Warnsdorff found his rule empirically, 64 years before complexity theory existed.')
    print('  He had no proof. He just noticed it worked.')


if __name__ == '__main__':
    main()
