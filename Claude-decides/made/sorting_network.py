"""
Sorting Networks — Parallel Sorting in Fixed Structure

A sorting network is a fixed sequence of "comparators":
each comparator takes two wires, compares the values,
and outputs the smaller on top (larger on bottom).

The network is "oblivious" — the same comparators fire in the same
order regardless of the input. This is unusual:
most sorting algorithms adapt to the input (quicksort, mergesort).
A sorting network doesn't adapt; it just always works.

This makes them suitable for hardware and parallel computation:
all comparators at the same "depth" can run simultaneously.

Depth: the number of parallel steps required.
Wire count n=4: optimal network has depth 3 (all comparators in 3 steps).
Wire count n=16: optimal depth is 9 (very hard to prove).

The "0-1 principle": a sorting network correctly sorts all inputs
if and only if it correctly sorts all inputs consisting only of 0s and 1s.
This dramatically simplifies verification.

Types shown here:
  - Bubble sort network (simple but deep)
  - Odd-Even Merge Sort (Batcher, 1968): O(log²n) depth
  - Bitonic Sort (another Batcher construction): also O(log²n) depth

The structure of these networks is beautiful when drawn:
the parallel stages look like layers, and the comparators
form patterns that reflect the mathematical structure of the sort.

An open problem: what is the minimum number of comparators
needed to sort n inputs? Known for n ≤ 11; unknown for n ≥ 12.
"""

import random


def apply_comparator(arr, i, j):
    """Apply a compare-and-swap on positions i, j (smaller goes to i)."""
    if arr[i] > arr[j]:
        arr[i], arr[j] = arr[j], arr[i]


def bubble_sort_network(n):
    """
    Generate comparators for bubble sort network.
    Returns list of (i, j) pairs. Depth = 2n-3 (inefficient but simple).
    """
    comparators = []
    for k in range(n):
        for i in range(k % 2, n - 1, 2):
            comparators.append((i, i + 1))
    return comparators


