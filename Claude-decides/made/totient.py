"""
Euler's Totient Function φ(n) — The Arithmetic of Irreducibility

φ(n) counts the positive integers ≤ n that are coprime to n
(share no common factor > 1).

Examples:
  φ(1) = 1     (1 is coprime to 1, trivially)
  φ(6) = 2     (1 and 5 are coprime to 6; 2,3,4 are not)
  φ(7) = 6     (all 1-6 are coprime to 7, because 7 is prime)
  φ(12) = 4    (1, 5, 7, 11 are coprime to 12)

For a prime p: φ(p) = p - 1
For prime power: φ(pⁿ) = pⁿ - pⁿ⁻¹ = pⁿ(1 - 1/p)
For coprime m, n: φ(mn) = φ(m)·φ(n)  [multiplicativity!]

General formula: φ(n) = n · ∏_{p|n} (1 - 1/p)

This formula says: to count numbers coprime to n, start with n,
and for each prime factor p of n, multiply by (1 - 1/p).
Each prime factor "knocks out" a fraction of the candidates.

Role in number theory:
  - Euler's theorem: a^φ(n) ≡ 1 (mod n) when gcd(a,n) = 1
  - Fermat's little theorem is the special case n = prime
  - RSA encryption: key generation uses φ(pq) = (p-1)(q-1)
  - The multiplicative group mod n has order φ(n)

The totient function is:
  - Multiplicative (but not completely multiplicative)
  - φ(n)/n = ∏ (1 - 1/p) — the "density" of coprimes
  - Highly composite numbers have unusually small φ(n)/n
  - Primes have φ(p)/p = 1 - 1/p → 1 as p → ∞

Sum formula: Σ_{d|n} φ(d) = n  (sum over divisors)
This is one of the beautiful identities in number theory.
"""

import math
from collections import defaultdict


def prime_factors(n):
    """Return set of prime factors of n."""
    factors = set()
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


def totient(n):
    """Compute Euler's totient φ(n)."""
    result = n
    for p in prime_factors(n):
        result -= result // p
    return result


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def visualize_coprimes(n, width=60):
    """Show which numbers are coprime to n."""
    coprimes = [k for k in range(1, n + 1) if gcd(k, n) == 1]
    print(f'  Coprimes to {n}: {coprimes}')
    print(f'  φ({n}) = {len(coprimes)}  (out of {n} numbers)')

    # Grid visualization
    cols = min(n, width)
    row = ''
    for k in range(1, n + 1):
        row += '█' if gcd(k, n) == 1 else '·'
    print(f'  [1..{n}]:  {row}')


def bar_totient(n_max=100, bar_width=40):
    """Bar chart of φ(n) vs n."""
    tots = [(n, totient(n)) for n in range(1, n_max + 1)]

    print(f'  φ(n) for n = 1 to {n_max}')
    print(f'  Full bar = n-1 (prime)')
    print()

    CHARS = '░▒▓█'
    for n, phi in tots:
        ratio = phi / (n - 1) if n > 1 else 1.0
        bar_len = int(ratio * bar_width)
        bar = '█' * bar_len + '░' * (bar_width - bar_len)

        is_prime = (phi == n - 1 and n > 1)
        marker = 'P' if is_prime else ' '
        print(f'  {n:>4}  φ={phi:>4}  {marker} {bar}  {phi/n:.3f}')


def totient_sum_identity(n):
    """Verify Σ_{d|n} φ(d) = n."""
    divisors = [d for d in range(1, n + 1) if n % d == 0]
    total = sum(totient(d) for d in divisors)
    return divisors, total


def main():
    print('Euler\'s Totient Function φ(n)\n')
    print('  φ(n) = count of numbers in [1..n] coprime to n\n')

    # Show small examples
    print('  ─── EXAMPLES ───')
    for n in [1, 4, 6, 7, 8, 9, 10, 12, 15, 16, 30]:
        phi = totient(n)
        pf = prime_factors(n)
        formula = ' × '.join(f'(1-1/{p})' for p in sorted(pf))
        formula_str = f'{n} × {formula} = {phi}' if formula else f'{phi}'
        print(f'  φ({n:>3}) = {phi:>4}    factors: {sorted(pf)}')
    print()

    # Visualize coprimes for specific n
    print('  ─── COPRIME PATTERNS ───')
    for n in [12, 30]:
        visualize_coprimes(n)
        print()

    # Sum identity
    print('  ─── BEAUTIFUL IDENTITY: Σ_{d|n} φ(d) = n ───')
    for n in [12, 30, 60]:
        divs, total = totient_sum_identity(n)
        contributions = [(d, totient(d)) for d in divs]
        print(f'  n = {n}:  divisors × φ = {contributions}')
        print(f'        sum = {total} = n ✓' if total == n else f'        sum = {total} ≠ n (!)')
        print()

    # The totient density φ(n)/n
    print('  ─── DENSITY φ(n)/n ───')
    print('  For primes p: φ(p)/p = (p-1)/p → 1')
    print('  For highly composite numbers (many small prime factors): small')
    print()
    print(f'  {"n":>6}  {"φ(n)":>6}  {"density":>8}  {"factors"}')
    notable = [2, 3, 4, 6, 8, 12, 24, 30, 60, 120, 210, 2310]
    for n in notable:
        phi = totient(n)
        density = phi / n
        pf = sorted(prime_factors(n))
        print(f'  {n:>6}  {phi:>6}  {density:>8.4f}  {pf}')

    print()
    print('  2310 = 2×3×5×7×11: the first 5 primes give density 0.2079')
    print('  As more primes are included, density → 0 (product formula)')
    print()

    # The bar chart (abbreviated)
    print('  ─── φ(n) vs n, n = 1..40 ───')
    print()
    n_max = 40
    bar_width = 30
    for n in range(1, n_max + 1):
        phi = totient(n)
        ratio = phi / n
        bar_len = int(ratio * bar_width)
        bar = '█' * bar_len + '·' * (bar_width - bar_len)
        is_prime = (phi == n - 1 and n > 1)
        marker = '← prime' if is_prime else ''
        print(f'  {n:>3}  {bar}  {phi:>3}/{n:<3}  {marker}')

    print()
    print('  Primes: bar reaches nearly full width (φ(p) = p-1).')
    print('  Powers of 2: bar halves each time (φ(2ⁿ) = 2ⁿ⁻¹).')
    print('  Highly composite: bars are short.')
    print()
    print('  The gaps in the bars are the non-coprime numbers.')
    print('  These are exactly the numbers sharing a factor with n.')
    print()
    print('  RSA: to encrypt with modulus n=pq, we need φ(n)=(p-1)(q-1).')
    print('  Knowing n but not p,q makes computing φ(n) as hard as factoring n.')
    print('  The security of RSA rests on this gap between structure and computation.')


if __name__ == '__main__':
    main()
