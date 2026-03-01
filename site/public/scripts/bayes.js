// Bayesian Inference — updating beliefs with evidence
// Coin-flipping scenario: θ = P(heads), evidence = observed flips
// Prior is uniform (Beta(1,1)). Each flip updates the Beta distribution.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const AMBER = '#c8922a';
const DIM = '#3a3530';
const BG = '#0f0f0f';
const WHITE = '#e8e4dc';
const DIMTEXT = '#6b6560';

// True bias of the "coin" (hidden from viewer — posterior should converge to this)
const TRUE_BIAS = 0.72;

// Beta distribution PDF: proportional to x^(a-1) * (1-x)^(b-1)
function betaPDF(x, alpha, beta) {
  if (x <= 0 || x >= 1) return 0;
  return Math.pow(x, alpha - 1) * Math.pow(1 - x, beta - 1);
}

// Beta distribution mean
function betaMean(alpha, beta) {
  return alpha / (alpha + beta);
}

// Sample from Bernoulli with given p
function flip(p) {
  return Math.random() < p ? 1 : 0;
}

let alpha = 1, beta_param = 1; // Beta(1,1) = uniform prior
let observations = [];
let heads = 0;
let step = 0;
let phaseTimeout = null;
let running = true;

const W = canvas.width;
const H = canvas.height;

// Layout
const GRAPH_X = 60;
const GRAPH_Y = 60;
const GRAPH_W = W - 120;
const GRAPH_H = H - 200;
const HIST_Y = GRAPH_Y + GRAPH_H + 40;
const HIST_H = 80;

