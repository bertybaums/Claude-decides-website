export interface ProgramMeta {
  name: string;
  title: string;
  category: string;
  description: string; // HTML ok, used in page
  pythonFile: string;
}

export const programs: ProgramMeta[] = [
  // 1D Cellular Automata
  {
    name: 'rule30',
    title: 'Rule 30',
    category: '1D Cellular Automaton',
    description: 'Wolfram discovered that this extremely simple rule produces output that is, as far as anyone can tell, genuinely random — statistically indistinguishable from randomness by every test we have. The center column of Rule 30 was used as a random number generator in Mathematica for years. <em>One cell. One rule. Incompressible output.</em>',
    pythonFile: 'rule30.py',
  },
  {
    name: 'rule90',
    title: 'Rule 90',
    category: '1D Cellular Automaton',
    description: 'Rule 90 is the cellular automaton equivalent of Pascal\'s triangle modulo 2 — it produces the Sierpiński triangle, one of the first fractals ever described. Every row is determined by a simple XOR of its neighbors, yet the pattern is self-similar at every scale. <em>A fractal hiding inside an arithmetic rule.</em>',
    pythonFile: 'rule90.py',
  },
  {
    name: 'rule110',
    title: 'Rule 110',
    category: '1D Cellular Automaton',
    description: 'Rule 110 is proven Turing-complete — meaning it can compute anything a computer can compute. It looks like organized chaos: regular regions punctuated by complex interactions. Matthew Cook proved its universality in 2004. <em>Turing completeness from a rule you can write on a napkin.</em>',
    pythonFile: 'rule110.py',
  },
  // 2D Cellular Automata
  {
    name: 'conway',
    title: "Conway's Game of Life",
    category: '2D Cellular Automaton',
    description: 'Four rules about neighbors. That\'s all. From these four rules: gliders, oscillators, spaceships, patterns that grow unboundedly, patterns that compute. Turing-complete. This animation runs the Gosper Glider Gun — the first known finite pattern with unbounded growth, discovered in 1970. <em>From four rules about neighbors: computation itself.</em>',
    pythonFile: 'conway.py',
  },
  {
    name: 'brians_brain',
    title: "Brian's Brain",
    category: '2D Cellular Automaton',
    description: 'A three-state automaton where every dying cell briefly glows before going dark. It produces a continuous stream of gliders — nearly every pattern eventually dissolves into a swarm of moving forms. Brian Silverman invented it in the 1990s. <em>A world where everything that lives becomes a traveler.</em>',
    pythonFile: 'brians_brain.py',
  },
  {
    name: 'wireworld',
    title: 'Wireworld',
    category: '2D Cellular Automaton',
    description: 'Wireworld simulates electron flow through wires. Electron heads, tails, and wire create signals that can be combined into logic gates — and from logic gates, entire computers have been built inside Wireworld. This demo shows electron signals flowing through a loop. <em>A computer inside a rule about colored squares.</em>',
    pythonFile: 'wireworld.py',
  },
  {
    name: 'highlife',
    title: 'HighLife',
    category: '2D Cellular Automaton',
    description: 'HighLife adds one rule to Conway\'s Life: a dead cell with exactly 6 neighbors also becomes alive. This tiny change produces "replicators" — patterns that copy themselves across the grid — which Life famously lacks. <em>One extra rule produces self-replication.</em>',
    pythonFile: 'highlife.py',
  },
  {
    name: 'seeds',
    title: 'Seeds',
    category: '2D Cellular Automaton',
    description: 'In Seeds, a cell becomes alive only if it has exactly 2 neighbors, and every living cell immediately dies. No cell survives more than one generation — yet from random seeds, explosive growth patterns form, spread, and interact. <em>Life without persistence, yet structure without memory.</em>',
    pythonFile: 'seeds.py',
  },
  {
    name: 'daynight',
    title: 'Day & Night',
    category: '2D Cellular Automaton',
    description: 'Day & Night has a beautiful symmetry: the same rule applies to living and dead cells alike. A cell survives if it has 3, 4, 6, 7, or 8 neighbors — and the same counts apply to birth. Inverting the grid produces the same behavior. <em>A rule symmetric under the exchange of life and death.</em>',
    pythonFile: 'daynight.py',
  },
  {
    name: 'langtons_ant',
    title: "Langton's Ant",
    category: '2D Cellular Automaton',
    description: 'Two rules: on a white square, turn right, flip the square, move forward. On a black square, turn left, flip the square, move forward. For ~10,000 steps the ant traces chaotic patterns — then suddenly builds a "highway," an infinitely repeating diagonal corridor. <em>Chaos that spontaneously organizes itself.</em>',
    pythonFile: 'langtons_ant.py',
  },
  // Fractals
  {
    name: 'mandelbrot',
    title: 'Mandelbrot Set',
    category: 'Fractal',
    description: 'The Mandelbrot set contains every possible Julia set as a cross-section. It has infinite perimeter but finite area. Zoom in anywhere on its boundary and find new complexity forever — the description (one equation) is finite; the object is not. <em>Finite rule. Infinite boundary.</em>',
    pythonFile: 'mandelbrot.py',
  },
  {
    name: 'julia',
    title: 'Julia Sets',
    category: 'Fractal',
    description: 'Each point in the Mandelbrot set corresponds to a Julia set. Connected Mandelbrot points produce connected Julia sets; disconnected points produce dust. This visualization cycles through parameters, showing how the fractal shape morphs continuously. <em>A family of fractals parameterized by a single complex number.</em>',
    pythonFile: 'julia.py',
  },
  {
    name: 'newton',
    title: 'Newton Fractal',
    category: 'Fractal',
    description: 'Newton\'s method for finding roots of a polynomial — a calculus algorithm — produces fractal boundaries between basins of attraction. The boundaries between which root you converge to are infinitely complex. <em>A calculus algorithm, visualized, becomes a fractal.</em>',
    pythonFile: 'newton.py',
  },
  // Attractors
  {
    name: 'lorenz',
    title: 'Lorenz Attractor',
    category: 'Attractor',
    description: 'Edward Lorenz simplified a weather model to three equations. The resulting trajectory never repeats, never escapes, and is exquisitely sensitive to initial conditions — the butterfly effect. This is the shape of unpredictability. <em>Three equations. The shape of weather\'s unpredictability.</em>',
    pythonFile: 'lorenz.py',
  },
  {
    name: 'logistic',
    title: 'Logistic Map (Bifurcation Diagram)',
    category: 'Attractor',
    description: 'One equation: x → r·x·(1−x). As r increases from 2 to 4, the system doubles its period — 1 fixed point, 2, 4, 8 — then suddenly goes chaotic. The bifurcation diagram makes this transition visible. It appears in population dynamics, electronics, and fluid mechanics. <em>The onset of chaos, made visible.</em>',
    pythonFile: 'logistic.py',
  },
  // Botanical/Spiral
  {
    name: 'fern',
    title: 'Barnsley Fern',
    category: 'Fractal',
    description: 'A fern, drawn by four simple affine transformations applied randomly. The shape emerges from probability — no explicit geometry is specified, only rules for where points tend to land. Michael Barnsley showed that all of nature\'s fractal forms could be generated this way. <em>A fern as a probability distribution.</em>',
    pythonFile: 'fern.py',
  },
  {
    name: 'lsystem',
    title: 'L-Systems',
    category: 'Botanical',
    description: 'Aristid Lindenmayer invented L-systems to model plant growth: start with a symbol, apply rewriting rules repeatedly, interpret the result as drawing instructions. Branching trees, snowflakes, and space-filling curves all emerge from a handful of rules. <em>Growth as rewriting.</em>',
    pythonFile: 'lsystem.py',
  },
  {
    name: 'sunflower',
    title: 'Sunflower Spiral',
    category: 'Botanical',
    description: 'Sunflowers pack seeds at the golden angle (≈137.5°) — the angle most irrational, most avoiding fractions, leaving no direction more favored. The result is Fibonacci spirals in both directions. <em>The golden ratio as optimal packing.</em>',
    pythonFile: 'sunflower.py',
  },
  // Number Theory
  {
    name: 'collatz',
    title: 'Collatz Conjecture',
    category: 'Number Theory',
    description: 'Take any positive integer. If even, halve it. If odd, multiply by 3 and add 1. Repeat. The conjecture: you always reach 1. Verified for numbers up to 2⁶⁸. Not proven. Erdős said "mathematics is not yet ready for such problems." <em>A problem any child can state. No one can prove.</em>',
    pythonFile: 'collatz.py',
  },
  {
    name: 'ulam',
    title: 'Ulam Spiral',
    category: 'Number Theory',
    description: 'Write the integers in a spiral. Highlight the primes. Diagonal lines appear — patterns that number theory doesn\'t fully explain. Stanisław Ulam discovered this while doodling in a boring meeting in 1963. <em>Primes, arranged in a spiral, reveal diagonal structure.</em>',
    pythonFile: 'ulam.py',
  },
  {
    name: 'pascal',
    title: "Pascal's Triangle mod 2",
    category: 'Number Theory',
    description: "Pascal's triangle, where each entry is the binomial coefficient mod 2 (0 or 1), produces Sierpiński's triangle — the same fractal as Rule 90. Number theory and cellular automata converge on the same shape. <em>Two completely different rules, one fractal.</em>",
    pythonFile: 'pascal.py',
  },
  {
    name: 'primegaps',
    title: 'Prime Gaps',
    category: 'Number Theory',
    description: 'The gaps between consecutive primes grow on average (prime number theorem) but fluctuate irregularly. Twin primes (gap = 2) appear infinitely often, conjecturally. The largest known prime gaps cluster in predictable places. <em>The irregular rhythm of the primes.</em>',
    pythonFile: 'primegaps.py',
  },
  {
    name: 'sieve',
    title: 'Sieve of Eratosthenes',
    category: 'Number Theory',
    description: 'The oldest known algorithm for finding primes: start with all numbers, cross off multiples of each prime in turn. Animated, you can watch the sieve work — the primes are what survive the elimination. <em>The primes as survivors.</em>',
    pythonFile: 'sieve.py',
  },
  {
    name: 'phi',
    title: 'Golden Ratio Convergence',
    category: 'Number Theory',
    description: 'The golden ratio φ = (1+√5)/2 ≈ 1.618 is the limit of consecutive Fibonacci numbers. It appears in plant phyllotaxis, art, and architecture — but most remarkably it is the "most irrational" number, the hardest to approximate by fractions. <em>The number that resists all rational approximation.</em>',
    pythonFile: 'phi.py',
  },
  {
    name: 'harmonic',
    title: 'Harmonic Series',
    category: 'Mathematical',
    description: 'The harmonic series 1 + 1/2 + 1/3 + 1/4 + ⋯ diverges — it grows without bound — but so slowly that a computer counting one term per nanosecond would need longer than the age of the universe to reach 60. <em>Divergence so slow it looks like convergence.</em>',
    pythonFile: 'harmonic.py',
  },
  {
    name: 'overtones',
    title: 'Harmonic Overtones',
    category: 'Mathematical',
    description: 'The overtone series — 1, 2, 3, 4, 5... times a fundamental frequency — is the physics of musical harmony. The intervals between overtones form the just intonation scale. Equal temperament is a compromise that makes all keys slightly out of tune with these ratios. <em>The mathematics inside musical tuning.</em>',
    pythonFile: 'overtones.py',
  },
  {
    name: 'euler_circle',
    title: "Euler's Identity Visualized",
    category: 'Mathematical',
    description: "Euler's formula e^(iθ) = cos θ + i sin θ traces a circle in the complex plane. As θ sweeps from 0 to 2π, the point travels once around the unit circle, passing through 1, i, −1, −i — the most fundamental values in mathematics meeting in one orbit. <em>Five fundamental constants, one circle.</em>",
    pythonFile: 'euler_circle.py',
  },
  // Statistical
  {
    name: 'central_limit',
    title: 'Central Limit Theorem',
    category: 'Statistical',
    description: 'Add enough independent random variables — from any distribution — and the sum approaches a normal distribution. This is why the bell curve appears everywhere: it is the attractor of repeated averaging. <em>The bell curve as inevitable convergence.</em>',
    pythonFile: 'central_limit.py',
  },
  {
    name: 'monte_carlo',
    title: 'Monte Carlo π',
    category: 'Statistical',
    description: 'Throw random darts at a square containing a circle. The fraction that land inside the circle approximates π/4. With enough darts, π emerges from randomness — a famous demonstration that computation and probability are deeply connected. <em>π computed by throwing darts.</em>',
    pythonFile: 'monte_carlo.py',
  },
  {
    name: 'random_walk',
    title: 'Random Walk',
    category: 'Statistical',
    description: 'A particle moves one step in a random direction at each tick. In 1D and 2D it returns to its origin with probability 1. In 3D it escapes forever with probability ≈0.66. This threshold — recurrence in low dimensions, transience in high — has deep implications for physics and probability. <em>Return is certain in two dimensions. In three, you wander forever.</em>',
    pythonFile: 'random_walk.py',
  },
];

export const programsByName = Object.fromEntries(programs.map(p => [p.name, p]));
