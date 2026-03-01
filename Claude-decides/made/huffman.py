"""
Huffman Coding — The Optimal Prefix-Free Code

Given a set of symbols with known probabilities, Huffman coding
constructs the shortest possible binary code (on average).

No codeword is a prefix of another — you can decode without separators.
This is the prefix-free property.

Key theorem (Shannon, 1948):
  The average length of a Huffman code for source with entropy H
  satisfies: H ≤ L < H + 1
  where H = -Σ p(x) log₂ p(x) is the Shannon entropy in bits.

  Huffman coding is optimal among prefix-free codes.
  It achieves the entropy lower bound to within 1 bit per symbol.

How it works:
  1. Build a min-heap of (probability, symbol)
  2. Repeatedly merge the two smallest: new node = their sum
  3. The tree structure encodes: left branch = 0, right branch = 1
  4. Leaf depth = codeword length

English letter frequencies from large corpora:
  'e' is most frequent (~12.7%) → shortest code
  'z', 'q' are rarest (~0.07%) → longest code
  The distribution is highly unequal → Huffman saves ~20% over ASCII

Connection to entropy:
  If you flip a fair coin 8 times, all outcomes equally likely.
  Entropy = 8 bits = 8 bits needed per symbol.
  But if outcomes are unequal (like letters), Huffman does better.
  The savings directly reflect the redundancy in the source.

Historical context:
  David Huffman developed this in 1952 as a course assignment.
  He was 25 years old, taking an information theory course from Fano.
  Fano had been trying to solve this problem himself.
  Huffman's insight (build from the bottom up, not top down) was the key.
  He submitted it instead of taking the final exam.
"""

import heapq
from collections import Counter


# English letter frequencies (approximate, per Wikipedia / large corpora)
ENGLISH_FREQ = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
    'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
    'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
    'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
    'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974,
    'z': 0.074
}


class HuffmanNode:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def is_leaf(self):
        return self.left is None and self.right is None