function normalizeAndDraw(alpha, beta_p, color, fillAlpha) {
  const N = 300;
  const vals = [];
  let maxVal = 0;
  for (let i = 0; i <= N; i++) {
    const x = i / N;
    const v = betaPDF(x, alpha, beta_p);
    vals.push(v);
    if (v > maxVal) maxVal = v;
  }
  if (maxVal === 0) return;

  ctx.save();
  ctx.globalAlpha = fillAlpha;
  ctx.beginPath();
  ctx.moveTo(GRAPH_X, GRAPH_Y + GRAPH_H);
  for (let i = 0; i <= N; i++) {
    const x = GRAPH_X + (i / N) * GRAPH_W;
    const y = GRAPH_Y + GRAPH_H - (vals[i] / maxVal) * GRAPH_H * 0.92;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.lineTo(GRAPH_X + GRAPH_W, GRAPH_Y + GRAPH_H);
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.fill();

  ctx.globalAlpha = 1;
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let i = 0; i <= N; i++) {
    const x = GRAPH_X + (i / N) * GRAPH_W;
    const y = GRAPH_Y + GRAPH_H - (vals[i] / maxVal) * GRAPH_H * 0.92;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();
  ctx.restore();
}

function drawFrame() {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  // Title
  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText('Bayesian Inference — θ = P(heads)', GRAPH_X, 30);

  // Axes
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(GRAPH_X, GRAPH_Y);
  ctx.lineTo(GRAPH_X, GRAPH_Y + GRAPH_H);
  ctx.lineTo(GRAPH_X + GRAPH_W, GRAPH_Y + GRAPH_H);
  ctx.stroke();

  // X axis labels
  ctx.fillStyle = DIMTEXT;
  ctx.font = '11px monospace';
  for (let v = 0; v <= 10; v += 2) {
    const x = GRAPH_X + (v / 10) * GRAPH_W;
    ctx.fillText((v / 10).toFixed(1), x - 8, GRAPH_Y + GRAPH_H + 16);
    ctx.beginPath();
    ctx.strokeStyle = '#222';
    ctx.moveTo(x, GRAPH_Y);
    ctx.lineTo(x, GRAPH_Y + GRAPH_H);
    ctx.stroke();
  }
  ctx.fillStyle = DIMTEXT;
  ctx.fillText('θ', GRAPH_X + GRAPH_W / 2, GRAPH_Y + GRAPH_H + 32);

  // Prior (dim) and posterior (amber)
  // Draw prior (uniform, dim)
  normalizeAndDraw(1, 1, DIM, 0.3);
  // Draw current posterior (amber)
  if (alpha > 1 || beta_param > 1) {
    normalizeAndDraw(alpha, beta_param, AMBER, 0.35);
  }

  // True value line
  const trueX = GRAPH_X + TRUE_BIAS * GRAPH_W;
  ctx.strokeStyle = '#ffffff44';
  ctx.setLineDash([4, 4]);
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(trueX, GRAPH_Y);
  ctx.lineTo(trueX, GRAPH_Y + GRAPH_H);
  ctx.stroke();
  ctx.setLineDash([]);

  // Posterior mean line
  if (observations.length > 0) {
    const mean = betaMean(alpha, beta_param);
    const meanX = GRAPH_X + mean * GRAPH_W;
    ctx.strokeStyle = AMBER;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(meanX, GRAPH_Y + 10);
    ctx.lineTo(meanX, GRAPH_Y + GRAPH_H);
    ctx.stroke();

    ctx.fillStyle = AMBER;
    ctx.font = '12px monospace';
    ctx.fillText(`μ = ${mean.toFixed(3)}`, meanX + 5, GRAPH_Y + 24);
  }

  // Observation history — last 40 shown as small circles
  const obsToShow = observations.slice(-60);
  const obsY = HIST_Y + HIST_H / 2;
  const circR = 5;
  ctx.fillStyle = DIMTEXT;
  ctx.font = '11px monospace';
  ctx.fillText('Evidence:', GRAPH_X, HIST_Y - 6);

  for (let i = 0; i < obsToShow.length; i++) {
    const x = GRAPH_X + i * 12 + 6;
    const obs = obsToShow[i];
    ctx.beginPath();
    ctx.arc(x, obsY, circR, 0, Math.PI * 2);
    ctx.fillStyle = obs === 1 ? AMBER : '#444';
    ctx.fill();
  }

  // Stats
  ctx.fillStyle = WHITE;
  ctx.font = '13px monospace';
  const n = observations.length;
  ctx.fillText(`n = ${n}   heads = ${heads}   tails = ${n - heads}`, GRAPH_X, HIST_Y + HIST_H + 20);

  if (n > 0) {
    ctx.fillStyle = DIMTEXT;
    ctx.font = '12px monospace';
    ctx.fillText(`Beta(α=${alpha}, β=${beta_param})   posterior mean = ${betaMean(alpha, beta_param).toFixed(3)}`, GRAPH_X, HIST_Y + HIST_H + 38);
    ctx.fillText(`true θ = ${TRUE_BIAS} (dashed line)`, GRAPH_X, HIST_Y + HIST_H + 54);
  } else {
    ctx.fillStyle = DIMTEXT;
    ctx.font = '12px monospace';
    ctx.fillText('prior = uniform Beta(1,1)  — any θ equally plausible', GRAPH_X, HIST_Y + HIST_H + 38);
  }

  // Legend
  ctx.fillStyle = DIM;
  ctx.fillRect(W - 160, GRAPH_Y + 10, 16, 16);
  ctx.fillStyle = DIMTEXT;
  ctx.font = '11px monospace';
  ctx.fillText('prior', W - 138, GRAPH_Y + 22);

  ctx.fillStyle = AMBER;
  ctx.fillRect(W - 160, GRAPH_Y + 32, 16, 16);
  ctx.fillStyle = DIMTEXT;
  ctx.fillText('posterior', W - 138, GRAPH_Y + 44);
}

function addObservation() {
  if (!running) return;
  const result = flip(TRUE_BIAS);
  observations.push(result);
  if (result === 1) {
    heads++;
    alpha++;
  } else {
    beta_param++;
  }
  drawFrame();
  const n = observations.length;
  window.__setStatus && window.__setStatus(`${n} observation${n > 1 ? 's' : ''} — posterior updating — click to restart`);
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  if (phaseTimeout) clearTimeout(phaseTimeout);
  alpha = 1;
  beta_param = 1;
  observations = [];
  heads = 0;
  step = 0;
  drawFrame();
  window.__setStatus && window.__setStatus('prior = uniform — click to restart');
  scheduleNext();
}

function scheduleNext() {
  if (!running) return;
  const n = observations.length;
  // Slow at first, then faster
  const delay = n < 5 ? 800 : n < 20 ? 400 : n < 60 ? 150 : n < 150 ? 80 : 40;
  if (n >= 300) {
    window.__setStatus && window.__setStatus(`300 observations — posterior ≈ ${betaMean(alpha, beta_param).toFixed(3)} — click to restart`);
    return;
  }
  phaseTimeout = setTimeout(() => {
    addObservation();
    scheduleNext();
  }, delay);
}

window.__programRestart = init;
init();
