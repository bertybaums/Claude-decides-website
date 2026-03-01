// Gaussian Primes — primes in the complex integers ℤ[i]
// A Gaussian integer a+bi is prime if it cannot be factored in ℤ[i].
// Gaussian primes: p if either:
//   1. p is a real prime ≡ 3 (mod 4) (stays prime in ℤ[i])
//   2. a²+b² is a (real) prime
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const AMBER = '#c8922a';
const BG = '#0f0f0f';
const WHITE = '#e8e4dc';
const DIMTEXT = '#6b6560';

const W = canvas.width;
const H = canvas.height;

// Sieve of Eratosthenes up to N
function sieve(N) {
  const isPrime = new Uint8Array(N + 1).fill(1);
  isPrime[0] = isPrime[1] = 0;
  for (let i = 2; i * i <= N; i++) {
    if (isPrime[i]) {
      for (let j = i * i; j <= N; j += i) isPrime[j] = 0;
    }
  }
  return isPrime;
}

const MAX_NORM = 2000;
const realPrimes = sieve(MAX_NORM);

function isGaussianPrime(a, b) {
  if (a === 0 && b === 0) return false;
  if (b === 0) {
    const aa = Math.abs(a);
    return realPrimes[aa] && aa % 4 === 3;
  }
  if (a === 0) {
    const bb = Math.abs(b);
    return realPrimes[bb] && bb % 4 === 3;
  }
  const norm = a * a + b * b;
  return norm <= MAX_NORM && realPrimes[norm] === 1;
}

const RANGE = 28; // show -RANGE..RANGE in each axis

// Pre-compute all Gaussian primes in range
const gaussianPrimes = [];
for (let a = -RANGE; a <= RANGE; a++) {
  for (let b = -RANGE; b <= RANGE; b++) {
    if (isGaussianPrime(a, b)) {
      const norm = a * a + b * b;
      gaussianPrimes.push({ a, b, norm });
    }
  }
}

// Layout: leave margin for labels
const MARGIN = 50;
const PLOT_X = MARGIN;
const PLOT_Y = MARGIN;
const PLOT_W = W - 2 * MARGIN;
const PLOT_H = H - 2 * MARGIN - 40;

function toScreen(a, b) {
  const x = PLOT_X + ((a + RANGE) / (2 * RANGE)) * PLOT_W;
  const y = PLOT_Y + ((RANGE - b) / (2 * RANGE)) * PLOT_H;
  return [x, y];
}

// Color by norm: dim (close) to bright (far), tinted amber→white
function normColor(norm, maxNorm) {
  const t = Math.sqrt(norm / maxNorm);
  const r = Math.round(200 + 55 * t);
  const g = Math.round(146 + (220 - 146) * t);
  const b = Math.round(42 + (200 - 42) * t);
  return `rgb(${r},${g},${b})`;
}

const maxNorm = RANGE * RANGE * 2;
let revealIdx = 0;
let running = true;
let phaseTimeout = null;

// Pre-sort by norm for reveal animation
gaussianPrimes.sort((x, y) => x.norm - y.norm);

function drawAxes() {
  ctx.strokeStyle = '#2a2520';
  ctx.lineWidth = 1;

  // Grid lines
  for (let v = -RANGE; v <= RANGE; v += 4) {
    const [sx] = toScreen(v, 0);
    const [, sy] = toScreen(0, v);
    ctx.beginPath();
    ctx.moveTo(sx, PLOT_Y);
    ctx.lineTo(sx, PLOT_Y + PLOT_H);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(PLOT_X, sy);
    ctx.lineTo(PLOT_X + PLOT_W, sy);
    ctx.stroke();
  }

  // Axes
  ctx.strokeStyle = '#444';
  ctx.lineWidth = 1.5;
  const [ox, oy] = toScreen(0, 0);
  ctx.beginPath();
  ctx.moveTo(PLOT_X, oy);
  ctx.lineTo(PLOT_X + PLOT_W, oy);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(ox, PLOT_Y);
  ctx.lineTo(ox, PLOT_Y + PLOT_H);
  ctx.stroke();

  // Axis labels
  ctx.fillStyle = DIMTEXT;
  ctx.font = '11px monospace';
  ctx.fillText('Re', PLOT_X + PLOT_W + 4, oy + 4);
  ctx.fillText('Im', ox + 4, PLOT_Y - 6);

  // Tick labels
  for (let v = -RANGE; v <= RANGE; v += 8) {
    if (v === 0) continue;
    const [sx] = toScreen(v, 0);
    ctx.fillStyle = DIMTEXT;
    ctx.fillText(String(v), sx - 6, oy + 16);
    const [, sy] = toScreen(0, v);
    ctx.fillText(String(v), ox + 4, sy + 4);
  }
}

function draw(n) {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  // Title
  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText('Gaussian Primes  ℤ[i]', MARGIN, 30);

  drawAxes();

  // Draw revealed primes
  const dotR = Math.max(2.5, PLOT_W / (2 * RANGE) * 0.38);

  for (let i = 0; i < Math.min(n, gaussianPrimes.length); i++) {
    const { a, b, norm } = gaussianPrimes[i];
    const [sx, sy] = toScreen(a, b);
    const color = normColor(norm, maxNorm);

    ctx.beginPath();
    ctx.arc(sx, sy, dotR, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();
  }

  // Counters
  const shown = Math.min(n, gaussianPrimes.length);
  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  ctx.fillText(`${shown} of ${gaussianPrimes.length} Gaussian primes in |a|,|b| ≤ ${RANGE}`, MARGIN, H - 16);

  // Legend
  ctx.fillStyle = AMBER;
  ctx.font = '11px monospace';
  ctx.fillText('near origin', W - 180, 30);
  ctx.fillStyle = '#e8e4dc';
  ctx.fillText('→ far from origin', W - 180, 46);

  // Fourfold symmetry note
  ctx.fillStyle = DIMTEXT;
  ctx.font = '11px monospace';
  ctx.fillText('4-fold symmetric: ×i rotates 90°', MARGIN, H - 2);
}

function reveal() {
  if (!running) return;
  if (revealIdx >= gaussianPrimes.length) {
    window.__setStatus && window.__setStatus(`${gaussianPrimes.length} Gaussian primes — fourfold symmetric — click to restart`);
    return;
  }
  revealIdx = Math.min(revealIdx + 6, gaussianPrimes.length);
  draw(revealIdx);
  const shown = Math.min(revealIdx, gaussianPrimes.length);
  window.__setStatus && window.__setStatus(`${shown} Gaussian primes — complex plane — click to restart`);
  const delay = revealIdx < 50 ? 60 : revealIdx < 200 ? 30 : 12;
  phaseTimeout = setTimeout(reveal, delay);
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  if (phaseTimeout) clearTimeout(phaseTimeout);
  revealIdx = 0;
  draw(0);
  window.__setStatus && window.__setStatus('Gaussian primes in the complex plane — click to restart');
  phaseTimeout = setTimeout(reveal, 300);
}

window.__programRestart = init;
init();
