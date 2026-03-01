"""
Bayesian Inference — Updating Beliefs with Evidence

Bayes' theorem:

  P(A | B) = P(B | A) · P(A) / P(B)

In words: the probability of A given B equals
  - the probability of B given A (the likelihood)
  - times the probability of A (the prior)
  - divided by the probability of B (the marginal)

P(A | B) = posterior
P(A) = prior
P(B | A) = likelihood
P(B) = normalizing constant = P(B|A)·P(A) + P(B|¬A)·P(¬A)

The theorem says: rational belief updating is multiplication.
Start with a prior. Observe evidence. Multiply by the likelihood.
Normalize. That's your new belief.

The hard part is human: we are systematically bad at this.
Specifically, we neglect the prior (base rate neglect).
We think the likelihood of evidence given hypothesis is the same
as the probability of hypothesis given evidence. It isn't.

The medical test example illustrates this starkly:
  - Test: 99% sensitivity (true positive rate), 99% specificity
  - Disease prevalence: 1 in 10,000
  - You test positive. What is the probability you have the disease?

Most people say ~99%. The correct answer is less than 1%.

Why? Because the disease is so rare (1 in 10,000 = 0.01%) that
even with a very accurate test, most positives are false positives.
Out of 10,000 people tested:
  - 1 has the disease → probably tests positive (99% sensitivity)
  - 9,999 don't → about 100 still test positive (1% false positive)
  So out of ~101 positive tests, only 1 is actually sick.

This is not a failure of the test. It's a feature of rare events.
Base rate neglect costs lives: over-treatment, over-diagnosis,
unnecessary anxiety, and waste.

Bayesian reasoning corrects this by making the prior explicit.
"""

import math


def bayes_update(prior, likelihood_pos, likelihood_neg):
    """
    Compute posterior given prior and likelihoods.
    prior: P(H) — prior probability of hypothesis
    likelihood_pos: P(E | H) — probability of evidence given H true
    likelihood_neg: P(E | ¬H) — probability of evidence given H false
    Returns: P(H | E) — posterior probability of H given evidence E
    """
    p_evidence = likelihood_pos * prior + likelihood_neg * (1 - prior)
    if p_evidence == 0:
        return 0
    return (likelihood_pos * prior) / p_evidence


def medical_test_demo():
    """Classic medical test example."""
    print('  ─── MEDICAL TEST EXAMPLE ───\n')

    cases = [
        ('Rare disease',     0.0001, 0.99, 0.01),  # 1 in 10,000, 99% accurate
        ('Common disease',   0.10,   0.95, 0.05),  # 10% prevalence, 95% accurate
        ('Very common',      0.50,   0.90, 0.10),  # 50% prevalence, 90% accurate
        ('Very rare, perfect', 0.0001, 0.999, 0.001),  # very accurate test
    ]

    for name, prev, sensitivity, false_pos_rate in cases:
        specificity = 1 - false_pos_rate
        posterior = bayes_update(prev, sensitivity, false_pos_rate)

        print(f'  {name}:')
        print(f'    Prevalence (prior):     {prev*100:>7.4f}%  (1 in {int(1/prev):,})')
        print(f'    Sensitivity (TPR):      {sensitivity*100:>7.1f}%  (P(+ | sick))')
        print(f'    False positive rate:    {false_pos_rate*100:>7.1f}%  (P(+ | healthy))')
        print(f'    Specificity:            {specificity*100:>7.1f}%  (P(- | healthy))')
        print(f'    POSTERIOR P(sick | +):  {posterior*100:>7.3f}%')

        # Explain in natural frequencies
        n = 100000
        sick = int(n * prev)
        healthy = n - sick
        true_pos = int(sick * sensitivity)
        false_pos = int(healthy * false_pos_rate)
        total_pos = true_pos + false_pos

        print(f'')
        print(f'    Natural frequencies (per {n:,} people):')
        print(f'      Sick: {sick:>6}  → {true_pos:>5} test positive  (true positives)')
        print(f'    Healthy: {healthy:>6}  → {false_pos:>5} test positive  (false positives)')
        print(f'    Total positive tests: {total_pos}')
        if total_pos > 0:
            actual_pct = true_pos / total_pos * 100
            print(f'    Fraction that are actually sick: {true_pos}/{total_pos} = {actual_pct:.1f}%')
        print()


