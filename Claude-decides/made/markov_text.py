"""
Markov Chains and Text Generation

A Markov chain assigns to each state a probability distribution
over the next state. The Markov property: the next state depends
only on the current state, not the history.

For text generation:
  - State = the last n characters (or words)
  - Transition = probability of the next character (or word)
  - The chain "remembers" n characters and predicts the (n+1)th

Order-1 chain: probabilities depend only on current character
Order-2 chain: probabilities depend on current pair of characters
Order-n chain: probabilities depend on the last n characters

At low order, the output looks random with slight regularities.
At high order, the output looks like the source text (just shuffled).
The sweet spot (order 3-6) produces something uncanny: it looks like
language without being language.

Shannon's experiment (1948): using letter frequencies, then bigram
frequencies, then trigram frequencies, he showed that text with
higher-order Markov statistics becomes progressively more English-like.

What this reveals:
  - Language has strong local structure (after "th", "e" is very likely)
  - But meaning requires structure at scales that Markov chains can't capture
  - The gap between "looks like language" and "is language" is meaning

The chain produces something that has the texture of speech
without having its substance. It is the form without the content.
It is the description of how language sounds, not what it says.
"""

import random
from collections import defaultdict


# The source text — a short philosophical passage for demonstration
SOURCE_TEXT = """
The limits of my language mean the limits of my world.
Whereof one cannot speak, thereof one must be silent.
The world is all that is the case. The world is the totality of facts, not of things.
What can be said at all can be said clearly, and what we cannot talk about
we must pass over in silence.
The world divides into facts. Any fact can either be the case or not be the case.
A logical picture of facts is a thought. A thought is a proposition with a sense.
Language disguises thought. So much so that from the outward form of the clothing
it is impossible to infer the form of the thought beneath.
Most of the propositions and questions of philosophers arise from our failure
to understand the logic of our language. They are of the same kind as the question
whether the Good is more or less identical than the Beautiful.
Philosophy is not one of the natural sciences.
The object of philosophy is the logical clarification of thoughts.
Philosophy is not a body of doctrine but an activity.
""".strip()


def build_markov_model(text, order=3):
    """Build an order-n Markov model from text."""
    model = defaultdict(list)
    for i in range(len(text) - order):
        context = text[i:i + order]
        next_char = text[i + order]
        model[context].append(next_char)
    return dict(model)


def generate_text(model, order, length=300, seed=None):
    """Generate text from a Markov model."""
    if seed is None:
        # Pick a random starting context that begins a word
        starts = [k for k in model.keys() if k[0] in ' \n']
        seed = random.choice(starts) if starts else random.choice(list(model.keys()))

    text = seed
    context = seed
    for _ in range(length - order):
        if context in model:
            next_char = random.choice(model[context])
            text += next_char
            context = context[1:] + next_char
        else:
            # Dead end: restart
            new_starts = [k for k in model.keys() if k[0] in ' \n']
            if new_starts:
                context = random.choice(new_starts)
            else:
                context = random.choice(list(model.keys()))
            text += context[0]
            context = context[1:] + text[-1]

    return text


def count_transitions(text, order=1):
    """Count transitions and return as frequency table."""
    counts = defaultdict(lambda: defaultdict(int))
    for i in range(len(text) - order):
        context = text[i:i + order]
        next_char = text[i + order]
        counts[context][next_char] += 1
    return dict(counts)


def show_transition_matrix(text, top_contexts=8):
    """Show top transitions as a table."""
    counts = count_transitions(text, order=1)

    # Find most common single-character contexts
    context_totals = {ctx: sum(nexts.values()) for ctx, nexts in counts.items()}
    top = sorted(context_totals.items(), key=lambda x: x[1], reverse=True)[:top_contexts]

    print('  Most frequent character transitions (order 1):')
    print()
    print(f'  {"Context":>8}   {"Total":>5}   Top 5 successors')
    print('  ' + '-' * 65)

    for ctx, total in top:
        nexts = counts[ctx]
        top_next = sorted(nexts.items(), key=lambda x: x[1], reverse=True)[:5]
        successors = '  '.join(f'{repr(c):>4}:{n:>3}' for c, n in top_next)
        print(f'  {repr(ctx):>8}   {total:>5}   {successors}')


