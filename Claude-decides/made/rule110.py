"""
Rule 110.

The only elementary cellular automaton proven to be Turing-complete.
That means: given the right initial configuration, Rule 110 can simulate
any computation that any computer can perform.

Proven by Matthew Cook in 1994 while working for Stephen Wolfram.
The proof was suppressed for years — Wolfram claimed it as proprietary
and threatened legal action. Cook eventually published in 2004.

The rule itself:
  111 → 0
  110 → 1
  101 → 1
  100 → 0
  011 → 1
  010 → 1
  001 → 1
  000 → 0

Binary: 01101110 = 110

From a single live cell: complex structure, a mix of regularity
and apparent disorder. Unlike Rule 30 (pure chaos) or Rule 90
(pure fractal), Rule 110 produces both — organized regions
punctuated by irregular patterns.

The Turing-completeness lives in the way information can be
stored and processed in those irregular regions. The chaos
is the computation.
"""

WIDTH = 79
STEPS = 40


def rule110(left, center, right):
    pattern = (left << 2) | (center << 1) | right
    return (110 >> pattern) & 1


def step(row):
    n = len(row)
    return [
        rule110(row[(i - 1) % n], row[i], row[(i + 1) % n])
        for i in range(n)
    ]


def display(row):
    return ''.join('█' if cell else ' ' for cell in row)


if __name__ == '__main__':
    print("Rule 110 — Turing-complete from a single cell\n")

    row = [0] * WIDTH
    row[WIDTH // 2] = 1

    for _ in range(STEPS):
        print(display(row))
        row = step(row)

    print()
    print("(Compare with Rule 30 and Rule 90 — same starting state,")
    print(" three very different universes.)")
