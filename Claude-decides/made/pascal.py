"""
Pascal's Triangle.

One rule: each number is the sum of the two above it.

Here is what that single rule contains:

  Powers of 2         — each row sums to 2^n
  Counting numbers    — run down the left edge: 1, 2, 3, 4...
  Triangular numbers  — next diagonal: 1, 3, 6, 10, 15...
  Tetrahedral numbers — next: 1, 4, 10, 20, 35...
  Fibonacci numbers   — appear as sums of shallow diagonals
  Binomial theorem    — row n gives the expansion of (a+b)^n
  Sierpinski triangle — color the odd entries; it appears

All of this is already in: each number equals the sum of the two above it.
The rule is the smallest possible version of the triangle.
"""


def pascal(n_rows):
    tri = [[1]]
    for i in range(1, n_rows):
        prev = tri[-1]
        row = [1] + [prev[j] + prev[j + 1] for j in range(len(prev) - 1)] + [1]
        tri.append(row)
    return tri


def display(tri, n_rows=None):
    """Show triangle as numbers, centered."""
    rows = tri[:n_rows] if n_rows else tri
    max_w = sum(len(str(x)) + 2 for x in rows[-1])
    for row in rows:
        s = '  '.join(str(x) for x in row)
        pad = (max_w - len(s)) // 2
        print(' ' * pad + s)


def display_mod2(tri):
    """Show odd/even — reveals the Sierpinski triangle."""
    n = len(tri)
    for i, row in enumerate(tri):
        pad = ' ' * (n - i - 1)
        s = ' '.join('█' if x % 2 else '·' for x in row)
        print(pad + s)


def fibonacci_from_diagonals(tri):
    """
    Fibonacci sequence appears in the shallow diagonal sums.
    Diagonal d: sum of tri[d][0], tri[d-1][1], tri[d-2][2], ...
    """
    n = len(tri)
    result = []
    for d in range(n):
        total = 0
        row, col = d, 0
        while row >= 0 and col < len(tri[row]):
            total += tri[row][col]
            row -= 1
            col += 1
        result.append(total)
    return result


if __name__ == '__main__':
    tri = pascal(20)

    print("Pascal's Triangle")
    print("Rule: each number is the sum of the two above it.\n")

    print("First 12 rows:\n")
    display(tri, 12)

    print()
    print("Each row sums to a power of 2:")
    for i in range(10):
        print(f"  Row {i:2d}:  sum = {sum(tri[i]):6d}  =  2^{i} = {2 ** i}")

    print()
    print("Second diagonal — triangular numbers:")
    print("  " + ", ".join(str(tri[n][1]) for n in range(1, 12)))
    print("  (each one is 1+2+3+...+n)")

    print()
    fibs = fibonacci_from_diagonals(tri)
    print("Shallow diagonal sums — Fibonacci sequence hidden in the structure:")
    print("  " + ", ".join(str(x) for x in fibs[:13]))

    print()
    print("Odd entries (█) and even entries (·) — all 20 rows.")
    print("The Sierpinski triangle emerges:\n")
    display_mod2(tri)

    print()
    print("This is not a coincidence.")
    print("The Sierpinski triangle is what you get when you ask:")
    print("  'which entries of Pascal's triangle are odd?'")
    print("The answer turns out to be fractal.")
