"""
3D ASCII Wireframe — Projection and Rotation

Demonstrates how 3D objects are rendered in 2D:
  1. Define vertices in 3D space
  2. Apply rotation matrices
  3. Project to 2D with perspective
  4. Draw edges between projected vertices

Rotation matrices (right-hand rule):
  Rx(θ): rotation around x-axis
  Ry(φ): rotation around y-axis
  Rz(ψ): rotation around z-axis

Perspective projection (point P at distance d from camera at origin):
  x_screen = x / (z + d) · scale
  y_screen = y / (z + d) · scale

Objects shown:
  1. Cube — 8 vertices, 12 edges
  2. Octahedron — 6 vertices, 12 edges
  3. Torus — approximated by vertex ring grid
  4. Icosahedron — 12 vertices, 30 edges (dual of dodecahedron)

This is how all 3D graphics worked before hardware acceleration:
  project, clip, rasterize — in software, one vertex at a time.
"""

import math

WIDTH = 60
HEIGHT = 28
D_PERSP = 3.0  # perspective distance
SCALE = 10.0


def rotate(x, y, z, rx, ry, rz):
    """Apply Rx, Ry, Rz rotations."""
    # Rx
    y, z = y * math.cos(rx) - z * math.sin(rx), y * math.sin(rx) + z * math.cos(rx)
    # Ry
    x, z = x * math.cos(ry) + z * math.sin(ry), -x * math.sin(ry) + z * math.cos(ry)
    # Rz
    x, y = x * math.cos(rz) - y * math.sin(rz), x * math.sin(rz) + y * math.cos(rz)
    return x, y, z


def project(x, y, z, d=D_PERSP, scale=SCALE, w=WIDTH, h=HEIGHT):
    """Perspective projection to screen coordinates."""
    denom = z + d
    if denom <= 0.1:
        denom = 0.1
    sx = x / denom * scale + w / 2
    sy = -y / denom * scale + h / 2
    return int(sx), int(sy)


def draw_line(grid, x0, y0, x1, y1, char='·', w=WIDTH, h=HEIGHT):
    """Bresenham line drawing on a character grid."""
    dx = abs(x1 - x0); dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    steps = 0
    while steps < 500:
        if 0 <= x0 < w and 0 <= y0 < h:
            if grid[y0][x0] == ' ':
                grid[y0][x0] = char
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy; x0 += sx
        if e2 < dx:
            err += dx; y0 += sy
        steps += 1


def render_object(vertices, edges, rx, ry, rz, title):
    """Render a 3D wireframe at given rotation angles."""
    # Rotate all vertices
    rotated = [rotate(x, y, z, rx, ry, rz) for x, y, z in vertices]
    # Project to 2D
    projected = [project(x, y, z) for x, y, z in rotated]

    # Draw
    grid = [[' '] * WIDTH for _ in range(HEIGHT)]
    for i, j in edges:
        x0, y0 = projected[i]
        x1, y1 = projected[j]
        draw_line(grid, x0, y0, x1, y1, '·')

    # Draw vertices
    for sx, sy in projected:
        if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
            grid[sy][sx] = '●'

    print(f'  {title}')
    print('  ┌' + '─' * WIDTH + '┐')
    for row in grid:
        print('  │' + ''.join(row) + '│')
    print('  └' + '─' * WIDTH + '┘')


def make_cube():
    """Unit cube vertices and edges."""
    vertices = [
        (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),  # back
        (-1, -1,  1), (1, -1,  1), (1, 1,  1), (-1, 1,  1),  # front
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # back face
        (4, 5), (5, 6), (6, 7), (7, 4),  # front face
        (0, 4), (1, 5), (2, 6), (3, 7),  # connecting edges
    ]
    return vertices, edges


