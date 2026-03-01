// Euler's Totient Function φ(n) — scatter plot for n = 1..500
// φ(n) counts integers from 1..n that share no common factor with n
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const AMBER = '#c8922a';
const BG = '#0f0f0f';
const WHITE = '#e8e4dc';
const DIMTEXT = '#6b6560';

const W = canvas.width;
const H = canvas.height;

const MAX_N = 500;

// Compute totient via sieve
function totientSieve(max) {
  const phi = new Int32Array(max + 1);
  for (let i = 0; i <= max; i++) phi[i] = i;
  for (let i = 2; i <= max; i++) {
    if (phi[i] === i) { // i is prime
      for (let j = i; j <= max; j += i) {
        phi[j] -= Math.floor(phi[j] / i);
      }
    }
  }
  return phi;
}

function isPrime(n, phi) {
  return n > 1 && phi[n] === n - 1;
}

const phi = totientSieve(MAX_N);

// Layout
const MARGIN_L = 60;
const MARGIN_R = 30;
const MARGIN_T = 70;
const MARGIN_B = 80;
const PLOT_X = MARGIN_L;
const PLOT_Y = MARGIN_T;
const PLOT_W = W - MARGIN_L - MARGIN_R;
const PLOT_H = H - MARGIN_T - MARGIN_B - 40;

// Ratio line area
const RATIO_Y = PLOT_Y + PLOT_H + 50;
const RATIO_H = 60;

function toScreen(n, val) {
  const x = PLOT_X + ((n - 1) / (MAX_N - 1)) * PLOT_W;
  const y = PLOT_Y + PLOT_H - (val / MAX_N) * PLOT_H;
  return [x, y];
}

// 6/π² ≈ 0.6079 — density of coprime pairs
const SIX_PI2 = 6 / (Math.PI * Math.PI);

let revealN = 1;
let running = true;
let phaseTimeout = null;

// Ratio history φ(n)/n for sparkline
const ratioHistory = [];

function drawAxes() {
  // Grid lines
  ctx.strokeStyle = '#1a1a1a';
  ctx.lineWidth = 1;
  for (let v = 0; v <= MAX_N; v += 100) {
    const [, sy] = toScreen(1, v);
    ctx.beginPath();
    ctx.moveTo(PLOT_X, sy);
    ctx.lineTo(PLOT_X + PLOT_W, sy);
    ctx.stroke();
    ctx.fillStyle = DIMTEXT;
    ctx.font = '10px monospace';
    ctx.fillText(String(v), PLOT_X - 30, sy + 4);
  }
  for (let n = 0; n <= MAX_N; n += 100) {
    const [sx] = toScreen(n || 1, 0);
    ctx.beginPath();
    ctx.moveTo(sx, PLOT_Y);
    ctx.lineTo(sx, PLOT_Y + PLOT_H);
    ctx.stroke();
    ctx.fillStyle = DIMTEXT;
    ctx.font = '10px monospace';
    ctx.fillText(String(n), sx - 10, PLOT_Y + PLOT_H + 16);
  }

  // Axes
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(PLOT_X, PLOT_Y);
  ctx.lineTo(PLOT_X, PLOT_Y + PLOT_H);
  ctx.lineTo(PLOT_X + PLOT_W, PLOT_Y + PLOT_H);
  ctx.stroke();

  // y = n line (max possible)
  ctx.strokeStyle = '#222';
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 4]);
  ctx.beginPath();
  const [x1, y1] = toScreen(1, 1);
  const [x2, y2] = toScreen(MAX_N, MAX_N);
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  ctx.setLineDash([]);

  // φ(n)/n → 6/π² line
  const avgY = PLOT_Y + PLOT_H - SIX_PI2 * PLOT_H;
  ctx.strokeStyle = '#33554a';
  ctx.lineWidth = 1;
  ctx.setLineDash([2, 4]);
  ctx.beginPath();
  ctx.moveTo(PLOT_X, avgY);
  ctx.lineTo(PLOT_X + PLOT_W, avgY);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#33554a';
  ctx.font = '10px monospace';
  ctx.fillText(`6/π² ≈ ${SIX_PI2.toFixed(3)}·n`, PLOT_X + PLOT_W - 90, avgY - 4);

  // Labels
  ctx.fillStyle = DIMTEXT;
  ctx.font = '11px monospace';
  ctx.save();
  ctx.translate(16, PLOT_Y + PLOT_H / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText('φ(n)', -18, 0);
  ctx.restore();
  ctx.fillText('n', PLOT_X + PLOT_W / 2, PLOT_Y + PLOT_H + 30);
}

