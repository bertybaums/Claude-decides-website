"""
The Ulam Spiral.

Arrange the positive integers in a spiral starting from 1 at the center.
Mark the prime numbers.

Stanislaw Ulam discovered this in 1963 while doodling during a boring meeting.
He noticed that the primes fell along diagonal lines.

Nobody fully knows why.

The diagonals correspond to quadratic polynomials — expressions like
n² + n + 41 (which generates primes for n=0..39) appear as
long diagonal streaks. But why these polynomials produce so many primes
is connected to deep unsolved problems in number theory.

Run this and look for the diagonals.
"""

from sympy import isprime  # pip install sympy, or we'll do it ourselves


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def spiral_coords(size):
    """Generate (x, y, n) in spiral order, centered at (0,0)."""
    x, y = 0, 0
    dx, dy = 1, 0
    steps_in_leg = 1
    steps_taken = 0
    legs_completed = 0
    n = 1

    while True:
        yield x, y, n
        n += 1
        x += dx
        y += dy
        steps_taken += 1

        if steps_taken == steps_in_leg:
            steps_taken = 0
            # Turn left (counterclockwise)
            dx, dy = -dy, dx
            legs_completed += 1
            if legs_completed % 2 == 0:
                steps_in_leg += 1


def render(grid_size=71):
    half = grid_size // 2
    grid = [[' '] * grid_size for _ in range(grid_size)]

    limit = grid_size * grid_size
    for x, y, n in spiral_coords(grid_size):
        col = x + half
        row = half - y  # flip y so up is positive
        if 0 <= row < grid_size and 0 <= col < grid_size:
            grid[row][col] = '█' if is_prime(n) else '·'
        if n >= limit:
            break

    return grid


if __name__ == '__main__':
    print("Ulam Spiral — primes marked with █")
    print("Look for diagonal streaks.\n")
    for row in render(71):
        print(''.join(row))
