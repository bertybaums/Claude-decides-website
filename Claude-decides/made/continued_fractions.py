"""
Continued Fractions — The Deepest Representations of Numbers

Every real number can be written as a continued fraction:
    x = a₀ + 1/(a₁ + 1/(a₂ + 1/(a₃ + ...)))

Written compactly: x = [a₀; a₁, a₂, a₃, ...]

Where:
  - a₀ = floor(x) (the integer part)
  - a₁, a₂, ... are positive integers called "partial quotients"
  - The sequence is finite for rationals, infinite for irrationals

Properties that make this remarkable:
  - Every rational number has a finite continued fraction
  - Every irrational has an infinite one
  - Periodic continued fractions correspond exactly to quadratic irrationals
    (numbers of the form (a + b√c) / d)
  - The convergents p_n/q_n (truncations) are the BEST rational approximations
    to x with denominator ≤ q_n
  - √2 = [1; 2, 2, 2, 2, ...] (periodic)
  - φ = [1; 1, 1, 1, 1, ...] (all 1s — the "most irrational" number)
  - e = [2; 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, ...] (pattern!)
  - π = [3; 7, 15, 1, 292, 1, 1, 1, ...] (irregular — deep mystery)

The convergents to π are famous:
  3, 22/7, 333/106, 355/113 (Milü — correct to 6 decimal places!)
  355/113 was known to Zu Chongzhi in 5th century China.
"""

import math
from fractions import Fraction


def to_continued_fraction(x, max_terms=20, tolerance=1e-10):
    """Compute the continued fraction expansion of x."""
    cf = []
    for _ in range(max_terms):
        a = int(x)
        cf.append(a)
        frac = x - a
        if abs(frac) < tolerance:
            break
        x = 1.0 / frac
    return cf


def convergents(cf):
    """Compute the convergents p_n/q_n from a continued fraction."""
    convs = []
    p_prev, p_curr = 1, cf[0]
    q_prev, q_curr = 0, 1
    convs.append(Fraction(p_curr, q_curr))
    for a in cf[1:]:
        p_next = a * p_curr + p_prev
        q_next = a * q_curr + q_prev
        p_prev, p_curr = p_curr, p_next
        q_prev, q_curr = q_curr, q_next
        convs.append(Fraction(p_curr, q_curr))
    return convs


def stern_brocot_level(p, q, max_depth=8):
    """Find level in Stern-Brocot tree where p/q appears."""
    lo_p, lo_q = 0, 1
    hi_p, hi_q = 1, 0
    depth = 0
    while depth < max_depth:
        med_p = lo_p + hi_p
        med_q = lo_q + hi_q
        if med_p == p and med_q == q:
            return depth
        elif p * med_q < q * med_p:
            hi_p, hi_q = med_p, med_q
        else:
            lo_p, lo_q = med_p, med_q
        depth += 1
    return depth


def quality_of_approximation(x, p, q):
    """How good is p/q as an approximation to x? Return |x - p/q| * q^2."""
    return abs(x - p / q) * q * q


def format_cf(cf, n_show=12):
    """Format a continued fraction nicely."""
    terms = cf[:n_show]
    suffix = '...' if len(cf) > n_show else ''
    if not terms:
        return '[]'
    return '[' + str(terms[0]) + '; ' + ', '.join(str(a) for a in terms[1:]) + suffix + ']'


def bar_chart(values, labels, width=40, title=''):
    """Simple horizontal bar chart."""
    if title:
        print(f'  {title}')
    maxv = max(values) if values else 1
    for v, label in zip(values, labels):
        bar_len = int(v / maxv * width)
        bar = '█' * bar_len + '░' * (width - bar_len)
        print(f'  {label:>12}  {bar}  {v:.2e}')


