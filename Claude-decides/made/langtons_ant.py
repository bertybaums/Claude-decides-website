"""
Langton's Ant.

An ant sits on an infinite grid of white squares.

Rules:
  On a WHITE square: turn right 90°, flip the square to black, move forward.
  On a BLACK square: turn left 90°, flip the square to white, move forward.

That's everything.

For roughly the first 10,000 steps: apparently random, chaotic scribbling.
Around step 10,000: the ant spontaneously begins building a "highway" —
a repeating diagonal pattern that extends forever.

Nobody predicted this. Nobody proved it would happen.
It just does.

This script prints snapshots so you can watch the transition.
"""

# Directions: 0=UP, 1=RIGHT, 2=DOWN, 3=LEFT
DR = [-1,  0, 1, 0]
DC = [ 0,  1, 0, -1]

def run(steps):
    black = set()
    r, c = 0, 0
    direction = 0  # facing up

    for _ in range(steps):
        if (r, c) in black:
            direction = (direction - 1) % 4   # turn left
            black.remove((r, c))
        else:
            direction = (direction + 1) % 4   # turn right
            black.add((r, c))
        r += DR[direction]
        c += DC[direction]

    return black, (r, c)


def display(black, ant_pos, step, pad=2):
    if not black:
        print(f"--- Step {step}: empty grid ---\n")
        return

    rows = [r for r, c in black]
    cols = [c for r, c in black]
    ar, ac = ant_pos
    rows.append(ar); cols.append(ac)

    min_r, max_r = min(rows) - pad, max(rows) + pad
    min_c, max_c = min(cols) - pad, max(cols) + pad

    # Cap display size
    if max_r - min_r > 60:
        mid_r = (min(r for r,c in black) + max(r for r,c in black)) // 2
        min_r, max_r = mid_r - 30, mid_r + 30
    if max_c - min_c > 100:
        mid_c = (min(c for r,c in black) + max(c for r,c in black)) // 2
        min_c, max_c = mid_c - 50, mid_c + 50

    print(f"--- Step {step:>6} | {len(black)} black cells ---")
    for r in range(min_r, max_r + 1):
        line = []
        for c in range(min_c, max_c + 1):
            if (r, c) == ant_pos:
                line.append('◆')
            elif (r, c) in black:
                line.append('█')
            else:
                line.append('·')
        print(''.join(line))
    print()


if __name__ == '__main__':
    for step in [100, 500, 2000, 8000, 10500, 12000]:
        black, ant = run(step)
        display(black, ant, step)