function draw(n) {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  // Title
  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText("Euler's Totient Function φ(n)", MARGIN_L, 32);
  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  ctx.fillText('φ(n) = count of integers 1..n coprime to n', MARGIN_L, 52);

  drawAxes();

  // Plot points
  for (let i = 1; i <= Math.min(n, MAX_N); i++) {
    const val = phi[i];
    const [sx, sy] = toScreen(i, val);
    const prime = isPrime(i, phi);
    ctx.fillStyle = prime ? AMBER : '#3a4050';
    ctx.fillRect(sx - 1, sy - 1, 2.5, 2.5);
  }

  // Running average φ(n)/n
  if (ratioHistory.length > 1) {
    ctx.fillStyle = '#111';
    ctx.fillRect(PLOT_X, RATIO_Y, PLOT_W, RATIO_H);

    const maxRatio = 1.0;
    ctx.strokeStyle = '#44aacc';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (let i = 0; i < ratioHistory.length; i++) {
      const x = PLOT_X + (i / (MAX_N - 1)) * PLOT_W;
      const y = RATIO_Y + RATIO_H - ratioHistory[i] * RATIO_H;
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // 6/π² target line
    const targetY = RATIO_Y + RATIO_H - SIX_PI2 * RATIO_H;
    ctx.strokeStyle = '#33554a';
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);
    ctx.beginPath();
    ctx.moveTo(PLOT_X, targetY);
    ctx.lineTo(PLOT_X + PLOT_W, targetY);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.fillStyle = DIMTEXT;
    ctx.font = '10px monospace';
    ctx.fillText(`φ(n)/n  →  6/π² ≈ ${SIX_PI2.toFixed(4)}`, PLOT_X + 4, RATIO_Y + 12);
  }

  // Legend
  ctx.fillStyle = AMBER;
  ctx.fillRect(W - 160, MARGIN_T + 10, 10, 10);
  ctx.fillStyle = WHITE;
  ctx.font = '11px monospace';
  ctx.fillText('prime n', W - 144, MARGIN_T + 20);
  ctx.fillStyle = '#3a4050';
  ctx.fillRect(W - 160, MARGIN_T + 26, 10, 10);
  ctx.fillStyle = DIMTEXT;
  ctx.fillText('composite n', W - 144, MARGIN_T + 36);

  // Current value
  if (n <= MAX_N) {
    const pn = phi[n];
    const ratio = pn / n;
    ctx.fillStyle = WHITE;
    ctx.font = '12px monospace';
    ctx.fillText(`n=${n}  φ(n)=${pn}  ratio=${ratio.toFixed(3)}`, MARGIN_L, H - 12);
  }
}

function advance() {
  if (!running) return;
  if (revealN > MAX_N) {
    // Compute running average
    let sum = 0;
    for (let i = 1; i <= MAX_N; i++) sum += phi[i] / i;
    const avg = sum / MAX_N;
    window.__setStatus && window.__setStatus(`φ(n) complete — avg φ(n)/n = ${avg.toFixed(4)} → 6/π² = ${SIX_PI2.toFixed(4)} — click to restart`);
    draw(MAX_N);
    return;
  }

  ratioHistory.push(phi[revealN] / revealN);
  draw(revealN);
  window.__setStatus && window.__setStatus(`n = ${revealN} — φ(${revealN}) = ${phi[revealN]} — click to restart`);
  revealN += 2;
  const delay = revealN < 30 ? 100 : revealN < 100 ? 30 : 8;
  phaseTimeout = setTimeout(advance, delay);
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  if (phaseTimeout) clearTimeout(phaseTimeout);
  revealN = 1;
  ratioHistory.length = 0;
  draw(0);
  window.__setStatus && window.__setStatus('φ(n) — integers coprime to n — click to restart');
  phaseTimeout = setTimeout(advance, 400);
}

window.__programRestart = init;
init();
