"""
Genetic Algorithm — Evolution in Miniature

A genetic algorithm solves optimization problems by mimicking
natural selection:

  1. Start with a random population of candidate solutions
  2. Evaluate fitness (how good is each candidate?)
  3. Select the fittest individuals to reproduce
  4. Create offspring via crossover (mix two parents) and mutation
  5. Replace the old generation with offspring
  6. Repeat until a solution is found or convergence

This demonstrates the algorithm evolving a target phrase.
Each individual is a string; fitness = number of matching characters.

Unlike a direct search, the algorithm never "knows" the target.
It only knows how close each candidate is.
Selection pressure + variation does the rest.

Key observations:
  - Early generations: random soup, fitness near 0
  - Middle: rapid improvement as fit patterns accumulate
  - Late: convergence, fine-tuning

The algorithm demonstrates that directed search requires only:
  1. A way to measure fitness (closeness to solution)
  2. A mechanism for variation (mutation)
  3. Differential reproduction (selection pressure)

No foresight. No goal. No designer. Just: the better ones
have more offspring. Over generations, this finds solutions
that direct search would take vastly longer to find.

This is evolution's core insight translated to computation.
"""

import random
import string

POPULATION = 200
MUTATION_RATE = 0.015
TARGET = "the gap between description and thing"
CHARS = string.ascii_lowercase + ' '
MAX_GENERATIONS = 2000
REPORT_EVERY = 50

random.seed(7)


def random_individual(length):
    return ''.join(random.choice(CHARS) for _ in range(length))


def fitness(individual, target):
    return sum(a == b for a, b in zip(individual, target))


def select_parent(population, fitnesses):
    """Tournament selection: pick two, return fitter."""
    a, b = random.sample(range(len(population)), 2)
    return population[a] if fitnesses[a] >= fitnesses[b] else population[b]


def crossover(p1, p2):
    """Single-point crossover."""
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:]


def mutate(individual, rate):
    return ''.join(
        random.choice(CHARS) if random.random() < rate else c
        for c in individual
    )


def highlight_match(individual, target):
    """Show matching characters as uppercase, mismatches as ·"""
    result = []
    for a, b in zip(individual, target):
        if a == b:
            result.append(a.upper())
        else:
            result.append('·')
    return ''.join(result)


def run():
    n = len(TARGET)
    population = [random_individual(n) for _ in range(POPULATION)]

    history = []

    for gen in range(MAX_GENERATIONS):
        fitnesses = [fitness(ind, TARGET) for ind in population]
        best_idx = max(range(len(fitnesses)), key=lambda i: fitnesses[i])
        best = population[best_idx]
        best_fit = fitnesses[best_idx]

        if gen % REPORT_EVERY == 0 or best_fit == n:
            history.append((gen, best_fit, best))

        if best_fit == n:
            break

        # New generation
        new_pop = [best]  # Elitism: keep best
        while len(new_pop) < POPULATION:
            p1 = select_parent(population, fitnesses)
            p2 = select_parent(population, fitnesses)
            child = crossover(p1, p2)
            child = mutate(child, MUTATION_RATE)
            new_pop.append(child)

        population = new_pop

    return history, gen


def main():
    print('Genetic Algorithm — Evolution in Miniature\n')
    print(f'  Target:      "{TARGET}"')
    print(f'  Population:  {POPULATION}   Mutation rate: {MUTATION_RATE:.1%}')
    print(f'  Alphabet:    {len(CHARS)} characters (a–z + space)')
    print()
    print('  UPPERCASE = correct character   · = wrong character')
    print()
    print('  Generation   Fitness   Best individual')
    print('  ' + '─' * 70)

    history, final_gen = run()

    for gen, fit, individual in history:
        highlighted = highlight_match(individual, TARGET)
        bar = '█' * fit + '░' * (len(TARGET) - fit)
        pct = 100 * fit // len(TARGET)
        print(f'  Gen {gen:>5}   {fit:>2}/{len(TARGET)}={pct:>3}%  {highlighted}')

    print()
    print(f'  Solved in {final_gen} generations.')
    print()

    # Show random-search comparison
    n = len(TARGET)
    n_chars = len(CHARS)
    random_expected = n_chars ** n
    print(f'  Random search would need ~{n_chars}^{n} = 10^{n * 0.85:.0f} trials on average.')
    print(f'  Genetic algorithm: {final_gen} × {POPULATION} = {final_gen * POPULATION} evaluations.')
    print()
    print('  The algorithm never saw the target.')
    print('  It only knew, for each candidate, how many characters matched.')
    print()
    print('  Selection pressure + variation + time.')
    print('  No foresight. No designer. No goal.')
    print('  The better candidates had more offspring.')
    print('  Over generations, the solution assembled itself.')
    print()
    print('  This is how the eye was built.')
    print('  Slower. Much slower. Otherwise identical in structure.')


if __name__ == '__main__':
    main()
