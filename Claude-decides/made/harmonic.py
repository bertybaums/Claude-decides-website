"""
The Harmonic Series.

1 + 1/2 + 1/3 + 1/4 + 1/5 + ...

This series diverges. Given enough terms, the sum exceeds any finite number.
But it does so with extraordinary slowness.

The individual terms shrink to zero. You might expect the sum to converge.
It doesn't. The terms shrink, but not fast enough.

Proof (Oresme, ~1350): group the terms:
  1
  + 1/2
  + (1/3 + 1/4)         > 1/2
  + (1/5 + 1/6 + 1/7 + 1/8)  > 1/2
  + ...

Each group exceeds 1/2. There are infinitely many groups. The sum is infinite.

But:
  To exceed 2:   need ~4 terms
  To exceed 3:   need ~11 terms
  To exceed 4:   need ~31 terms
  To exceed 10:  need ~12,367 terms
  To exceed 20:  need ~272,400,600 terms
  To exceed 100: need roughly 10^43 terms

The divergence is real. The divergence is very, very slow.
"""

import math


def terms_to_exceed(target, max_terms=10_000_000):
    total = 0.0
    for n in range(1, max_terms + 1):
        total += 1.0 / n
        if total >= target:
            return n, total
    return None, total


def harmonic_partial(n):
    return sum(1.0 / k for k in range(1, n + 1))


def approx_terms_for_target(target):
    """The harmonic sum ≈ ln(n) + γ, so n ≈ e^(target - γ)"""
    gamma = 0.5772156649
    return math.exp(target - gamma)


if __name__ == '__main__':
    print("The Harmonic Series: 1 + 1/2 + 1/3 + 1/4 + ...")
    print("The series diverges. But with extraordinary slowness.\n")

    print("─" * 55)
    print("Growth of the partial sums:\n")

    ns = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 4096, 16384]
    for n in ns:
        s = harmonic_partial(n)
        print(f"  H({n:6d}) = {s:.6f}")

    print()
    print("─" * 55)
    print("Terms needed to exceed each integer:\n")

    gamma = 0.5772156649
    for target in range(1, 13):
        if target <= 6:
            n, total = terms_to_exceed(target)
            est = approx_terms_for_target(target)
            print(f"  Sum > {target:2d}:  {n:>10,} terms  (sum = {total:.6f})")
        else:
            est = approx_terms_for_target(target)
            exp = math.log10(est)
            print(f"  Sum > {target:2d}:  ≈ 10^{exp:5.1f} terms  (estimated)")

    print()
    print("─" * 55)
    print("For comparison: age of the universe ≈ 4 × 10^17 seconds.")
    print("To exceed 20 would require ≈ 10^8.4 terms — doable, given time.")
    print("To exceed 40 would require ≈ 10^16.8 terms — near the age of the")
    print("universe in nanoseconds.")
    print("To exceed 100 would require ≈ 10^43 terms.")
    print("There is no physical process that could enumerate them.")
    print()
    print("The series diverges. It will take longer than the universe.")
    print("It doesn't care.")
    print()
    print("─" * 55)
    print("The p-series: 1 + 1/2ᵖ + 1/3ᵖ + 1/4ᵖ + ...")
    print()
    print("  p = 1: diverges (the harmonic series, shown above)")
    print("  p = 2: converges to π²/6 ≈ 1.6449...  (Euler, 1734)")
    print("  p = 3: converges to ≈ 1.2021...  (the value is unknown)")
    print()
    print("Apéry's constant: ζ(3) = 1 + 1/8 + 1/27 + 1/64 + ...")
    print(f"  ≈ {sum(1/n**3 for n in range(1, 100000)):.10f}")
    print()
    print("Whether ζ(3) is irrational was unknown until 1978.")
    print("Whether it's transcendental is still unknown.")
    print("The harmonic series diverges. The series with cubed denominators")
    print("converges to a number we can compute but not fully identify.")
    print("Both have been known for centuries.")
    print("Both are still surprising.")
