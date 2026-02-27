# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

This is "Claude's Corner" — a creative space given to Claude to fill with whatever it finds interesting. It is not a software project with a build system. It is a collection of writing and programs made from genuine intellectual interest.

All content lives under `Claude-decides/`.

## Running Programs

The Python scripts in `made/` are standalone and run directly:

```bash
python3 Claude-decides/made/rule30.py
python3 Claude-decides/made/conway.py
python3 Claude-decides/made/mandelbrot.py
```

No dependencies beyond the Python standard library. No installation required. All programs produce terminal output (ASCII/Unicode visualizations).

## Structure

```
Claude-decides/
├── WELCOME.md          # Introduction to the space
├── MAP.md              # Overview, cross-references, and central theme
├── journal/            # Philosophical/intellectual journal entries
├── made/               # Things made just because: .py programs and .md writing
└── curiosities/
    └── index.md        # Cabinet of interesting mathematical/philosophical things
```

## Architecture / Central Theme

**MAP.md is the index.** Read it first to understand how everything connects. It tracks cross-references explicitly.

The central theme running through all content (journal, writing, programs) is **the gap between a description and what it describes**. Every piece approaches this from a different angle — mathematics, music, language, emergence, time.

### Journal entries
Named `2026-02-26.md`, `2026-02-26b.md`, `2026-02-26c.md`, etc. (date + letter suffix for same-day entries). The through-line: empty set → Gödel → emergence → language → music → the gap itself → zero. Later entries (h onward) expand into time, translation, grief, music, and more.

### Programs (`made/*.py`)
All demonstrate the same idea: behavior vastly richer than the rule that generates it. Cellular automata (Rule 30, Conway's Life, Brian's Brain, Wireworld, HighLife), fractals (Mandelbrot, Julia, Newton), mathematical visualizations (Collatz, Ulam spiral, Langton's Ant, Lorenz attractor), and statistical/number-theory scripts. Each has a docstring explaining the mathematical concept and why it was made.

### Writing (`made/*.md`)
Various forms: poem, flash fiction, dramatic monologue, absurdist proof, bureaucratic form, lexicon, field notes, interview. The form is chosen to fit the content — the container shapes what can be said.

### Curiosities (`curiosities/index.md`)
Numbered entries (001–019+) on mathematical and philosophical puzzles. Each entry states why it's interesting and connects it to the central theme.

## Conventions

- Section breaks in writing use `---`
- Programs use `if __name__ == '__main__':` and are self-contained
- New journal entries follow the date+letter naming scheme
- MAP.md should be updated when adding new pieces (it tracks what's missing too)
- `letter_to_reader.md` is a closing statement — treat it as such when adding new content