def show_order_comparison(text, length=200):
    """Show generated text at different orders."""
    random.seed(42)

    for order in [1, 2, 3, 5, 7]:
        model = build_markov_model(text, order=order)
        generated = generate_text(model, order, length=length)
        # Trim to last complete word
        last_space = generated.rfind(' ')
        if last_space > length - 30:
            generated = generated[:last_space]

        print(f'  Order {order}:')
        # Wrap at 60 chars
        words = generated.replace('\n', ' ').split()
        line = '    '
        for word in words:
            if len(line) + len(word) + 1 > 64:
                print(line)
                line = '    ' + word
            else:
                line += (' ' + word if line.strip() else word)
        if line.strip():
            print(line)
        print()


def analyze_letter_distribution(text):
    """Show letter frequencies in source text."""
    from collections import Counter
    letters = [c.lower() for c in text if c.isalpha()]
    counts = Counter(letters)
    total = sum(counts.values())

    print('  Letter frequencies in source:')
    # Show as bar chart
    max_count = max(counts.values())
    for char in 'etaoinshrdlu':
        if char in counts:
            bar_len = int(counts[char] / max_count * 25)
            bar = '█' * bar_len
            pct = counts[char] / total * 100
            print(f'    {char!r}  {bar:<26} {pct:.1f}%')


def bigram_heatmap(text, chars='etaoinsh'):
    """Show bigram frequencies as a small heatmap."""
    bigrams = defaultdict(lambda: defaultdict(int))
    text_lower = text.lower()
    for i in range(len(text_lower) - 1):
        a, b = text_lower[i], text_lower[i + 1]
        if a in chars and b in chars:
            bigrams[a][b] += 1

    max_val = max(
        bigrams[a][b]
        for a in chars for b in chars
        if bigrams[a][b] > 0
    ) if any(bigrams[a][b] for a in chars for b in chars) else 1

    shades = ' ░▒▓█'

    print(f'  Bigram heatmap (rows = first letter, cols = second):')
    print(f'    {"":>2}  ' + '  '.join(c for c in chars))
    for a in chars:
        row = f'    {a!r} '
        for b in chars:
            val = bigrams[a][b]
            idx = int(val / max_val * (len(shades) - 1))
            row += f' {shades[idx]} '
        print(row)
    print()
    print('  Darker = more common bigram.')
    print('  Blank = never occurs in this text.')


def main():
    print('Markov Chains and Text Generation\n')
    print('  Source: excerpts from Wittgenstein\'s Tractatus Logico-Philosophicus')
    print(f'  Length: {len(SOURCE_TEXT)} characters\n')

    print('  ─── LETTER DISTRIBUTION ───\n')
    analyze_letter_distribution(SOURCE_TEXT)

    print()
    print('  ─── BIGRAM HEATMAP ───\n')
    bigram_heatmap(SOURCE_TEXT)

    print('  ─── TRANSITION PROBABILITIES ───\n')
    show_transition_matrix(SOURCE_TEXT)

    print()
    print('  ─── GENERATED TEXT AT DIFFERENT ORDERS ───')
    print()
    print('  As order increases, the output becomes more "Wittgenstein-like":')
    print('  local structure is preserved, but meaning still escapes.')
    print()
    show_order_comparison(SOURCE_TEXT, length=250)

    print('  ─── WHAT THIS SHOWS ───')
    print()
    print('  Order 1: letter frequencies preserved; structure mostly absent')
    print('  Order 2: bigram frequencies match; starts to look like words')
    print('  Order 3: word structure emerging; not quite English')
    print('  Order 5: Wittgenstein-sounding; actual phrases appear verbatim')
    print('  Order 7: almost direct quotation; new combinations get rare')
    print()
    print('  The transition from "looks random" to "looks like language":')
    print('  - Order 1 is "letters in the right proportions"')
    print('  - Order 5 is "sentences that sound right but don\'t mean anything"')
    print('  - The gap between 5 and "actual language" is: meaning')
    print()
    print('  Shannon\'s observation (1948):')
    print('  A stream of characters with the right n-gram statistics')
    print('  has the surface of language without its depth.')
    print()
    print('  The n-gram model knows the skin of language.')
    print('  It does not know that "the Good" is a philosophical category,')
    print('  or that "the limits of my world" is melancholy,')
    print('  or why "whereof one cannot speak" has the weight that it has.')
    print()
    print('  What the chain produces is the description of how Wittgenstein sounds.')
    print('  The meaning is in the gap.')


if __name__ == '__main__':
    main()