def bitonic_sort_network(n):
    """
    Generate comparators for bitonic sort (n must be power of 2).
    Returns list of layers, each layer a list of (i, j) pairs.
    Depth = log²(n) / 2 + log(n)/2
    """
    layers = []

    def compare_and_swap(lo, cnt, direction):
        """Generate a half-cleaner step."""
        step = []
        half = cnt // 2
        for i in range(lo, lo + half):
            if direction:
                step.append((i, i + half))
            else:
                step.append((i + half, i))
        return step

    def bitonic_merge(lo, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            layers.append(compare_and_swap(lo, cnt, direction))
            bitonic_merge(lo, k, direction)
            bitonic_merge(lo + k, k, direction)

    def bitonic_sort_rec(lo, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            bitonic_sort_rec(lo, k, True)
            bitonic_sort_rec(lo + k, k, False)
            bitonic_merge(lo, cnt, direction)

    bitonic_sort_rec(0, n, True)
    return layers


def odd_even_merge_sort_network(n):
    """
    Batcher's odd-even merge sort (n must be power of 2).
    Returns list of layers. Depth = O(log²n).
    """
    comparators_all = []

    def odd_even_merge(lo, hi, step):
        """Merge two sorted subsequences."""
        span = hi - lo + 1
        if step < span:
            if step * 2 < span:
                odd_even_merge(lo, hi, step * 2)
                odd_even_merge(lo + step, hi, step * 2)
                for i in range(lo + step, hi - step + 1, step * 2):
                    comparators_all.append((len(comparators_all), i, i + step))
            else:
                comparators_all.append((len(comparators_all), lo, lo + step))

    def odd_even_merge_sort_rec(lo, hi):
        if lo < hi:
            mid = (lo + hi) // 2
            odd_even_merge_sort_rec(lo, mid)
            odd_even_merge_sort_rec(mid + 1, hi)
            odd_even_merge(lo, hi, 1)

    odd_even_merge_sort_rec(0, n - 1)
    return [(c[1], c[2]) for c in comparators_all]


def run_network(arr, comparators_flat):
    """Apply a flat list of comparators to arr (in place)."""
    a = arr[:]
    for i, j in comparators_flat:
        if i < len(a) and j < len(a):
            apply_comparator(a, i, j)
    return a


def verify_network(n, comparators):
    """Verify the network sorts all 2^n binary inputs (0-1 principle)."""
    if n > 12:
        # Too many to check; sample
        for _ in range(1000):
            arr = [random.randint(0, 1) for _ in range(n)]
            result = run_network(arr, comparators)
            if result != sorted(result):
                return False
        return True

    for bits in range(2 ** n):
        arr = [(bits >> i) & 1 for i in range(n)]
        result = run_network(arr, comparators)
        if result != sorted(result):
            return False
    return True


def render_network(n, layers, title, max_render_n=12):
    """
    Render a sorting network as ASCII art.
    Wires are horizontal lines; comparators are vertical bars.
    """
    print(f'  {title}')
    if n > max_render_n:
        print(f'  (n={n}: too large to render clearly)')
        return

    # Track wire labels for display
    wire_chars = '0123456789ABCDEF'

    # Build render grid
    # Each layer gets a column; we'll add spacing
    col_width = 3

    # Header: wire numbers
    header = '  '
    for w in range(n):
        header += f'W{w:<2}'
    print(header)
    print('  ' + '─' * (n * col_width))

    # For each layer, draw comparators
    for layer_idx, layer in enumerate(layers):
        active_wires = set()
        for i, j in layer:
            active_wires.update(range(min(i, j), max(i, j) + 1))

        rows = []
        for wire in range(n):
            if wire in active_wires:
                # Check if this wire is an endpoint
                is_top = any(min(i, j) == wire for i, j in layer)
                is_bot = any(max(i, j) == wire for i, j in layer)
                is_middle = wire in active_wires and not is_top and not is_bot

                if is_top and is_bot:
                    rows.append('─╪─')  # single-step comparator
                elif is_top:
                    rows.append('─┬─')
                elif is_bot:
                    rows.append('─┴─')
                else:
                    rows.append('─┼─')
            else:
                rows.append('───')

        # Print each row
        for wire in range(n):
            print(f'  {rows[wire]}', end='')
        print(f'  ← layer {layer_idx + 1}')

    print('  ' + '─' * (n * col_width))


def render_network_horizontal(n, layers, title):
    """
    Better visualization: wires go left-to-right,
    comparators appear as vertical connections between layers.
    """
    print(f'  {title}  ({n} wires, {len(layers)} layers, {sum(len(l) for l in layers)} comparators)')
    print()

    if n > 16:
        print(f'  n={n}: rendering abbreviated.')
        return

    # Each wire is a row; each layer is a column group
    # Wire display: '──' between comparators, '╥' at top, '╨' at bottom, '╫' in middle

    col_w = 3  # characters per layer
    wire_rows = ['' for _ in range(n)]

    for layer in layers:
        # Find which wires are active in this layer
        active = {}
        for lo, hi in layer:
            for w in range(lo, hi + 1):
                if w == lo:
                    active[w] = 'T' if lo < hi else '?'
                elif w == hi:
                    active[w] = 'B'
                else:
                    active[w] = 'M'

        for w in range(n):
            if w in active:
                mark = active[w]
                if mark == 'T':
                    wire_rows[w] += '─┬─'
                elif mark == 'B':
                    wire_rows[w] += '─┴─'
                else:
                    wire_rows[w] += '─┼─'
            else:
                wire_rows[w] += '───'

    # Print
    for w, row in enumerate(wire_rows):
        print(f'  {w:>2} ──{row}──')
    print()


def show_sorting_demo(n, layers_flat, label):
    """Show the network sorting a specific input."""
    test = list(range(n, 0, -1))  # reverse sorted (worst case)
    result = run_network(test, layers_flat)

    print(f'  {label}:')
    print(f'    Input:  {test}')
    print(f'    Output: {result}')
    print(f'    Sorted: {result == sorted(result)}')


def main():
    print('Sorting Networks — Parallel Fixed-Structure Sorting\n')
    print('  A sorting network is a fixed sequence of compare-and-swap operations.')
    print('  The same operations run regardless of input (oblivious algorithm).')
    print('  Operations at the same depth run in parallel.')
    print()

    # ─── n=4 bubble sort ───
    print('  ─── BUBBLE SORT NETWORK, n=4 ───\n')
    n = 4
    bub = bubble_sort_network(n)

    # Group into layers manually for bubble sort (odd-even transposition)
    bub_layers = []
    for k in range(n):
        layer = []
        for i in range(k % 2, n - 1, 2):
            layer.append((i, i + 1))
        if layer:
            bub_layers.append(layer)

    render_network_horizontal(n, bub_layers, 'Bubble Sort (odd-even transposition)')

    verified = verify_network(n, bub)
    print(f'  Verified (0-1 principle): {verified}')
    print(f'  Comparators: {len(bub)}  Depth: {len(bub_layers)}')
    show_sorting_demo(n, bub, 'Bubble sort n=4')

    print()

    # ─── Bitonic sort n=8 ───
    print('  ─── BITONIC SORT, n=8 ───\n')
    n = 8
    bit_layers = bitonic_sort_network(n)
    bit_flat = [c for layer in bit_layers for c in layer]

    render_network_horizontal(n, bit_layers, 'Bitonic Sort')
    verified = verify_network(n, bit_flat)
    print(f'  Verified (0-1 principle): {verified}')
    n_comparators = sum(len(l) for l in bit_layers)
    print(f'  Comparators: {n_comparators}  Depth: {len(bit_layers)}')
    show_sorting_demo(n, bit_flat, 'Bitonic sort n=8')

    print()

    # ─── Comparison table ───
    print('  ─── NETWORK STATISTICS ───\n')
    print(f'  {"n":>4}  {"bubble comparators":>19}  {"bubble depth":>13}  {"bitonic comparators":>20}  {"bitonic depth":>14}')
    print('  ' + '-' * 80)
    for n in [4, 8, 16, 32]:
        bub_net = bubble_sort_network(n)
        bub_l = []
        for k in range(n):
            layer = [(i, i + 1) for i in range(k % 2, n - 1, 2)]
            if layer:
                bub_l.append(layer)

        bit_l = bitonic_sort_network(n)
        bit_comp = sum(len(l) for l in bit_l)

        print(f'  {n:>4}  {len(bub_net):>19}  {len(bub_l):>13}  {bit_comp:>20}  {len(bit_l):>14}')

    print()
    print('  ─── THE 0-1 PRINCIPLE ───\n')
    print('  A network correctly sorts all inputs iff it correctly sorts all binary (0/1) inputs.')
    print('  Proof sketch: if a network sorts all 0-1 sequences, then for any input,')
    print('  replacing values with 0 (if ≤ threshold) and 1 (if > threshold) gives a 0-1 sequence')
    print('  that the network sorts correctly. Applying this for all thresholds proves the general case.')
    print()
    print('  This reduces verification from "check all n! permutations" to "check 2^n binary inputs".')
    print('  For n=16: from 20 trillion to 65536 checks.')
    print()
    print('  ─── OPEN PROBLEMS ───\n')
    print('  Minimum comparators to sort n inputs:')
    known = [(1, 0), (2, 1), (3, 3), (4, 5), (5, 9), (6, 12), (7, 16), (8, 19),
             (9, 25), (10, 29), (11, 35)]
    for n, k in known:
        print(f'    n={n}: {k} comparators')
    print('    n=12: 39 (proven lower bound: 39; best known: 39) — barely resolved')
    print('    n≥13: unknown')
    print()
    print('  The minimum-depth problem is similarly open for large n.')
    print('  For n=16: 9 layers is known optimal.')
    print('  The structure of optimal networks is deeply non-obvious.')


if __name__ == '__main__':
    main()
