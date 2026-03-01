"""
Game Theory — The Mathematics of Strategic Interaction

A game, in the mathematical sense, consists of:
  - Players: agents making decisions
  - Strategies: what each player can choose
  - Payoffs: what each player receives for each outcome

The central solution concept: Nash equilibrium.
A strategy profile is a Nash equilibrium if no player can increase
their payoff by unilaterally changing their strategy, given what
everyone else is doing.

The Prisoner's Dilemma (Merrill Flood & Melvin Dresher, 1950):
  Two suspects, unable to communicate. Each can Cooperate (C) or Defect (D).

        Row player payoff, column player payoff:
               C          D
          C  (3, 3)    (0, 5)
          D  (5, 0)    (1, 1)

  Dominant strategy: always D (regardless of what other does, D is better)
  Nash equilibrium: (D, D) with payoffs (1, 1)
  But (C, C) gives (3, 3) — better for both.

  This is the tragedy: individually rational strategy leads to
  collectively suboptimal outcome. Models: arms races, overfishing,
  climate negotiation, advertising wars.

The Iterated Prisoner's Dilemma changes everything.
  Play repeatedly. Now reputation matters. You can reward cooperation
  and punish defection.

  Robert Axelrod's tournaments (1980, 1984): solicited strategies,
  ran round-robin of 100 rounds. Winner both times: Tit-for-Tat.
  Rules: cooperate first, then mirror opponent's previous move.

  Properties of successful strategies (Axelrod's analysis):
  - Nice: never defect first
  - Retaliatory: immediately punish defection
  - Forgiving: return to cooperation after punishment
  - Clear: simple enough for opponent to recognize and model

Evolutionary Game Theory:
  Instead of rational players, consider a population playing repeatedly.
  Strategies that earn more reproduce more. Which strategies survive?

  Evolutionarily Stable Strategy (ESS): a strategy that, once dominant
  in a population, cannot be invaded by a rare mutant.

  In iterated games with noise: TfT-like strategies can be ESS.
  In standard (non-iterated) PD: AllDefect is the ESS.
  The difference: whether the shadow of the future is long enough.
"""

import random
from collections import defaultdict

# Strategies encoded as integers: 0 = Cooperate, 1 = Defect
COOP, DEFT = 0, 1
MOVES = ['C', 'D']

# Payoff matrix: PD_PAYOFFS[row_move][col_move] = (row_payoff, col_payoff)
PD_PAYOFFS = [
    [(3, 3), (0, 5)],  # row=C: (C,C)=3,3 | (C,D)=0,5
    [(5, 0), (1, 1)],  # row=D: (D,C)=5,0 | (D,D)=1,1
]


# ─── Classic 2x2 Games ────────────────────────────────────────────────────────

GAMES = {
    "Prisoner's Dilemma": {
        "strategies": ["C (cooperate)", "D (defect)"],
        "payoffs": [[(3, 3), (0, 5)], [(5, 0), (1, 1)]],
        "note": "Dominant strategy: D. Nash eq: (D,D)=(1,1). Pareto opt: (C,C)=(3,3).",
    },
    "Stag Hunt": {
        "strategies": ["Stag", "Hare"],
        "payoffs": [[(4, 4), (0, 2)], [(2, 0), (2, 2)]],
        "note": "Two Nash eq: (Stag,Stag) and (Hare,Hare). Coordination problem.",
    },
    "Hawk-Dove": {
        "strategies": ["Hawk", "Dove"],
        "payoffs": [[(0, 0), (4, 1)], [(1, 4), (2, 2)]],
        "note": "Two pure Nash eq: (Hawk,Dove) and (Dove,Hawk), plus mixed. Models conflict.",
    },
}


def find_pure_nash(payoffs, n):
    """Find pure strategy Nash equilibria."""
    equilibria = []
    for i in range(n):
        for j in range(n):
            row_best = max(payoffs[k][j][0] for k in range(n))
            col_best = max(payoffs[i][k][1] for k in range(n))
            if payoffs[i][j][0] == row_best and payoffs[i][j][1] == col_best:
                equilibria.append((i, j))
    return equilibria


def display_game(name, game):
    strats = game["strategies"]
    payoffs = game["payoffs"]
    n = len(strats)
    w = 12

    print(f"  {name}")
    print(f"  {game['note']}")
    print()

    header = "  " + " " * 14
    for s in strats:
        label = s[:10]
        header += f"{label:^{w}}"
    print(header)

    for i, s_row in enumerate(strats):
        row = f"  {s_row[:12]:>12}  "
        for j in range(n):
            p = payoffs[i][j]
            cell = f"({p[0]},{p[1]})"
            row += f"{cell:^{w}}"
        print(row)

    equil = find_pure_nash(payoffs, n)
    if equil:
        eq_strs = [f"({strats[i][:6]}, {strats[j][:6]})" for i, j in equil]
        print(f"  Nash eq (pure): {', '.join(eq_strs)}")
    else:
        print("  Nash eq (pure): none — mixed strategy equilibrium exists")
    print()


