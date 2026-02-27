"""
Prime Gaps.

The gap between consecutive primes grows, on average, as ln(p).
But the actual gaps are wildly irregular.

Twin primes: pairs with gap=2 (like 11,13 or 17,19 or 41,43).
Nobody has proven there are infinitely many. Almost certainly true.

Prime deserts: long stretches with no primes at all.
The first gap of size 72 or more appears after 31397.
You can always find arbitrarily large prime deserts:
the numbers n!+2, n!+3, ..., n!+n are all composite.
(n!+k is divisible by k for 2 ≤ k ≤ n.)

So there are primes everywhere and also arbitrarily long gaps.
Both things are true.
"""


def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [i for i in range(2, n+1) if is_prime[i]]


if __name__ == '__main__':
    primes = sieve(1000)
    gaps = [(primes[i], primes[i+1], primes[i+1] - primes[i])
            for i in range(len(primes) - 1)]

    max_gap = max(g for _, _, g in gaps)
    bar_width = 50

    print("Prime gaps up to 1000")
    print("Twin primes (gap=2) marked with ★\n")

    for p, q, g in gaps:
        bar = '█' * int((g / max_gap) * bar_width)
        twin = ' ★' if g == 2 else ''
        print(f"{p:>4}→{q:<4} {bar:<{bar_width}} {g}{twin}")

    print(f"\nLargest gap in this range: {max_gap}")

    twins = [(p, q) for p, q, g in gaps if g == 2]
    print(f"Twin prime pairs: {len(twins)}")
    print(f"Last twin pair found: {twins[-1]}")

    # Show gap distribution
    from collections import Counter
    dist = Counter(g for _, _, g in gaps)
    print("\nGap size distribution:")
    for size in sorted(dist):
        count = dist[size]
        bar = '█' * count
        print(f"  gap={size:>3}: {bar} ({count})")