def make_octahedron():
    """Regular octahedron vertices and edges."""
    r = 1.4
    vertices = [
        (r, 0, 0), (-r, 0, 0),
        (0, r, 0), (0, -r, 0),
        (0, 0, r), (0, 0, -r),
    ]
    edges = [
        (0, 2), (0, 3), (0, 4), (0, 5),
        (1, 2), (1, 3), (1, 4), (1, 5),
        (2, 4), (2, 5), (3, 4), (3, 5),
    ]
    return vertices, edges


def make_torus(R=1.2, r=0.5, n_major=14, n_minor=8):
    """Torus as vertex grid."""
    vertices = []
    for i in range(n_major):
        phi = 2 * math.pi * i / n_major
        for j in range(n_minor):
            theta = 2 * math.pi * j / n_minor
            x = (R + r * math.cos(theta)) * math.cos(phi)
            y = (R + r * math.cos(theta)) * math.sin(phi)
            z = r * math.sin(theta)
            vertices.append((x, y, z))

    edges = []
    for i in range(n_major):
        for j in range(n_minor):
            idx = i * n_minor + j
            next_j = i * n_minor + (j + 1) % n_minor
            next_i = ((i + 1) % n_major) * n_minor + j
            edges.append((idx, next_j))    # minor circle
            if i % 2 == 0:                 # major circles (every other)
                edges.append((idx, next_i))

    return vertices, edges


def make_icosahedron():
    """Regular icosahedron vertices and edges."""
    phi = (1 + math.sqrt(5)) / 2  # golden ratio
    s = 1.0
    vertices = [
        (0, s, phi), (0, -s, phi), (0, s, -phi), (0, -s, -phi),
        (s, phi, 0), (-s, phi, 0), (s, -phi, 0), (-s, -phi, 0),
        (phi, 0, s), (-phi, 0, s), (phi, 0, -s), (-phi, 0, -s),
    ]
    # Normalize
    norm = math.sqrt(1 + phi**2)
    vertices = [(x/norm, y/norm, z/norm) for x, y, z in vertices]

    # Edges: connect vertices at distance ~2/norm
    edges = []
    target_dist = 2 / norm
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            dx = vertices[i][0] - vertices[j][0]
            dy = vertices[i][1] - vertices[j][1]
            dz = vertices[i][2] - vertices[j][2]
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if abs(dist - target_dist) < 0.01:
                edges.append((i, j))

    return vertices, edges


def main():
    print('3D ASCII Wireframe — Projection and Rotation\n')
    print('  Vertices rotated, then projected with perspective:')
    print('  x_screen = x/(z+d)·s,  y_screen = y/(z+d)·s')
    print()

    # Cube at different angles
    cube_v, cube_e = make_cube()
    render_object(cube_v, cube_e,
                  rx=0.5, ry=0.7, rz=0.2,
                  title='Cube (rx=0.5, ry=0.7, rz=0.2)')

    print()
    render_object(cube_v, cube_e,
                  rx=0.3, ry=1.1, rz=0.4,
                  title='Cube (different angle)')

    print()

    oct_v, oct_e = make_octahedron()
    render_object(oct_v, oct_e,
                  rx=0.4, ry=0.6, rz=0.1,
                  title='Octahedron (dual of cube)')

    print()

    torus_v, torus_e = make_torus()
    render_object(torus_v, torus_e,
                  rx=0.4, ry=0.3, rz=0.1,
                  title='Torus (R=1.2, r=0.5)')

    print()

    ico_v, ico_e = make_icosahedron()
    render_object(ico_v, ico_e,
                  rx=0.5, ry=0.8, rz=0.3,
                  title=f'Icosahedron ({len(ico_v)} vertices, {len(ico_e)} edges, φ-symmetric)')

    print()
    print('  The golden ratio φ appears in the icosahedron: each vertex is')
    print('  a cyclic permutation of (0, ±1, ±φ), projected onto the unit sphere.')
    print()
    print('  Perspective: objects that are farther (larger z) appear smaller.')
    print('  The effect is subtle here because the objects are small relative to D.')
    print('  Increase perspective by reducing D for more dramatic foreshortening.')


if __name__ == '__main__':
    main()
