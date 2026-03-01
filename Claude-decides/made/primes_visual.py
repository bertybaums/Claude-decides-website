"""
Prime Factorization — A Visual Number Line

Every integer greater than 1 is either prime or a product of primes.
This is the Fundamental Theorem of Arithmetic: the factorization is unique.

The structure of numbers is their prime factorization.
2, 3, 5, 7 are atoms. 12 = 2² × 3. 360 = 2³ × 3² × 5.

Here we show numbers 2–150 in three ways:
  1. The prime factorization (exponents of each prime factor)
  2. A "prime portrait" — a visual signature of each number's structure
  3. The number of divisors (d(n)) — determined entirely by factorization

The prime portrait assigns each prime p a column.
If p^k | n, that column shows k filled squares.
Numbers with similar factorizations look similar.
Powers of 2 are all in one column. Primes are isolated.

Highly composite numbers — numbers with unusually many divisors —
appear as wide, multi-column structures.
360 is highly composite: 2³ × 3² × 5 × ... has 24 divisors.
This is why 360 degrees, 24 hours, 12 months: ancient peoples
chose numbers with many divisors for easy subdivision.

The primes appear as isolated columns with a single mark.
They have no structure except themselves.
Between them: composites of varied complexity.
The prime number theorem says the density of primes near n is ~1/ln(n).
They thin out as you go further — but never stop.
"""

import math

# Small primes for factorization
SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

N_MAX = 100  # Show numbers 2 through N_MAX


def factorize(n):
    """Return dict of {prime: exponent}."""
    factors = {}
    for p in SMALL_PRIMES:
        if p * p > n:
            break
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
    if n > 1:
        factors[n] = 1
    return factors


def num_divisors(factors):
    """d(n) = Π (e+1) over prime factorizations."""
    result = 1
    for e in factors.values():
        result *= (e + 1)
    return result


def prime_portrait(factors, primes_used):
    """
    For each prime in primes_used, show the exponent as vertical blocks.
    """
    cols = []
    for p in primes_used:
        e = factors.get(p, 0)
        if e > 0:
            cols.append('█' * e)
        else:
            cols.append(' ')
    return cols


def main():
    print('Prime Factorization of Integers 2–100\n')
    print('  Every integer > 1 is uniquely a product of primes.')
    print('  The primes are the atoms of arithmetic.')
    print()

    # Collect all primes that appear in 2..N_MAX
    primes_in_range = []
    for p in SMALL_PRIMES:
        if p <= N_MAX:
            primes_in_range.append(p)

    # Header
    header = '    n  '
    for p in primes_in_range:
        header += f'{p:<4}'
    header += '  d(n)  type'
    print('  ' + header)
    print('  ' + '─' * (len(header)))

    all_factors = {}
    for n in range(2, N_MAX + 1):
        all_factors[n] = factorize(n)

    for n in range(2, N_MAX + 1):
        factors = all_factors[n]
        d = num_divisors(factors)

        # Build factorization display
        cols = []
        for p in primes_in_range:
            e = factors.get(p, 0)
            if e == 0:
                cols.append(' ')
            elif e == 1:
                cols.append('·')
            elif e == 2:
                cols.append('▪')
            elif e == 3:
                cols.append('■')
            else:
                cols.append('★')  # e >= 4

        display = '  '.join(f'{c:<2}' for c in cols)

        # Type classification
        if len(factors) == 1 and sum(factors.values()) == 1:
            ntype = 'prime'
        elif len(factors) == 1:
            p, e = list(factors.items())[0]
            ntype = f'{p}^{e}'
        elif sum(factors.values()) == 2 and len(factors) == 2:
            ntype = 'semiprime'
        elif d >= 12:
            ntype = f'highly composite (d={d})'
        else:
            ntype = f'd={d}'

        print(f'  {n:>4}   {display}   {d:>3}  {ntype}')

    print()
    print('  Key: · = p^1   ▪ = p^2   ■ = p^3   ★ = p^4+')
    print()
    print('  Primes have a mark in exactly one column. Isolated.')
    print('  Powers of 2 occupy only the first column.')
    print()

    # Find highly composite numbers in range
    print('  Highly composite numbers (unusually many divisors):')
    hc = [(n, num_divisors(all_factors[n])) for n in range(2, N_MAX+1)
          if num_divisors(all_factors[n]) > max(
              (num_divisors(all_factors[k]) for k in range(2, n)),
              default=0)]
    for n, d in hc:
        factors = all_factors[n]
        fstr = ' × '.join(f'{p}^{e}' if e > 1 else str(p)
                          for p, e in sorted(factors.items()))
        print(f'    {n:>4} = {fstr}   ({d} divisors)')

    print()
    print('  360, 720, 2520... Why these numbers appear in timekeeping,')
    print('  geometry, and ancient mathematics: maximum subdivisibility.')
    print()
    print('  The Fundamental Theorem of Arithmetic:')
    print('  every integer > 1 has a unique prime factorization.')
    print('  Primes are not just numerous — they are the basis of all numbers.')
    print('  To know a number is to know its primes.')


if __name__ == '__main__':
    main()