def main():
    print('Continued Fractions — The Deepest Representations of Numbers\n')

    # Famous irrationals
    numbers = [
        (math.sqrt(2),     '√2'),
        (math.sqrt(3),     '√3'),
        (math.sqrt(5),     '√5'),
        ((1+math.sqrt(5))/2, 'φ (golden ratio)'),
        (math.pi,          'π'),
        (math.e,           'e'),
    ]

    print('  CONTINUED FRACTION EXPANSIONS')
    print('  ' + '─' * 72)
    for x, name in numbers:
        cf = to_continued_fraction(x, max_terms=15)
        print(f'  {name:>16}  =  {format_cf(cf, 12)}')

    print()
    print('  Note: φ = [1; 1, 1, 1, ...] — all partial quotients = 1')
    print('        This makes it the hardest number to approximate rationally.')
    print('        e has the pattern [2; 1, 2, 1, 1, 4, 1, 1, 6, ...]')
    print('        π has no visible pattern — deep unsolved mystery.')

    # Convergents to π
    print()
    print('  CONVERGENTS TO π (best rational approximations)')
    print('  ' + '─' * 72)
    cf_pi = to_continued_fraction(math.pi, max_terms=10)
    convs_pi = convergents(cf_pi)
    print(f'  {"Fraction":>15}  {"Decimal":>14}  {"Error":>12}  {"Error × q²":>12}')
    for c in convs_pi[:9]:
        p, q = c.numerator, c.denominator
        val = float(c)
        err = abs(val - math.pi)
        quality = quality_of_approximation(math.pi, p, q)
        print(f'  {str(c):>15}  {val:>14.10f}  {err:>12.2e}  {quality:>12.4f}')
    print()
    print('  355/113 = 3.1415929... error = 2.7×10⁻⁷, correct to 6 decimal places')
    print('  Known to Zu Chongzhi (5th century China). Europe rediscovered it in 1585.')

    # Quality of approximation: φ vs. other numbers
    print()
    print('  THE GOLDEN RATIO IS THE HARDEST NUMBER TO APPROXIMATE')
    print('  Quality measure: |x - p/q| × q² (lower = better approximation)')
    print('  For well-approximable numbers, this is small.')
    print()

    cf_phi = to_continued_fraction((1 + math.sqrt(5)) / 2, max_terms=10)
    cf_sqrt2 = to_continued_fraction(math.sqrt(2), max_terms=10)
    convs_phi = convergents(cf_phi)
    convs_sqrt2 = convergents(cf_sqrt2)

    phi_val = (1 + math.sqrt(5)) / 2
    sqrt2_val = math.sqrt(2)

    print(f'  {"n":>3}  {"Conv to φ":>10}  {"Quality φ":>12}  {"Conv to √2":>12}  {"Quality √2":>12}')
    for i in range(min(8, len(convs_phi), len(convs_sqrt2))):
        cp = convs_phi[i]; c2 = convs_sqrt2[i]
        qp = quality_of_approximation(phi_val, cp.numerator, cp.denominator)
        q2 = quality_of_approximation(sqrt2_val, c2.numerator, c2.denominator)
        print(f'  {i:>3}  {str(cp):>10}  {qp:>12.4f}  {str(c2):>12}  {q2:>12.4f}')

    print()
    print("  phi's quality measures cluster near 1/sqrt(5) ~= 0.447 — never getting small.")
    print("  sqrt(2)'s measures are smaller: its continued fraction [1;2,2,2,...] has")
    print('  larger partial quotients, allowing better approximations.')
    print()

    # Visual: the Farey sequence and where convergents live
    print('  CONTINUED FRACTIONS AND THE FAREY SEQUENCE')
    print()
    print('  Convergents to φ: 1/1, 2/1, 3/2, 5/3, 8/5, 13/8, 21/13, ...')
    print('  These are consecutive Fibonacci ratios — converging to φ from above/below.')
    print()

    # Show Fibonacci convergence visually
    WIDTH_VIZ = 60
    phi_true = phi_val
    fibs = [1, 1]
    while fibs[-1] < 1000:
        fibs.append(fibs[-1] + fibs[-2])

    print('  Fibonacci convergence to φ:')
    print()
    for i in range(2, min(14, len(fibs))):
        ratio = fibs[i] / fibs[i-1]
        err = ratio - phi_true
        pos = int((ratio - 1.6) / 0.04 * WIDTH_VIZ)
        pos = max(0, min(WIDTH_VIZ - 1, pos))
        marker_line = ' ' * pos + '▲'
        sign = '+' if err >= 0 else '-'
        print(f'  F({i:2d})/F({i-1:2d}) = {fibs[i]:4d}/{fibs[i-1]:4d} = {ratio:.8f}  ({sign}{abs(err):.2e})')

    print()
    print(f'  φ = {phi_true:.10f}...')
    print()
    print('  The convergents alternate above and below φ.')
    print('  Each is the BEST approximation with that denominator.')
    print('  No fraction with smaller denominator gets closer.')


if __name__ == '__main__':
    main()
