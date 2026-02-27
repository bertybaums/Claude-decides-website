"""
The Golden Ratio — φ (phi).

φ = (1 + √5) / 2 ≈ 1.6180339887...

The "most irrational" number. The number hardest to approximate by rationals.
The continued fraction of every number is eventually periodic (for square roots)
or terminates (for rationals). The continued fraction for φ is:

  φ = 1 + 1/(1 + 1/(1 + 1/(1 + ...)))  — all 1s, forever.

All 1s is the worst case for approximation: no term is large enough to "jump"
you close to the target. This makes φ the number furthest from all rationals
in a precise sense. This is why it appears in nature: growth processes that use
the golden angle (360° × (1 - 1/φ) ≈ 137.5°) pack seeds most densely, because
adjacent seeds are as non-aligned as possible, avoiding the regular gaps that
simpler angles would create.

φ satisfies: φ² = φ + 1   (i.e., 1/φ = φ - 1)
The Fibonacci sequence converges to φ: F(n+1)/F(n) → φ as n → ∞.
"""

import math

PHI = (1 + math.sqrt(5)) / 2


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def continued_fraction_convergents(n_terms):
    """Convergents of the continued fraction [1; 1, 1, 1, ...] = φ."""
    p_prev, p_curr = 1, 1
    q_prev, q_curr = 0, 1
    convergents = [(p_curr, q_curr)]
    for _ in range(n_terms - 1):
        p_prev, p_curr = p_curr, p_curr + p_prev
        q_prev, q_curr = q_curr, q_curr + q_prev
        convergents.append((p_curr, q_curr))
    return convergents


def show_bar(value, width=50, label=''):
    filled = int(value / PHI * width)
    filled = min(filled, width)
    bar = '█' * filled + '·' * (width - filled)
    suffix = f'  {label}' if label else ''
    print(f'  |{bar}|{suffix}')


if __name__ == '__main__':
    print('The Golden Ratio — φ')
    print(f'φ = (1 + √5) / 2 = {PHI:.15f}...\n')

    print('─' * 60)
    print('Properties of φ:\n')
    print(f'  φ       = {PHI:.10f}')
    print(f'  φ²      = {PHI**2:.10f}  (should equal φ + 1 = {PHI+1:.10f})')
    print(f'  1/φ     = {1/PHI:.10f}  (should equal φ - 1 = {PHI-1:.10f})')
    print(f'  φ - 1/φ = {PHI - 1/PHI:.10f}  (should equal 1)')
    print()
    print(f'  φ is the only positive number equal to its own reciprocal plus 1.')
    print(f'  It is the positive solution to x² - x - 1 = 0.')

    print()
    print('─' * 60)
    print('Fibonacci convergents — F(n+1)/F(n) → φ:\n')

    print(f'  {"n":>4}  {"F(n)":>12}  {"F(n+1)":>12}  {"ratio":>14}  {"error":>12}')
    print('  ' + '─' * 58)
    for n in range(1, 20):
        fn = fibonacci(n)
        fn1 = fibonacci(n + 1)
        ratio = fn1 / fn if fn > 0 else 0
        error = abs(ratio - PHI)
        print(f'  {n:>4}  {fn:>12,}  {fn1:>12,}  {ratio:>14.10f}  {error:>12.2e}')

    print()
    print('─' * 60)
    print('Continued fraction convergents [1; 1, 1, 1, ...] — same sequence:\n')

    convergents = continued_fraction_convergents(15)
    print(f'  {"k":>4}  {"p":>8}  {"q":>8}  {"p/q":>14}  {"error":>12}')
    print('  ' + '─' * 52)
    for k, (p, q) in enumerate(convergents, 1):
        ratio = p / q
        error = abs(ratio - PHI)
        print(f'  {k:>4}  {p:>8}  {q:>8}  {ratio:>14.10f}  {error:>12.2e}')
    print()
    print('  p/q values are exactly the Fibonacci ratios.')
    print('  The continued fraction IS the Fibonacci sequence.')

    print()
    print('─' * 60)
    print('How well can rationals approximate φ?\n')
    print('  For any irrational α, there are infinitely many p/q with |α - p/q| < 1/q².')
    print('  But for φ, there are no rationals with |φ - p/q| < 1/(√5 · q²).')
    print(f'  √5 ≈ {math.sqrt(5):.6f}')
    print()
    print('  All 1s in the continued fraction = worst case for rational approximation.')
    print('  φ is the number furthest from all fractions in this precise sense.')
    print('  This is why it appears in phyllotaxis:')
    print('  the golden angle creates the most irrational spacing between seeds.')

    print()
    print('─' * 60)
    print('Golden angle = 360° × (1 - 1/φ) = 360°/φ²:\n')
    golden_angle = 360 * (1 - 1 / PHI)
    print(f'  {golden_angle:.6f}°  ≈ 137.508°')
    print()
    print('  After n seeds placed at 137.508° apart, no two are ever aligned.')
    print('  Any simpler fraction of 360° would create spokes and gaps.')
    print('  The golden angle creates the densest packing — no pattern, no waste.')
