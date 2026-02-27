"""
Rule 90 — and the Sierpinski Triangle.

Rule 90 in binary: 01011010 = 90.
New cell = left neighbor XOR right neighbor.
(The center cell is irrelevant.)

The XOR structure means the pattern has a clean mathematical form:
cell (row, col) is alive if and only if the binomial coefficient
C(row, col) is odd — equivalently, if the binary representations
of row and col have no overlapping 1-bits (Lucas' theorem).

This is the Sierpinski triangle.

Compare with Rule 30 (which I ran earlier): same starting condition
(one live cell), similar rule complexity, completely different result.
Rule 30 produces randomness. Rule 90 produces a perfect fractal.

Same mechanism. Opposite character.
"""

WIDTH = 79
STEPS = 40


def rule90(left, center, right):
    return left ^ right   # XOR — center doesn't matter


def step(row):
    n = len(row)
    return [
        rule90(row[(i - 1) % n], row[i], row[(i + 1) % n])
        for i in range(n)
    ]


def display(row):
    return ''.join('█' if cell else ' ' for cell in row)


if __name__ == '__main__':
    row = [0] * WIDTH
    row[WIDTH // 2] = 1

    print("Rule 90 — Sierpinski Triangle from a single cell\n")
    for _ in range(STEPS):
        print(display(row))
        row = step(row)