def sequential_updating():
    """Show belief updating as evidence accumulates."""
    print('  ─── SEQUENTIAL BAYESIAN UPDATING ───\n')
    print('  Start with a prior. Update with each piece of evidence.')
    print('  Each posterior becomes the prior for the next update.')
    print()

    # Example: trying to determine if a coin is fair or biased
    # Hypotheses: H = coin is biased (70% heads), ¬H = coin is fair (50% heads)
    prior = 0.3  # prior belief that coin is biased
    outcomes = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]

    p_heads_if_biased = 0.7
    p_heads_if_fair = 0.5

    print(f'  Hypothesis: coin is biased (70% heads) vs fair (50% heads)')
    print(f'  Prior P(biased) = {prior}')
    print()
    print(f'  {"Step":>5}  {"Outcome":>7}  {"P(biased)":>10}  {"Belief bar"}')
    print('  ' + '-' * 60)

    bar_width = 30
    belief = prior
    total_heads = 0
    total_tosses = 0

    print(f'  {"prior":>5}  {"":>7}  {belief:>10.4f}  ' + '█' * int(belief * bar_width) + '░' * (bar_width - int(belief * bar_width)))

    for i, outcome in enumerate(outcomes):
        total_tosses += 1
        if outcome == 1:
            total_heads += 1
            # Heads: update with P(heads | H) vs P(heads | ¬H)
            belief = bayes_update(belief, p_heads_if_biased, p_heads_if_fair)
            symbol = 'H (heads)'
        else:
            # Tails: update with P(tails | H) vs P(tails | ¬H)
            belief = bayes_update(belief, 1 - p_heads_if_biased, 1 - p_heads_if_fair)
            symbol = 'T (tails)'

        bar_len = int(belief * bar_width)
        bar = '█' * bar_len + '░' * (bar_width - bar_len)
        print(f'  {i+1:>5}  {symbol:>9}  {belief:>10.4f}  {bar}')

    print()
    print(f'  After {total_tosses} tosses ({total_heads} heads, {total_tosses-total_heads} tails):')
    print(f'  P(biased) = {belief:.4f}')
    emp_rate = total_heads / total_tosses
    print(f'  Empirical rate: {total_heads}/{total_tosses} = {emp_rate:.3f} (coin was biased toward {p_heads_if_biased})')
    print()
    print('  The Bayesian updates the belief continuously.')
    print('  No single piece of evidence decides; all evidence accumulates.')


def prior_sensitivity():
    """Show how different priors converge with enough evidence."""
    print('  ─── PRIOR SENSITIVITY: DO PRIORS MATTER? ───\n')
    print('  Different starting beliefs, same evidence stream.')
    print('  Do they converge? How fast?\n')

    # Biased coin generating data
    true_bias = 0.65
    n_flips = 100
    import random
    random.seed(123)
    flips = [1 if random.random() < true_bias else 0 for _ in range(n_flips)]

    priors = [0.1, 0.3, 0.5, 0.7, 0.9]
    beliefs = {p: p for p in priors}

    p_heads_biased = 0.65
    p_heads_fair = 0.50

    # Checkpoints to display
    checkpoints = [0, 5, 10, 20, 50, 100]

    print(f'  Priors:  ' + '  '.join(f'{p:.1f}' for p in priors))
    print(f'  True bias: {true_bias}')
    print()

    bar_w = 15
    for cp_idx, cp in enumerate(checkpoints):
        # Update to this checkpoint
        if cp_idx > 0:
            prev_cp = checkpoints[cp_idx - 1]
            for flip in flips[prev_cp:cp]:
                for p in priors:
                    if flip == 1:
                        beliefs[p] = bayes_update(beliefs[p], p_heads_biased, p_heads_fair)
                    else:
                        beliefs[p] = bayes_update(beliefs[p], 1 - p_heads_biased, 1 - p_heads_fair)

        row = f'  n={cp:>3}:  '
        for p in priors:
            b = beliefs[p]
            row += f'{b:>5.3f}  '
        print(row)

    print()
    print(f'  With enough evidence, different priors converge to the same posterior.')
    print(f'  The prior matters less as n grows. Evidence dominates in the limit.')
    print(f'  (This is why science works even with different prior beliefs.)')


def main():
    print('Bayesian Inference — Updating Beliefs with Evidence\n')
    print('  P(H|E) = P(E|H) · P(H) / P(E)')
    print('  posterior = likelihood × prior / normalizer\n')

    medical_test_demo()

    sequential_updating()

    print()
    prior_sensitivity()

    print()
    print('  ─── KEY INSIGHT ───\n')
    print('  The medical test problem shows that:')
    print('  P(positive test | disease) ≠ P(disease | positive test)')
    print()
    print('  These are different questions. The test\'s sensitivity answers the first.')
    print('  You want the answer to the second.')
    print()
    print('  Bayes\' theorem provides the conversion.')
    print('  The conversion requires knowing the base rate (prevalence).')
    print('  Without the base rate, you cannot convert the first into the second.')
    print()
    print('  Human intuition tends to equate them.')
    print('  This error — base rate neglect — is systematic and well-documented.')
    print('  It affects medical diagnosis, criminal trials, security screening,')
    print('  and everyday belief formation.')
    print()
    print('  The Bayesian framework is not a claim about the world.')
    print('  It is a constraint on rational belief: your posterior must be')
    print('  your prior times the likelihood, normalized.')
    print('  Everything else is optional. That part is not.')


if __name__ == '__main__':
    main()
