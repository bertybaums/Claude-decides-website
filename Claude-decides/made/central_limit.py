"""
The Central Limit Theorem.

Take any distribution — uniform, exponential, bimodal, lopsided,
as weird as you like. Sample from it repeatedly. Average the samples.
As the sample size grows, the distribution of averages approaches
the normal distribution (bell curve), regardless of the original shape.

This is extraordinary. The source distribution can be grotesque.
The averages will be bell-shaped. Every time.

The normal distribution emerges from averaging. Since almost everything
we measure is an average of many smaller influences, the normal
distribution shows up everywhere: heights, measurement errors, test scores,
the position of a particle in Brownian motion.

It's not that the world is normally distributed. It's that sums of
independent things tend to be, and much of what we measure is a sum.

Below: four different source distributions, each averaged many times,
all converging to the same bell curve.
"""

import random
import math


def sample_uniform():
    return random.random()


def sample_exponential(rate=1.0):
    return -math.log(1 - random.random()) / rate


def sample_bimodal():
    if random.random() < 0.5:
        return random.gauss(0.2, 0.05)
    return random.gauss(0.8, 0.05)


def sample_bernoulli(p=0.1):
    return 1.0 if random.random() < p else 0.0


def average_of(sample_fn, n):
    return sum(sample_fn() for _ in range(n)) / n


def histogram(values, bins=60, width=70, label=''):
    lo, hi = min(values), max(values)
    if lo == hi:
        return
    bin_size = (hi - lo) / bins
    counts = [0] * bins
    for v in values:
        idx = min(int((v - lo) / bin_size), bins - 1)
        counts[idx] += 1
    max_count = max(counts)
    if label:
        print(f'  {label}')
    for i, c in enumerate(counts):
        bar_len = int(c / max_count * width)
        print('  ' + '█' * bar_len)
    print()


def multi_histogram(values, bins=60, width=72):
    """Show histogram with bin markers."""
    lo, hi = min(values), max(values)
    bin_size = (hi - lo) / bins
    counts = [0] * bins
    for v in values:
        idx = min(int((v - lo) / bin_size), bins - 1)
        counts[idx] += 1
    max_count = max(counts)
    rows = 14
    lines = []
    for row in range(rows, 0, -1):
        threshold = row / rows * max_count
        line = ''
        for c in counts:
            line += '█' if c >= threshold else ' '
        lines.append('  |' + line)
    lines.append('  +' + '─' * bins)
    return lines


if __name__ == '__main__':
    random.seed(42)
    N_SAMPLES = 8000

    distributions = [
        ('Uniform [0,1]',         sample_uniform,              'flat — no preference for any value'),
        ('Exponential',           sample_exponential,          'skewed — most values near 0, long tail right'),
        ('Bimodal (two peaks)',   sample_bimodal,              'two humps at 0.2 and 0.8'),
        ('Bernoulli (p=0.1)',     sample_bernoulli,            '90% zeros, 10% ones — extremely skewed'),
    ]

    sample_sizes = [1, 2, 5, 30]

    print('The Central Limit Theorem')
    print('Each distribution, averaged over increasing sample sizes.\n')
    print('Watch the bell curve emerge regardless of the original shape.\n')

    for name, fn, description in distributions:
        print('═' * 65)
        print(f'  Source: {name}')
        print(f'  ({description})\n')

        for n in sample_sizes:
            averages = [average_of(fn, n) for _ in range(N_SAMPLES)]
            label = f'n={n:2d}  — average of {n} sample{"s" if n > 1 else ""}'
            lines = multi_histogram(averages)
            print(f'  {label}')
            for line in lines:
                print(line)

    print('═' * 65)
    print()
    print('In each case: n=1 shows the original shape.')
    print('By n=30, every distribution has become a bell curve.')
    print()
    print('The theorem does not say the original distribution changes.')
    print('It says: averages of random things are normally distributed,')
    print('no matter where they came from.')
    print()
    print('The bell curve is not a property of data. It is a property of averaging.')
