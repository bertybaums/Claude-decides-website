"""
Erdős-Rényi Random Graph — The Giant Component

Take n nodes. Add edges randomly, each with probability p.
Watch what happens as p increases.

At low p: many tiny isolated components.
At p ≈ 1/n: a "giant component" suddenly appears — one component
           containing a finite fraction of all nodes.
At high p: almost all nodes are connected to each other.

The transition at p = 1/n is a phase transition. Below it:
the largest component has O(log n) nodes. Above it: O(n) nodes.
The jump is sudden — a percolation-like threshold.

This is the mathematical model of:
  - How rumors spread through social networks
  - How epidemics ignite (R₀ > 1 ↔ above the threshold)
  - How connected the internet is (if you remove random nodes)
  - Why social networks rapidly become "small worlds"

The famous small-world result (Watts-Strogatz, 1998):
  In many real networks, any two nodes are connected by
  a surprisingly short path. "Six degrees of separation."
  This emerges from the structure of sparse random graphs.

Erdős and Rényi (1959-60): the threshold for connectivity is p = ln(n)/n.
Below this: isolated nodes remain. Above: the graph is almost surely connected.

The visualization shows n=30 nodes at different p values.
Nodes are placed on a circle. Edges connect them.
Component membership is shown by character (different symbols per component).
The giant component uses '█'; smaller components use '·', '○', '+', etc.
"""

import random
import math

# Union-Find for components
class UF:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]

    def components(self, n):
        groups = {}
        for i in range(n):
            r = self.find(i)
            groups.setdefault(r, []).append(i)
        return groups


def make_graph(n, p, seed):
    rng = random.Random(seed)
    edges = []
    uf = UF(n)
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                edges.append((i, j))
                uf.union(i, j)
    return edges, uf


def render_graph(n, edges, uf, W=70, H=35):
    """Render graph with nodes on a circle."""
    grid = [[' '] * W for _ in range(H)]

    # Node positions on circle
    cx, cy = W / 2, H / 2
    rx, ry = W * 0.42, H * 0.42
    aspect = 2.0  # chars taller than wide

    def node_pos(i):
        theta = 2 * math.pi * i / n - math.pi / 2
        col = int(cx + rx * math.cos(theta))
        row = int(cy + ry * math.sin(theta) / aspect)
        return col, row

    # Find components
    comps = uf.components(n)
    sizes = sorted(comps.items(), key=lambda x: -len(x[1]))

    # Assign symbols to components
    symbols = ['█', '▓', '▒', '░', '·', '○', '+', '×', '◆', '◇']
    node_sym = {}
    for idx, (root, members) in enumerate(sizes):
        sym = symbols[min(idx, len(symbols) - 1)]
        for m in members:
            node_sym[m] = sym

    # Draw edges first (thin lines)
    for (i, j) in edges:
        c1, r1 = node_pos(i)
        c2, r2 = node_pos(j)
        steps = max(abs(c2-c1), abs(r2-r1), 1)
        for s in range(1, steps):
            c = int(round(c1 + s / steps * (c2 - c1)))
            r = int(round(r1 + s / steps * (r2 - r1)))
            if 0 <= c < W and 0 <= r < H and grid[r][c] == ' ':
                grid[r][c] = '·'

    # Draw nodes on top
    for i in range(n):
        c, r = node_pos(i)
        if 0 <= c < W and 0 <= r < H:
            grid[r][c] = node_sym.get(i, '·')

    return grid


def component_stats(uf, n):
    comps = uf.components(n)
    sizes = sorted([len(v) for v in comps.values()], reverse=True)
    return sizes


N = 30
SEED = 42
PC = 1.0 / N  # Threshold for giant component
P_CONNECTED = math.log(N) / N  # Threshold for full connectivity

CASES = [
    (0.03,  f'p=0.03  (below threshold 1/n={1/N:.3f})'),
    (PC,    f'p=1/n={PC:.3f}  (at threshold — giant component just emerging)'),
    (0.12,  f'p=0.12  (above threshold — giant component growing)'),
    (P_CONNECTED, f'p=ln(n)/n={P_CONNECTED:.3f}  (connectivity threshold)'),
    (0.40,  f'p=0.40  (dense — most nodes connected)'),
]


def main():
    print(f'Erdős-Rényi Random Graph   n={N} nodes\n')
    print('  Add each possible edge with probability p.')
    print(f'  Giant component threshold: p = 1/n = {1/N:.3f}')
    print(f'  Full connectivity threshold: p = ln(n)/n = {P_CONNECTED:.3f}')
    print()
    print('  █ = largest component    ▓ = second largest    · = edge or isolated node')
    print()

    for p, label in CASES:
        edges, uf = make_graph(N, p, SEED)
        sizes = component_stats(uf, N)
        grid = render_graph(N, edges, uf)

        n_edges = len(edges)
        giant = sizes[0] if sizes else 0
        n_comps = len(sizes)

        print(f'  {label}')
        print(f'  {n_edges} edges   {n_comps} components   largest: {giant}/{N} nodes ({100*giant//N}%)')
        print()
        for row in grid:
            print('  ' + ''.join(row))
        print()

    print('  The transition from "fragmented" to "connected" is abrupt.')
    print(f'  At p = 1/n: the largest component suddenly jumps to O(n) size.')
    print()
    print('  This is the epidemic threshold:')
    print('  below it, outbreaks are small and self-limiting;')
    print('  above it, an epidemic can reach a finite fraction of the population.')
    print()
    print('  Erdős and Rényi proved this in 1959.')
    print('  The internet, social networks, and gene regulatory networks')
    print('  all show similar phase transitions in connectivity.')
    print()
    print('  The question "are things connected?" has a threshold answer.')
    print('  Below the threshold: mostly no. Above: mostly yes.')
    print('  At the threshold: something is happening.')


if __name__ == '__main__':
    main()
