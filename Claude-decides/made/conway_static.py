"""Same logic, no animation — just prints a few snapshots."""

WIDTH, HEIGHT = 80, 30

def make_grid():
    return [[False] * WIDTH for _ in range(HEIGHT)]

def count_neighbors(grid, r, c):
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = (r + dr) % HEIGHT, (c + dc) % WIDTH
            if grid[nr][nc]:
                count += 1
    return count

def step(grid):
    new_grid = make_grid()
    for r in range(HEIGHT):
        for c in range(WIDTH):
            n = count_neighbors(grid, r, c)
            if grid[r][c]:
                new_grid[r][c] = n in (2, 3)
            else:
                new_grid[r][c] = n == 3
    return new_grid

def display(grid, generation):
    print(f"--- Generation {generation} ---")
    for row in grid:
        print(''.join('█' if cell else '·' for cell in row))
    print()

def place(grid, pattern, row, col):
    for dr, dc in pattern:
        r, c = (row + dr) % HEIGHT, (col + dc) % WIDTH
        grid[r][c] = True

GOSPER_GLIDER_GUN = [
    (0, 24),
    (1, 22), (1, 24),
    (2, 12), (2, 13), (2, 20), (2, 21), (2, 34), (2, 35),
    (3, 11), (3, 15), (3, 20), (3, 21), (3, 34), (3, 35),
    (4, 0), (4, 1), (4, 10), (4, 16), (4, 20), (4, 21),
    (5, 0), (5, 1), (5, 10), (5, 14), (5, 16), (5, 17), (5, 22), (5, 24),
    (6, 10), (6, 16), (6, 24),
    (7, 11), (7, 15),
    (8, 12), (8, 13),
]

grid = make_grid()
place(grid, GOSPER_GLIDER_GUN, row=5, col=2)

snapshots = [0, 30, 60, 100, 150]
for gen in range(151):
    if gen in snapshots:
        display(grid, gen)
    grid = step(grid)
