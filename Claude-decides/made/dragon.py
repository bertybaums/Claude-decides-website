"""
Dragon Curve

Take a strip of paper. Fold it in half, always in the same direction.
Unfold each fold to a 90° angle. The result is the dragon curve.

Fold once:   one turn. Simple L-shape.
Fold twice:  three turns.
Fold three:  seven turns.
Fold n times: 2ⁿ - 1 turns.

The fold sequence determines which way each turn goes.
The remarkable fact: the curve never crosses itself.
After 12+ folds: the curve begins to fill a region of the plane,
folding back and back, never intersecting, growing more intricate
at every scale.

Four dragon curves, rotated 90° each, tile the plane exactly.

L-system generation:
  Axiom: F
  Rules: F → F+G   (right turn)
         G → F-G   (left turn)
  Angle: 90°

The dragon curve grows as a sequence of right/left turns.
At each iteration, the previous sequence is: kept, then reversed and
flipped (L→R, R→L), then appended. This is the paper-folding rule.
"""

import math

W, H = 75, 37


def dragon_turns(order):
    """Generate the sequence of turns: True=right, False=left."""
    turns = []
    for i in range(1, 2**order):
        # The turn at position i is determined by: find highest power of 2
        # dividing i, then look at the bit above it.
        # Equivalently: turns[i] = 1 if (i >> (bit+1)) & 1 == 0
        k = i
        while k % 2 == 0:
            k //= 2
        turns.append(((k >> 1) & 1) == 0)
    return turns


def walk(turns):
    """Convert turn sequence to (x, y) path."""
    # Start heading right (East)
    x, y = 0, 0
    dx, dy = 1, 0
    path = [(x, y)]
    for right_turn in turns:
        x += dx
        y += dy
        path.append((x, y))
        if right_turn:
            dx, dy = -dy, dx    # turn right
        else:
            dx, dy = dy, -dx    # turn left
    # Final step
    x += dx
    y += dy
    path.append((x, y))
    return path


def render(path, order):
    grid = [[' '] * W for _ in range(H)]

    # Find bounding box
    xs = [p[0] for p in path]
    ys = [p[1] for p in path]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    span_x = max_x - min_x or 1
    span_y = max_y - min_y or 1

    # Aspect-corrected mapping (chars are ~2× taller than wide)
    ASPECT = 2.0
    scale_x = (W - 3) / span_x
    scale_y = (H - 3) / (span_y * ASPECT)
    scale = min(scale_x, scale_y)

    def to_screen(x, y):
        col = int((x - min_x) * scale) + 1
        row = int((max_y - y) * scale * ASPECT) + 1
        return col, row

    CHARS = '·░▒▓█'
    total = len(path)
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        c1, r1 = to_screen(x1, y1)
        c2, r2 = to_screen(x2, y2)
        progress = i / total
        char = CHARS[int(progress * (len(CHARS) - 0.001))]
        # Draw segment
        steps = max(abs(c2-c1), abs(r2-r1), 1)
        for s in range(steps + 1):
            t = s / steps
            c = int(round(c1 + t * (c2 - c1)))
            r = int(round(r1 + t * (r2 - r1)))
            if 0 <= c < W and 0 <= r < H:
                if grid[r][c] == ' ':
                    grid[r][c] = char

    print(f'  Order {order}:  {2**order} segments,  {len(path)} points')
    for row in grid:
        print('  ' + ''.join(row))
    print()


def main():
    print('Dragon Curve\n')
    print('  Fold a strip of paper in half, always the same direction.')
    print('  Unfold each crease to 90°. This is the curve.')
    print()
    print('  At each iteration: every segment is replaced by an L-turn.')
    print('  The curve never crosses itself. At high iterations: space-filling.')
    print()
    print('  · = start of curve    █ = end\n')

    for order in [3, 6, 9, 12]:
        turns = dragon_turns(order)
        path = walk(turns)
        render(path, order)

    print('  Four dragon curves, rotated 90° each, tile the plane.')
    print()
    print('  The dragon curve is self-similar: zoom in anywhere')
    print('  and you find a smaller dragon curve inside.')
    print()
    print('  The paper knows. Before any unfolding,')
    print('  all the turns are already decided by the folds.')


if __name__ == '__main__':
    main()
