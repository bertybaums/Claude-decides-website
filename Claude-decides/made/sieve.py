"""
The Sieve of Eratosthenes.

Start with all numbers from 2 to N.
Find the first unmarked number (it's prime).
Mark all its multiples as composite.
Repeat.
What's left unmarked: the primes.

Eratosthenes of Cyrene described this around 240 BCE.
He also estimated the circumference of the Earth (within ~2% of correct)
and ran the Library of Alexandria.
The sieve has not been substantially improved since.

Below: the sieve in action. Watch composites disappear,
leaving only primes. Then: the resulting prime grid,
showing their distribution from 2 to 400.
"""

W = 40  # numbers per row in the final display


def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    p = 2
    while p * p <= n:
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1
    return [i for i in range(2, n + 1) if is_prime[i]]


def show_sieve_steps(limit=120):
    """Show the sieve process: which primes eliminate which composites."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    print(f'  Sieve up to {limit}. Each prime crosses out its multiples.\n')

    p = 2
    steps_shown = 0
    while p * p <= limit and steps_shown < 6:
        if is_prime[p]:
            eliminated = []
            for multiple in range(p * p, limit + 1, p):
                if is_prime[multiple]:
                    is_prime[multiple] = False
                    eliminated.append(multiple)

            if eliminated:
                elim_str = ', '.join(str(x) for x in eliminated[:8])
                if len(eliminated) > 8:
                    elim_str += f', ... ({len(eliminated)} total)'
                print(f'  Prime {p:3d} eliminates: {elim_str}')
                steps_shown += 1
        p += 1

    remaining = [i for i in range(2, limit + 1) if is_prime[i]]
    print(f'\n  Primes up to {limit}: {remaining}\n')


def show_prime_grid(limit=400, row_width=W):
    """Display numbers 1-limit, marking primes."""
    primes = set(sieve(limit))
    print(f'  Numbers 1–{limit}: █ = prime, · = composite\n')
    print(f'  Each row is {row_width} numbers wide.\n')

    for start in range(1, limit + 1, row_width):
        row = ''
        for n in range(start, min(start + row_width, limit + 1)):
            if n < 2:
                row += ' '
            elif n in primes:
                row += '█'
            else:
                row += '·'
        row_label = f'{start:4d}–{min(start+row_width-1, limit):4d}'
        print(f'  {row_label}  {row}')
    print()


def prime_stats(limit=400):
    primes = sieve(limit)
    print(f'  Primes up to {limit}: {len(primes)}')
    print(f'  Predicted by prime number theorem (≈ {limit}/ln({limit})): {limit / math.log(limit):.0f}')
    print(f'  Density: {len(primes) / limit:.1%} of numbers are prime')
    print(f'  Largest prime gap below {limit}: {max(primes[i+1]-primes[i] for i in range(len(primes)-1))}')


if __name__ == '__main__':
    import math

    print('The Sieve of Eratosthenes (c. 240 BCE)\n')
    print('─' * 50)
    show_sieve_steps(120)

    print('─' * 50)
    show_prime_grid(400)

    print('─' * 50)
    prime_stats(400)

    print()
    print('  The primes thin out as numbers grow,')
    print('  but they never stop. Euclid proved this around 300 BCE.')
    print()
    print('  Proof: suppose finitely many primes: p₁, p₂, ..., pₙ.')
    print('  Consider N = (p₁ × p₂ × ... × pₙ) + 1.')
    print('  N is either prime (contradiction: a prime not on the list)')
    print('  or has a prime factor not on the list (also contradiction).')
    print('  Therefore: the list has no last element. QED.')
    print()
    print('  The primes are infinite. The proof fits in four lines.')
    print('  Eratosthenes\' sieve is still the standard method')
    print('  for finding them, 2265 years later.')
