"""
The Collatz Conjecture.

Take any positive integer.
  If even: divide by 2.
  If odd:  multiply by 3, add 1.
Repeat.

Conjecture: you always eventually reach 1.

This has been checked for every number up to 2^68.
It has never been proven.
Paul Erdős said: "Mathematics is not yet ready for such problems."

This script shows the stopping time (steps to reach 1) for
each integer from 1 to N, rendered as a bar chart.
Watch for 27. It takes 111 steps before reaching 1.
"""

N = 100


def stopping_time(n):
    steps = 0
    while n != 1:
        n = (n * 3 + 1) if n % 2 else n // 2
        steps += 1
    return steps


def collatz_path(n):
    path = [n]
    while n != 1:
        n = (n * 3 + 1) if n % 2 else n // 2
        path.append(n)
    return path


if __name__ == '__main__':
    times = [(i, stopping_time(i)) for i in range(1, N + 1)]
    max_time = max(t for _, t in times)
    bar_width = 60

    print(f"Collatz stopping times, n=1 to {N}")
    print(f"(bar length proportional to steps; max={max_time} steps)\n")

    for n, t in times:
        bar_len = int((t / max_time) * bar_width)
        bar = '█' * bar_len
        # highlight the notorious ones
        flag = ' ←' if t > 80 else ''
        print(f"{n:>3} | {bar:<{bar_width}} {t:>3}{flag}")

    print(f"\nTop 5 slowest (1–{N}):")
    top5 = sorted(times, key=lambda x: -x[1])[:5]
    for n, t in top5:
        path = collatz_path(n)
        peak = max(path)
        print(f"  n={n}: {t} steps, peaks at {peak}")
