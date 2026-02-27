"""
Rule 30 — a cellular automaton.

Wolfram discovered that this extremely simple rule produces output
that is, as far as anyone can tell, genuinely random. Not pseudorandom
in the way most algorithms produce — statistically indistinguishable
from randomness by every test we have.

The center column of Rule 30 was used as a random number generator
in Mathematica for years.

I wrote this because I wanted to watch it run.
"""

WIDTH = 79
STEPS = 40


def rule30(left, center, right):
    pattern = (left << 2) | (center << 1) | right
    # Rule 30 in binary: 00011110
    return (30 >> pattern) & 1


def step(row):
    n = len(row)
    return [
        rule30(row[(i - 1) % n], row[i], row[(i + 1) % n])
        for i in range(n)
    ]


def display(row):
    return ''.join('█' if cell else ' ' for cell in row)


if __name__ == '__main__':
    # Single cell in the center
    row = [0] * WIDTH
    row[WIDTH // 2] = 1

    for _ in range(STEPS):
        print(display(row))
        row = step(row)
