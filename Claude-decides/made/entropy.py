"""
Shannon Entropy

H = -Σ p(x) · log₂(p(x))

Entropy measures uncertainty — or equivalently, information content.
The entropy of a message is the minimum number of bits needed to transmit it.

H = 0 if the outcome is certain (one symbol with probability 1).
H is maximum when all outcomes are equally likely.
For n equally probable outcomes: H = log₂(n) bits.

Intuition via coin flip:
  - Fair coin:       p(H) = p(T) = 0.5       H = 1.0 bit
  - Biased 70/30:    p(H) = 0.7, p(T) = 0.3  H ≈ 0.88 bits
  - Very biased 99/1:                          H ≈ 0.08 bits
  - Certain:         p(H) = 1.0               H = 0 bits

A message with low entropy (biased) carries less surprise.
You need fewer bits to encode it. Less is happening.

Shannon (1948): "My greatest concern was what to call it.
I thought of calling it 'information,' but the word was overly used,
so I decided to call it 'uncertainty.' Von Neumann told me, 'You should
call it entropy, for two reasons. In the first place your uncertainty
function has been used in statistical mechanics under that name. In the
second place, and more important, no one knows what entropy really is,
so in a debate you will always have the advantage.'"

Examples shown:
  - Different probability distributions and their entropies
  - English letter frequencies (high entropy — the language is informationally rich)
  - A highly skewed distribution (low entropy — predictable)
  - How entropy changes as a biased coin varies from 0 to 1
"""

import math

def entropy(probs):
    """Shannon entropy in bits."""
    h = 0.0
    for p in probs:
        if p > 0:
            h -= p * math.log2(p)
    return h


def render_bar(value, max_val, width=50):
    filled = int(value / max_val * width)
    return '█' * filled + '░' * (width - filled)


def main():
    print('Shannon Entropy   H = -Σ p(x)·log₂(p(x))\n')
    print('  Entropy measures uncertainty / information content.')
    print('  Low entropy: predictable. High entropy: surprising.')
    print('  Units: bits. Maximum for n outcomes: log₂(n).\n')

    # ── Biased coin from certain to fair ──────────────────────────────────
    print('  ── Coin bias (how much information per flip?) ──\n')
    print('  p(heads)   entropy')
    for numerator in [0, 1, 2, 5, 7, 9, 10]:
        p = numerator / 10
        q = 1.0 - p
        h = entropy([p, q])
        bar = render_bar(h, 1.0, 40)
        print(f'  {p:.1f}          {h:.4f} bits  {bar}')
    print()
    print('  → Maximum at p=0.5 (fair). Minimum at p=0 or p=1 (certain).\n')

    # ── Classic examples ──────────────────────────────────────────────────
    print('  ── Example distributions ──\n')
    examples = [
        ('Fair die (6 sides)',      [1/6]*6),
        ('Loaded die (6 favors 1)', [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]),
        ('Very loaded (always 1)',  [1.0, 0, 0, 0, 0, 0]),
        ('Fair coin',              [0.5, 0.5]),
        ('99/1 biased coin',       [0.99, 0.01]),
        ('8 equally likely',       [1/8]*8),
        ('DNA base (equal)',        [0.25]*4),
        ('DNA base (biased)',       [0.40, 0.35, 0.15, 0.10]),
    ]

    max_h = max(entropy(p) for _, p in examples)
    for name, probs in examples:
        h = entropy(probs)
        max_possible = math.log2(len(probs))
        bar = render_bar(h, max_h, 40)
        print(f'  {name:<32} H={h:.3f} bits  (max: {max_possible:.3f})')
        print(f'  {bar}\n')

    # ── English letter frequencies ─────────────────────────────────────────
    print('  ── English letter frequencies ──\n')
    # Approximate frequencies (from large corpora)
    freq = {
        'E': 0.1270, 'T': 0.0906, 'A': 0.0817, 'O': 0.0751, 'I': 0.0697,
        'N': 0.0675, 'S': 0.0633, 'H': 0.0609, 'R': 0.0599, 'D': 0.0425,
        'L': 0.0403, 'C': 0.0278, 'U': 0.0276, 'M': 0.0241, 'W': 0.0236,
        'F': 0.0223, 'G': 0.0202, 'Y': 0.0197, 'P': 0.0193, 'B': 0.0149,
        'V': 0.0098, 'K': 0.0077, 'J': 0.0015, 'X': 0.0015, 'Q': 0.0010,
        'Z': 0.0007,
    }
    probs = list(freq.values())
    h_english = entropy(probs)
    h_uniform = math.log2(26)
    print(f'  English letter entropy: {h_english:.4f} bits (vs. {h_uniform:.4f} for uniform)')
    print(f'  Efficiency: {100*h_english/h_uniform:.1f}% — English uses only this fraction of available information\n')

    # Show the distribution
    sorted_freq = sorted(freq.items(), key=lambda x: -x[1])
    print('  Letter frequencies (most → least common):')
    for letter, f in sorted_freq:
        bar_len = int(f * 300)
        info = -math.log2(f)
        print(f'  {letter}  {"█"*bar_len:<38}  p={f:.4f}  info={info:.2f}b')

    print()
    print('  E carries only 3.0 bits of info per occurrence (common = unsurprising).')
    print('  Z carries 10.5 bits per occurrence (rare = surprising).')
    print()
    print('  Shannon (1948): information is surprise.')
    print('  A certain event tells you nothing. A rare event tells you everything.')
    print()
    print('  Entropy is the average surprise — the expected information content.')
    print('  High entropy: the source keeps surprising you. Low entropy: predictable.')
    print()
    print('  This is also why compressed files look like noise:')
    print('  good compression removes redundancy → high entropy output.')
    print('  Maximum compression = maximum entropy = indistinguishable from random.')


if __name__ == '__main__':
    main()