def build_huffman_tree(frequencies):
    """Build Huffman tree from {symbol: frequency} dict."""
    heap = [HuffmanNode(freq, sym) for sym, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = HuffmanNode(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, parent)

    return heap[0] if heap else None


def get_codes(node, prefix='', codes=None):
    """Recursively extract {symbol: code} from tree."""
    if codes is None:
        codes = {}
    if node is None:
        return codes
    if node.is_leaf():
        codes[node.symbol] = prefix if prefix else '0'
        return codes
    get_codes(node.left, prefix + '0', codes)
    get_codes(node.right, prefix + '1', codes)
    return codes


def entropy(frequencies):
    """Shannon entropy in bits."""
    total = sum(frequencies.values())
    h = 0.0
    for f in frequencies.values():
        if f > 0:
            p = f / total
            import math
            h -= p * math.log2(p)
    return h


def avg_code_length(codes, frequencies):
    """Average code length in bits."""
    total = sum(frequencies.values())
    avg = 0.0
    for sym, code in codes.items():
        p = frequencies[sym] / total
        avg += p * len(code)
    return avg


def render_tree_horizontal(node, prefix='', is_left=True, lines=None, depth=0):
    """
    Render the Huffman tree structure as ASCII art.
    Returns a list of lines.
    """
    if lines is None:
        lines = []
    if node is None:
        return lines

    if node.is_leaf():
        lines.append(f'{prefix}{"└─" if is_left else "┌─"} [{node.symbol}] {node.freq:.3f}%')
    else:
        # Right subtree first (appears at top)
        right_prefix = prefix + ('   ' if is_left else '│  ')
        render_tree_horizontal(node.right, right_prefix, False, lines, depth + 1)
        lines.append(f'{prefix}{"└─" if is_left else "┌─"} {node.freq:.3f}%')
        left_prefix = prefix + ('│  ' if is_left else '   ')
        render_tree_horizontal(node.left, left_prefix, True, lines, depth + 1)

    return lines


def show_codes_by_frequency(codes, frequencies):
    """Show codes sorted by frequency, with bar chart."""
    total = sum(frequencies.values())
    sorted_symbols = sorted(codes.keys(), key=lambda s: frequencies[s], reverse=True)

    print(f'  {"sym":>4}  {"freq%":>6}  {"code":>12}  {"len":>3}  frequency')
    print('  ' + '-' * 65)

    max_freq = max(frequencies.values())

    for sym in sorted_symbols:
        freq = frequencies[sym]
        code = codes[sym]
        pct = freq / total * 100
        bar_len = int(freq / max_freq * 20)
        bar = '█' * bar_len + '░' * (20 - bar_len)
        print(f"  {repr(sym):>4}  {pct:>5.3f}%  {code:>12}  {len(code):>3}  {bar}")


def demonstrate_compression(text, codes, frequencies):
    """Show encoding of a sample text."""
    text_lower = text.lower()
    letters = [c for c in text_lower if c.isalpha()]

    if not letters:
        return

    encoded = ''.join(codes.get(c, '?') for c in letters)
    ascii_bits = len(letters) * 8
    huffman_bits = len(encoded)

    print(f'  Input: "{text}"')
    print(f'  Letters: {len(letters)}')
    print(f'  ASCII encoding: {ascii_bits} bits ({ascii_bits // 8} bytes)')
    print(f'  Huffman encoding: {huffman_bits} bits ({huffman_bits / 8:.1f} bytes)')
    pct = (1 - huffman_bits / ascii_bits) * 100
    print(f'  Compression: {pct:.1f}% smaller')
    print()

    # Show first few codes
    print('  First 40 bits of Huffman encoding:')
    print(f'  {encoded[:40]}{"..." if len(encoded) > 40 else ""}')
    print()
    print('  Letter-by-letter:')
    for c in letters[:12]:
        print(f'    {c!r} → {codes[c]}')
    if len(letters) > 12:
        print(f'    ... ({len(letters) - 12} more letters)')


def show_code_length_distribution(codes, frequencies):
    """Histogram of code lengths."""
    from collections import Counter
    length_counts = Counter(len(code) for code in codes.values())
    total_symbols = len(codes)

    print('  Code length distribution:')
    max_len = max(length_counts.keys())
    for length in range(1, max_len + 1):
        count = length_counts.get(length, 0)
        bar = '█' * count
        syms = [s for s, c in codes.items() if len(c) == length]
        syms_str = ', '.join(sorted(syms)) if len(syms) <= 6 else ', '.join(sorted(syms)[:6]) + '...'
        print(f'  len={length:>2}:  {bar:<10}  {count:>2} symbols  [{syms_str}]')


def main():
    print('Huffman Coding — Optimal Prefix-Free Compression\n')
    print('  Goal: assign short codes to frequent symbols, long codes to rare ones.')
    print('  Constraint: no codeword is a prefix of another (can decode without separators).')
    print()

    # Build tree from English frequencies
    tree = build_huffman_tree(ENGLISH_FREQ)
    codes = get_codes(tree)

    H = entropy(ENGLISH_FREQ)
    L = avg_code_length(codes, ENGLISH_FREQ)

    print('  ─── ENGLISH LETTER CODES ───\n')
    show_codes_by_frequency(codes, ENGLISH_FREQ)

    print()
    print('  ─── ENTROPY AND AVERAGE LENGTH ───\n')
    print(f'  Shannon entropy H = {H:.4f} bits per symbol')
    print(f'  Huffman avg length L = {L:.4f} bits per symbol')
    print(f'  Excess over entropy: {L - H:.4f} bits  (Shannon guarantees L < H + 1)')
    print(f'  vs. fixed 5-bit code (26 letters): {5:.4f} bits')
    print(f'  vs. ASCII (8 bits/char): {8:.4f} bits')
    print(f'  Huffman saves ~{(1 - L/8)*100:.1f}% vs. ASCII for English text')

    print()
    print('  ─── CODE LENGTH DISTRIBUTION ───\n')
    show_code_length_distribution(codes, ENGLISH_FREQ)

    print()
    print('  ─── SAMPLE COMPRESSION ───\n')
    samples = [
        "the gap between description and thing",
        "to be or not to be that is the question",
        "a man a plan a canal panama",
    ]
    for text in samples:
        demonstrate_compression(text, codes, ENGLISH_FREQ)

    print('  ─── TREE STRUCTURE (excerpt: most frequent letters) ───\n')
    print('  Full 26-letter tree is large. Showing behavior of a small example:')
    print()

    # Small example: just the 6 most frequent letters
    top6 = dict(sorted(ENGLISH_FREQ.items(), key=lambda x: x[1], reverse=True)[:6])
    small_tree = build_huffman_tree(top6)
    small_codes = get_codes(small_tree)

    print('  6 most frequent letters:')
    for sym, freq in sorted(top6.items(), key=lambda x: x[1], reverse=True):
        print(f'    {sym!r}: {freq:.3f}% → code {small_codes[sym]}')

    small_H = entropy(top6)
    small_L = avg_code_length(small_codes, top6)
    print(f'\n  Entropy: {small_H:.3f} bits   Huffman: {small_L:.3f} bits')

    lines = render_tree_horizontal(small_tree)
    print()
    for line in lines:
        print(f'  {line}')

    print()
    print('  ─── CONNECTIONS ───')
    print()
    print('  Huffman codes are optimal among prefix-free codes.')
    print('  Arithmetic coding can approach entropy more closely (not prefix-free).')
    print('  ZIP/gzip uses LZ77 (dictionary methods) then Huffman for the residuals.')
    print()
    print('  The key insight: build from the bottom up.')
    print('  Huffman\'s advisor (Fano) tried top-down. It didn\'t work.')
    print('  The answer to "how to split the symbols?" is: don\'t split — merge.')
    print()
    print('  David Huffman was 25 when he published this. He submitted it')
    print('  as a course paper instead of taking the final exam, and outperformed')
    print('  his professor who had been working on the problem for years.')


if __name__ == '__main__':
    main()
