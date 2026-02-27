"""
The Overtone Series vs. Equal Temperament.

When you strike a string, it vibrates at many frequencies simultaneously:
  - The fundamental (f)
  - The 2nd harmonic (2f) — one octave up
  - The 3rd harmonic (3f) — one octave + a fifth up
  - The 4th harmonic (4f) — two octaves up
  - ...

These overtones are exact integer multiples of the fundamental.
They're what makes a violin sound different from a flute playing the same note:
different instruments produce different overtone mixes.

The piano uses *equal temperament*: each octave is divided into 12 equal steps,
each a ratio of 2^(1/12) ≈ 1.0595. This means every semitone is exactly equal,
every key is playable in, and no interval is exactly in tune.

The natural overtone series produces beautiful simple ratios:
  - Perfect fifth: exactly 3/2 = 1.5000
  - Equal temperament fifth: 2^(7/12) = 1.4983

The difference is 2 cents (hundredths of a semitone). Barely perceptible.
But it accumulates: tune 12 consecutive pure fifths and you don't return
to the octave. You arrive 23 cents sharp. The Pythagorean comma.

Equal temperament splits the comma evenly across all 12 intervals.
Everyone is equally, imperceptibly out of tune. Music is possible everywhere.
The compromise is 2 cents. The gain is the entire keyboard repertoire.
"""

import math

# Equal temperament: semitone = 2^(1/12)
SEMITONE = 2 ** (1/12)

# Note names for 12-tone equal temperament (starting from C)
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Middle C = MIDI 60. For display, use C4 as reference.
# Frequency of C4 = 261.63 Hz
C4 = 261.63


def semitones_above_c4(freq):
    """How many semitones above C4 is this frequency?"""
    return 12 * math.log2(freq / C4)


def note_name(semitones_from_c4):
    """Name of the note n semitones above C4."""
    octave_offset = int(semitones_from_c4) // 12
    position = int(round(semitones_from_c4)) % 12
    octave = 4 + octave_offset
    name = NOTE_NAMES[position % 12]
    return f"{name}{octave}"


def cents_error(exact_freq, tempered_note_semitones):
    """
    Cents error: how far is the exact frequency from the nearest
    equal-tempered note?
    Positive = sharp; negative = flat.
    """
    exact_semitones = semitones_above_c4(exact_freq)
    return (exact_semitones - tempered_note_semitones) * 100


def nearest_et_note(freq):
    """Return (note_name, semitones_above_c4, cents_error) for nearest ET note."""
    s = semitones_above_c4(freq)
    s_rounded = round(s)
    cents = (s - s_rounded) * 100
    name = note_name(s_rounded)
    return name, s_rounded, cents


if __name__ == '__main__':
    print("The Overtone Series vs. Equal Temperament")
    print(f"Reference: middle C (C4) = {C4} Hz\n")

    print("The natural overtone series for a string vibrating at C4:\n")
    print(f"  {'Harmonic':>9}  {'Frequency':>10}  {'Ratio':>8}  {'Nearest ET note':>15}  {'Error (cents)':>13}  Name")
    print("  " + "─" * 75)

    # Show first 16 harmonics
    names = [
        '', 'fundamental', 'octave', 'fifth', 'octave', 'major third', 'fifth',
        'minor seventh*', 'octave', 'major second', 'major third', 'tritone*',
        'fifth', 'major sixth*', 'minor seventh*', 'major seventh',
    ]

    for n in range(1, 17):
        freq = C4 * n
        ratio = f"{n}/1" if n <= 4 else f"{n}"
        name, s_rounded, cents = nearest_et_note(freq)
        interval = names[n] if n < len(names) else ''
        cents_str = f"{cents:+.1f}"
        flag = '  ✓' if abs(cents) < 5 else '  ≈' if abs(cents) < 15 else '  ✗'
        print(f"  {n:>9}  {freq:>10.2f}  {ratio:>8}  {name:>15}  {cents_str:>13}  {interval}{flag}")

    print()
    print("  ✓ = nearly in tune  ≈ = slightly off  ✗ = noticeably out of tune")
    print("  * = these harmonics have no good equal-tempered equivalent")
    print()

    print("─" * 60)
    print("The Pythagorean comma:\n")
    print("  Pure fifth: 3/2 = 1.50000")
    print(f"  ET fifth:   2^(7/12) = {2**(7/12):.5f}")
    print(f"  Error per fifth: {(2**(7/12) - 1.5) / 1.5 * 1200:.1f} cents")
    print()

    # Stack 12 pure fifths
    after_12_fifths = C4 * (1.5 ** 12)
    after_7_octaves = C4 * (2 ** 7)
    comma = 12 * math.log2(after_12_fifths / after_7_octaves) * 100

    print(f"  After 12 pure fifths: {after_12_fifths:.2f} Hz")
    print(f"  After 7 octaves (expected): {after_7_octaves:.2f} Hz")
    print(f"  Pythagorean comma: {comma:.1f} cents sharp")
    print()
    print("  Equal temperament distributes this comma across 12 intervals.")
    print(f"  Each fifth is {comma/12:.2f} cents flat. Barely audible.")
    print("  The tradeoff: every key playable. The cost: no interval exact.")
    print()
    print("  The piano is slightly wrong everywhere")
    print("  so it can be approximately right everywhere.")