# ─── Strategies for Iterated PD ───────────────────────────────────────────────

class Strategy:
    def __init__(self, name, fn):
        self.name = name
        self._fn = fn

    def move(self, my_history, opp_history):
        return self._fn(my_history, opp_history)


def _pavlov(my_h, op_h):
    if not my_h:
        return COOP
    last_pay = PD_PAYOFFS[my_h[-1]][op_h[-1]][0]
    return my_h[-1] if last_pay >= 3 else 1 - my_h[-1]


STRATEGIES = [
    Strategy("AllCooperate",  lambda m, o: COOP),
    Strategy("AllDefect",     lambda m, o: DEFT),
    Strategy("TitForTat",     lambda m, o: COOP if not o else o[-1]),
    Strategy("TfT-2Tats",     lambda m, o: DEFT if len(o) >= 2 and o[-1] == DEFT and o[-2] == DEFT else COOP),
    Strategy("Grudger",       lambda m, o: DEFT if DEFT in o else COOP),
    Strategy("Pavlov",        _pavlov),
    Strategy("Random",        lambda m, o: random.randint(0, 1)),
]


def play_match(a, b, n_rounds=100, seed=None):
    """Play a match between two strategies, return total scores."""
    if seed is not None:
        random.seed(seed)
    hist_a, hist_b = [], []
    score_a = score_b = 0
    for _ in range(n_rounds):
        ma = a.move(hist_a, hist_b)
        mb = b.move(hist_b, hist_a)
        pa, pb = PD_PAYOFFS[ma][mb]
        score_a += pa
        score_b += pb
        hist_a.append(ma)
        hist_b.append(mb)
    return score_a, score_b


def run_tournament(strategies, n_rounds=100):
    """Round-robin tournament. Each pair plays twice (A vs B and B vs A)."""
    random.seed(42)
    total_scores = defaultdict(int)
    match_count = defaultdict(int)

    for i in range(len(strategies)):
        for j in range(len(strategies)):
            a, b = strategies[i], strategies[j]
            sa, _ = play_match(a, b, n_rounds)
            total_scores[a.name] += sa
            match_count[a.name] += 1

    avg = {name: total_scores[name] / match_count[name]
           for name in total_scores}
    return avg


def show_match_detail(a, b, n_rounds=20):
    """Show move-by-move detail for a short match."""
    random.seed(7)
    hist_a, hist_b = [], []
    score_a = score_b = 0
    moves_a, moves_b = [], []
    for _ in range(n_rounds):
        ma = a.move(hist_a, hist_b)
        mb = b.move(hist_b, hist_a)
        pa, pb = PD_PAYOFFS[ma][mb]
        score_a += pa
        score_b += pb
        hist_a.append(ma)
        hist_b.append(mb)
        moves_a.append(MOVES[ma])
        moves_b.append(MOVES[mb])

    print(f"  {a.name:>14}:  {''.join(moves_a)}  total={score_a}")
    print(f"  {b.name:>14}:  {''.join(moves_b)}  total={score_b}")


# ─── Evolutionary Simulation ──────────────────────────────────────────────────

def evolutionary_simulation(strategies, n_gen=40, n_rounds=30):
    """
    Replicator dynamics: each strategy's share grows proportional
    to its fitness relative to mean population fitness.
    """
    random.seed(0)
    n = len(strategies)
    fracs = [1.0 / n] * n

    history = [fracs[:]]

    for _ in range(n_gen):
        # Average payoff per round for each strategy vs current population
        avg_pay = []
        for i in range(n):
            total = 0.0
            for j in range(n):
                if fracs[j] > 0:
                    sa, _ = play_match(strategies[i], strategies[j], n_rounds)
                    total += (sa / n_rounds) * fracs[j]
            avg_pay.append(total)

        mean_fit = sum(avg_pay[i] * fracs[i] for i in range(n))

        if mean_fit > 1e-9:
            new_fracs = [fracs[i] * avg_pay[i] / mean_fit for i in range(n)]
        else:
            new_fracs = fracs[:]

        total = sum(new_fracs)
        fracs = [f / total for f in new_fracs] if total > 1e-9 else fracs

        history.append(fracs[:])

    return history


