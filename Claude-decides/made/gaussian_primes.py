"""
Gaussian Integers and Gaussian Primes

The Gaussian integers are ℤ[i] = {a + bi : a, b ∈ ℤ}
— the complex numbers with integer real and imaginary parts.

They form a ring: you can add, subtract, and multiply them,
and you get back a Gaussian integer. Division works too,
if the result is a Gaussian integer.

Norm: N(a + bi) = a² + b² (the squared magnitude)
  N(z · w) = N(z) · N(w)  — norms multiply

Units: ±1, ±i (the four elements with norm 1)

A Gaussian prime is a Gaussian integer that cannot be written as
a product of two non-unit Gaussian integers.

Which ordinary primes remain prime in ℤ[i]?
  - 2 = -i(1+i)² — NOT a Gaussian prime (ramifies)
  - p ≡ 1 (mod 4): splits into two conjugate Gaussian primes
    e.g., 5 = (2+i)(2-i)
  - p ≡ 3 (mod 4): stays prime in ℤ[i]
    e.g., 3, 7, 11, 19, 23 are Gaussian primes

This pattern is deep: it's Fermat's theorem on sums of two squares.
A prime p can be written as p = a² + b² if and only if p = 2 or p ≡ 1 (mod 4).
The primes that stay prime in ℤ[i] are exactly those that CANNOT be so written.

The Gaussian primes have a beautiful visual pattern:
they appear in "crosses" rotated by 90° (because i is a unit),
and they cluster along circles of increasing radius (norm).
Their distribution in the complex plane has been studied for over 150 years.

Open problem: the Gaussian prime spiral.
Starting at 0, moving in direction +1, turning 90° left at each Gaussian prime
you encounter — does this walk reach every Gaussian prime? Unknown.
"""

import math


def norm(a, b):
    return a * a + b * b


def is_gaussian_prime(a, b):
    """
    Test if a + bi is a Gaussian prime.

    a + bi is a Gaussian prime iff one of:
    1. a = 0 and |b| is a rational prime ≡ 3 (mod 4)
    2. b = 0 and |a| is a rational prime ≡ 3 (mod 4)
    3. a,b both nonzero and N(a+bi) = a² + b² is a rational prime

    (The rational primes ≡ 3 mod 4 cannot be written as sums of two squares,
    so they stay prime in ℤ[i]. Primes ≡ 1 mod 4 split: p = (a+bi)(a-bi).)
    """
    if a == 0 and b == 0:
        return False
    n = norm(a, b)
    if n == 1:
        return False  # units: ±1, ±i
    if b == 0:
        abs_a = abs(a)
        return is_rational_prime(abs_a) and abs_a % 4 == 3
    if a == 0:
        abs_b = abs(b)
        return is_rational_prime(abs_b) and abs_b % 4 == 3
    # Both nonzero: prime iff norm is a rational prime
    return is_rational_prime(n)


def is_rational_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def gaussian_primes_in_region(radius):
    """Return all Gaussian primes a + bi with |a|, |b| <= radius."""
    primes = []
    r = int(radius)
    for a in range(-r, r + 1):
        for b in range(-r, r + 1):
            if is_gaussian_prime(a, b):
                primes.append((a, b))
    return primes


