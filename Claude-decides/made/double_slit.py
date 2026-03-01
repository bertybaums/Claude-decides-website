"""
Double-Slit Interference — Where Waves Meet

When waves pass through two slits, they spread and overlap.
Where two crests meet: constructive interference (bright).
Where a crest meets a trough: destructive interference (dark).
The result: alternating bands of bright and dark — a fringe pattern.

This is wave interference. It works for water waves, sound waves,
light waves, and — most disturbingly — single photons and single electrons.

The double-slit experiment is famous because quantum particles
show interference patterns even when sent one at a time.
The single particle seems to pass through both slits simultaneously
and interfere with itself. This is not a metaphor. The fringes appear.

When you try to detect which slit the particle passed through,
the fringes disappear. The act of measurement changes the result.
This is the measurement problem. It has not been resolved.

Below: two visualizations
  1. Amplitude map (sum of two wave sources)
  2. Intensity map (amplitude squared — what you'd see on a screen)

The slits are in the middle column. The screen is on the right.
"""

import math

WIDTH = 74
HEIGHT = 38

# Physical parameters
WAVELENGTH = 6.0       # in grid units
SLIT_SEP = 8           # distance between slits (grid units)
SLIT_Y1 = HEIGHT // 2 - SLIT_SEP // 2
SLIT_Y2 = HEIGHT // 2 + SLIT_SEP // 2
BARRIER_X = WIDTH // 3
SOURCE_X = 5           # incoming plane wave from left


def two_source_amplitude(x, y, slit_y1, slit_y2, barrier_x, wavelength):
    """
    Amplitude at (x, y) from two coherent point sources at the slits.
    Only computed for x > barrier_x (the right side).
    """
    k = 2 * math.pi / wavelength

    r1 = math.hypot(x - barrier_x, y - slit_y1)
    r2 = math.hypot(x - barrier_x, y - slit_y2)

    # Amplitude decays as 1/sqrt(r), phase as e^{ikr}
    # Sum the two sources
    if r1 < 0.5: r1 = 0.5
    if r2 < 0.5: r2 = 0.5

    a1 = math.cos(k * r1) / math.sqrt(r1)
    a2 = math.cos(k * r2) / math.sqrt(r2)
    return a1 + a2


def render_amplitude():
    """Amplitude map: positive=above baseline, negative=below."""
    # Precompute
    field = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            if x < BARRIER_X - 1:
                # Incident plane wave
                k = 2 * math.pi / WAVELENGTH
                val = math.cos(k * x)
            elif x == BARRIER_X - 1 or x == BARRIER_X:
                # Barrier
                if y == SLIT_Y1 or y == SLIT_Y2:
                    val = 0.0  # slit opening
                else:
                    val = None  # solid barrier
            else:
                val = two_source_amplitude(x, y, SLIT_Y1, SLIT_Y2, BARRIER_X, WAVELENGTH)
            row.append(val)
        field.append(row)

    # Find max amplitude for normalization
    vals = [v for row in field for v in row if v is not None]
    vmax = max(abs(v) for v in vals) if vals else 1.0

    # Render
    CHARS_POS = ' ░▒▓█'
    CHARS_NEG = ' ░▒▓█'
    lines = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            val = field[y][x]
            if val is None:
                row.append('│')
            else:
                n = val / vmax  # -1 to 1
                if n >= 0:
                    idx = int(n * (len(CHARS_POS) - 1))
                    row.append(CHARS_POS[idx])
                else:
                    idx = int(-n * (len(CHARS_NEG) - 1))
                    row.append(CHARS_NEG[idx])
        lines.append(''.join(row))
    return lines, field, vmax


def render_intensity(field, vmax):
    """Intensity = amplitude^2. Shows what a detector screen would see."""
    CHARS = ' ·:;+=xX#█'

    lines = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            val = field[y][x]
            if val is None:
                row.append('│')
            else:
                intensity = (val / vmax) ** 2   # 0 to 1
                idx = int(intensity * (len(CHARS) - 1))
                row.append(CHARS[idx])
        lines.append(''.join(row))
    return lines


def intensity_at_screen(field):
    """Return intensity profile at the rightmost column."""
    x = WIDTH - 1
    profile = []
    for y in range(HEIGHT):
        val = field[y][x]
        if val is not None:
            profile.append((y, val))
    return profile


def main():
    print('Double-Slit Interference\n')
    print(f'  Wavelength: {WAVELENGTH:.0f} units | Slit separation: {SLIT_SEP} units')
    print(f'  Slits at y={SLIT_Y1} and y={SLIT_Y2} | Barrier at x={BARRIER_X}')
    print()

    amp_lines, field, vmax = render_amplitude()
    int_lines = render_intensity(field, vmax)

    # Mark slit positions on a guide line
    print('  Plane wave →   barrier    → diffracted waves')
    print()

    print('  AMPLITUDE (light = positive, dark = negative):')
    print('  ┌' + '─' * WIDTH + '┐')
    for i, line in enumerate(amp_lines):
        marker = ''
        if i == SLIT_Y1:
            marker = ' ← slit 1'
        elif i == SLIT_Y2:
            marker = ' ← slit 2'
        print(f'  │{line}│{marker}')
    print('  └' + '─' * WIDTH + '┘')

    print()
    print('  INTENSITY (amplitude² — what a screen would record):')
    print('  ┌' + '─' * WIDTH + '┐')
    for i, line in enumerate(int_lines):
        marker = ''
        if i == SLIT_Y1:
            marker = ' ← slit 1'
        elif i == SLIT_Y2:
            marker = ' ← slit 2'
        print(f'  │{line}│{marker}')
    print('  └' + '─' * WIDTH + '┘')

    print()

    # Screen profile (rightmost column)
    profile = intensity_at_screen(field)
    if profile:
        ivals = [v for _, v in profile]
        vmax_i = max(abs(v) for v in ivals) if ivals else 1.0
        BAR_W = 20
        print('  Screen intensity profile (right edge):')
        center_y = HEIGHT // 2
        for y, val in profile:
            intensity = (val / vmax) ** 2
            bar_len = int(intensity / 1.0 * BAR_W)
            bar = '█' * bar_len + '░' * (BAR_W - bar_len)
            bright = '◉' if intensity > 0.7 else ('·' if intensity > 0.1 else ' ')
            dist = y - center_y
            print(f'  y={dist:+3d}  {bar}  {bright}')

    print()
    print('  Bright bands: constructive interference (path difference = nλ)')
    print('  Dark bands:   destructive interference  (path difference = (n+½)λ)')
    print()
    print('  Fringe spacing = λ·L / d')
    print(f'  λ={WAVELENGTH:.0f}, L≈{WIDTH - BARRIER_X}, d={SLIT_SEP}  →  fringe ≈ {WAVELENGTH * (WIDTH - BARRIER_X) / SLIT_SEP:.1f} units')
    print()
    print('  This same pattern appears when single electrons are fired')
    print('  one at a time. Each electron lands as a point, but the')
    print('  pattern that accumulates over many electrons shows fringes.')
    print()
    print('  Each electron interferes with itself.')
    print('  This has been verified. It has not been explained.')


if __name__ == '__main__':
    main()