def render_evolution(history, strategies, width=50):
    """Show strategy prevalence over generations as a stacked bar."""
    checkpoints = list(range(0, len(history), max(1, len(history) // 8)))
    if len(history) - 1 not in checkpoints:
        checkpoints.append(len(history) - 1)

    chars = '█▓▒░·○●◆'
    n = len(strategies)

    print(f"  {'Gen':>4}  {'Strategy shares (stacked bar)':^{width}}  dominant")
    print("  " + "─" * (width + 20))

    for gen in checkpoints:
        fracs = history[gen]
        bar = ''
        for i, f in enumerate(fracs):
            bar += chars[i % len(chars)] * int(f * width)
        bar = bar[:width].ljust(width)
        dominant = strategies[fracs.index(max(fracs))].name
        print(f"  {gen:>4}  {bar}  {dominant}")

    print()
    print("  Legend: " + "  ".join(f"{chars[i%len(chars)]}={s.name}" for i, s in enumerate(strategies)))
    print()
    final = history[-1]
    print("  Final distribution:")
    for i, s in enumerate(strategies):
        bar = '█' * int(final[i] * 40)
        print(f"  {s.name:>14}: {bar} {final[i]*100:5.1f}%")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("Game Theory — Strategic Interaction\n")
    print("  Two players. Known rules. What should you do?\n")

    # Classic games
    print("  ─── CLASSIC 2×2 GAMES ───\n")
    for name, game in GAMES.items():
        display_game(name, game)

    # Iterated PD: match details
    print("  ─── ITERATED PRISONER'S DILEMMA (20 rounds, sample) ───\n")
    pairs = [
        (STRATEGIES[0], STRATEGIES[1]),  # AllCooperate vs AllDefect
        (STRATEGIES[2], STRATEGIES[2]),  # TfT vs TfT
        (STRATEGIES[2], STRATEGIES[4]),  # TfT vs Grudger
        (STRATEGIES[1], STRATEGIES[5]),  # AllDefect vs Pavlov
    ]
    for a, b in pairs:
        label = f"{a.name} vs {b.name}"
        print(f"  {label}")
        show_match_detail(a, b, n_rounds=20)
        print()

    # Tournament
    print("  ─── ROUND-ROBIN TOURNAMENT (100 rounds each match) ───\n")
    avg_scores = run_tournament(STRATEGIES)
    ranked = sorted(avg_scores.items(), key=lambda x: -x[1])

    print(f"  {'Rank':>4}  {'Strategy':>14}  {'Avg score/match':>16}  {'Bar'}")
    print("  " + "─" * 60)
    max_score = ranked[0][1]
    for rank, (name, score) in enumerate(ranked, 1):
        bar = '█' * int(score / max_score * 30)
        print(f"  {rank:>4}  {name:>14}  {score:>16.1f}  {bar}")

    print()
    print("  Observation: Nice strategies (never first defect) cluster at top.")
    print("  TitForTat earns less than Grudger against AllDefect, but recovers")
    print("  from mistakes — its forgiveness makes it robust across opponents.\n")

    # Evolutionary dynamics (exclude Random for cleaner signal)
    print("  ─── EVOLUTIONARY DYNAMICS (replicator equation, 40 generations) ───\n")
    print("  Starting with equal shares. Fitness = average payoff vs population.")
    print("  Strategies that earn more grow; those that earn less shrink.\n")
    evo_strategies = STRATEGIES[:-1]  # exclude Random
    history = evolutionary_simulation(evo_strategies, n_gen=40)
    render_evolution(history, evo_strategies)

    print("  ─── WHAT GAME THEORY TEACHES ───\n")
    print("  1. Rational self-interest can produce collectively bad outcomes.")
    print("     (Prisoner's Dilemma: both defect, both get 1 instead of 3.)")
    print()
    print("  2. Repeated interaction changes the math.")
    print("     When tomorrow matters, cooperation can be sustained.")
    print("     'The shadow of the future' disciplines the present.")
    print()
    print("  3. Nice strategies can outcompete nasty ones in the long run.")
    print("     Not because they're nicer — because they're better.")
    print("     Cooperation is, under the right conditions, a winning strategy.")
    print()
    print("  4. Equilibrium is not optimum.")
    print("     A Nash equilibrium is stable, not necessarily good.")
    print("     Players can be trapped in outcomes they'd all prefer to escape.")
    print()
    print("  Limits: real agents aren't fully rational; games aren't always known;")
    print("  the payoff matrix is itself contested. The model abstracts away much.")
    print("  What survives: the basic insight that incentive structures matter.")
    print("  Change the rules, and the equilibrium changes.")


if __name__ == '__main__':
    main()