def render_gaussian_plane(radius=20, width=60, height=30):
    """
    Render the Gaussian integers in a region, marking primes.
    """
    grid = [[' '] * width for _ in range(height)]

    # Map Gaussian plane to grid
    def to_screen(a, b):
        cx = width // 2
        cy = height // 2
        # Scale to fit in grid
        scale_x = (width // 2 - 1) / radius
        scale_y = (height // 2 - 1) / radius
        sx = int(cx + a * scale_x)
        sy = int(cy - b * scale_y)  # flip y (screen y goes down)
        return sx, sy

    # Mark axes
    for a in range(-int(radius), int(radius) + 1):
        sx, sy = to_screen(a, 0)
        if 0 <= sx < width and 0 <= sy < height:
            if grid[sy][sx] == ' ':
                grid[sy][sx] = '·'
    for b in range(-int(radius), int(radius) + 1):
        sx, sy = to_screen(0, b)
        if 0 <= sx < width and 0 <= sy < height:
            if grid[sy][sx] == ' ':
                grid[sy][sx] = '·'

    # Mark Gaussian primes
    primes = gaussian_primes_in_region(radius)
    for a, b in primes:
        sx, sy = to_screen(a, b)
        if 0 <= sx < width and 0 <= sy < height:
            # Use different markers by type
            if b == 0:  # real axis
                grid[sy][sx] = '▪'
            elif a == 0:  # imaginary axis
                grid[sy][sx] = '▪'
            else:
                n = norm(a, b)
                if n <= 50:
                    grid[sy][sx] = '█'
                elif n <= 200:
                    grid[sy][sx] = '▓'
                else:
                    grid[sy][sx] = '░'

    # Origin
    sx, sy = to_screen(0, 0)
    if 0 <= sx < width and 0 <= sy < height:
        grid[sy][sx] = '+'

    print('  ┌' + '─' * width + '┐')
    for row in grid:
        print('  │' + ''.join(row) + '│')
    print('  └' + '─' * width + '┘')
    print(f'  ▪ = prime on real/imaginary axis; █ = prime (norm ≤ 50); ░ = prime (larger norm)')


def show_factorization_table():
    """Show how ordinary primes factor in the Gaussian integers."""
    print('  How ordinary primes behave in ℤ[i]:')
    print()
    print(f'  {"p":>4}   {"p mod 4":>7}   {"Behavior":>9}   {"Factorization"}')
    print('  ' + '-' * 65)

    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        mod4 = p % 4
        if p == 2:
            behavior = 'ramifies'
            factor_str = '−i(1+i)²  [N(1+i)=2]'
        elif mod4 == 3:
            behavior = 'stays prime'
            factor_str = f'{p} is a Gaussian prime'
        else:  # mod4 == 1
            # Find a² + b² = p
            a, b = 0, 0
            for candidate_a in range(1, p):
                remainder = p - candidate_a * candidate_a
                if remainder > 0:
                    candidate_b = int(math.isqrt(remainder))
                    if candidate_b * candidate_b == remainder and candidate_b > 0:
                        a, b = candidate_a, candidate_b
                        break
            behavior = 'splits'
            factor_str = f'({a}+{b}i)({a}−{b}i)  [N={a}²+{b}²={p}]'

        print(f'  {p:>4}   {mod4:>7}   {behavior:>9}   {factor_str}')


def show_gaussian_prime_properties():
    """Illustrate key properties of Gaussian primes."""
    print('  Properties of specific Gaussian primes:')
    print()
    print(f'  {"z":>10}   {"N(z)":>5}   {"Prime?":>6}   {"z mod 4 meaning"}')
    print('  ' + '-' * 55)

    examples = [
        (1+0j, 1, 0), (2+1j, 2, 1), (1+2j, 1, 2),
        (3+0j, 3, 0), (2+3j, 2, 3), (3+2j, 3, 2),
        (5+0j, 5, 0), (1+4j, 1, 4), (4+1j, 4, 1),
        (7+0j, 7, 0), (3+4j, 3, 4), (4+3j, 4, 3),
        (11+0j, 11, 0), (5+4j, 5, 4), (4+5j, 4, 5),
    ]

    for _, a, b in examples:
        n = norm(a, b)
        prime = is_gaussian_prime(a, b)
        z_str = f'{a}+{b}i' if b >= 0 else f'{a}{b}i'
        prime_str = 'YES' if prime else 'no'
        print(f'  {z_str:>10}   {n:>5}   {prime_str:>6}')

    print()
    print('  Conjugate pairs: if a+bi is prime, so is a-bi')
    print('  Rotations: if z is prime, so are iz, -z, -iz (units multiply primes → primes)')
    print('  This 4-fold symmetry means Gaussian primes come in "cross" clusters of 4')
    print('  (or 8 if a ≠ b ≠ 0: four rotations × two from conjugate)')


def gaussian_prime_walk():
    """
    The Gaussian prime spiral: start at 0, walk until you hit a prime,
    turn left 90°, continue. Where does it go?
    """
    print('  The Gaussian prime walk:')
    print('  Start at origin. Walk in +real direction.')
    print('  Each time you reach a Gaussian prime, turn 90° counterclockwise.')
    print()

    # Directions: 0=+real, 1=+imag, 2=-real, 3=-imag
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    a, b = 0, 0
    direction = 0  # start going right
    positions = [(a, b)]
    turns = 0
    steps = 0

    for _ in range(200):
        da, db = dirs[direction]
        a += da
        b += db
        steps += 1
        positions.append((a, b))

        if is_gaussian_prime(a, b):
            direction = (direction + 1) % 4  # turn left
            turns += 1

        if turns >= 20:
            break

    # Render the path
    if positions:
        min_a = min(p[0] for p in positions)
        max_a = max(p[0] for p in positions)
        min_b = min(p[1] for p in positions)
        max_b = max(p[1] for p in positions)

        w = max_a - min_a + 3
        h = max_b - min_b + 3

        # Cap size
        w = min(w, 60)
        h = min(h, 20)

        grid = [[' '] * w for _ in range(h)]

        pos_set = set()
        for i, (pa, pb) in enumerate(positions):
            ga = pa - min_a + 1
            gb = (max_b - pb) + 1  # flip y
            if 0 <= ga < w and 0 <= gb < h:
                if is_gaussian_prime(pa, pb):
                    grid[gb][ga] = '█'
                elif i == 0:
                    grid[gb][ga] = 'S'
                else:
                    grid[gb][ga] = '·'
                pos_set.add((pa, pb))

        print('  Walk path (S=start, █=Gaussian prime where we turned):')
        print('  ┌' + '─' * w + '┐')
        for row in grid:
            print('  │' + ''.join(row) + '│')
        print('  └' + '─' * w + '┘')
        print(f'  Walk: {steps} steps, {turns} turns at Gaussian primes')
        print(f'  Current position after {turns} turns: ({a}, {b})')
        print()
        print('  Does this walk visit every Gaussian prime?')
        print('  Does it ever return to the origin?')
        print('  Both questions are open. No one knows.')


def main():
    print('Gaussian Integers and Gaussian Primes\n')
    print('  ℤ[i] = {a + bi : a, b integers}')
    print('  The complex numbers with integer coordinates.')
    print()

    print('  ─── HOW ORDINARY PRIMES FACTOR IN ℤ[i] ───\n')
    show_factorization_table()

    print()
    print('  Fermat\'s theorem on sums of two squares:')
    print('  p can be written a² + b² ⟺ p = 2 or p ≡ 1 (mod 4)')
    print('  These are exactly the primes that SPLIT in the Gaussian integers.')
    print('  The primes that ≡ 3 (mod 4) cannot be sums of squares — they STAY prime.')
    print()

    print('  ─── GAUSSIAN PRIME PROPERTIES ───\n')
    show_gaussian_prime_properties()

    print()
    print('  ─── GAUSSIAN PRIMES IN THE COMPLEX PLANE ───\n')
    print('  Radius 20 region (Re and Im from -20 to +20):')
    print()
    render_gaussian_plane(radius=20, width=64, height=30)

    # Count primes in region
    primes = gaussian_primes_in_region(20)
    print(f'\n  Gaussian primes in radius-20 region: {len(primes)}')
    print(f'  (Including all four unit rotations of each prime)')

    print()
    print('  ─── THE GAUSSIAN PRIME SPIRAL WALK ───\n')
    gaussian_prime_walk()

    print()
    print('  ─── NOTES ───')
    print()
    print('  The Gaussian integers form a Euclidean domain:')
    print('  there is a division algorithm (with remainder), so unique factorization holds.')
    print('  Every Gaussian integer factors uniquely into Gaussian primes (up to units and order).')
    print()
    print('  This is the first extension of ℤ studied by Gauss (~1832).')
    print('  The methods generalize: ℤ[ω] for ω = e^(2πi/3) (Eisenstein integers) behaves similarly.')
    print('  Other extensions, like ℤ[√-5], lose unique factorization — the start of algebraic K-theory.')
    print()
    print('  The distribution of Gaussian primes is an active research area.')
    print('  Their visual pattern — cross-shaped clusters along circles — is one of the')
    print('  most beautiful things in elementary number theory.')


if __name__ == '__main__':
    main()
