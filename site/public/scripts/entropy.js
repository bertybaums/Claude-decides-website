// Shannon Entropy — H = -Σ p·log₂(p)
// Animate distributions morphing and show entropy changing
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const AMBER = '#c8922a';
const BG = '#0f0f0f';
const WHITE = '#e8e4dc';
const DIMTEXT = '#6b6560';
const DIM_BAR = '#2a2520';

const W = canvas.width;
const H = canvas.height;

function entropy(probs) {
  let h = 0;
  for (const p of probs) {
    if (p > 1e-10) h -= p * Math.log2(p);
  }
  return h;
}

// Named configurations with their target probability distributions (8 bins)
const CONFIGS = [
  {
    name: 'Uniform (max entropy)',
    probs: [1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/8],
    labels: ['A','B','C','D','E','F','G','H'],
  },
  {
    name: 'Slightly skewed',
    probs: [0.25, 0.18, 0.15, 0.13, 0.11, 0.08, 0.06, 0.04],
    labels: ['A','B','C','D','E','F','G','H'],
  },
  {
    name: 'Geometric distribution',
    probs: [0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125, 0.0078125],
    labels: ['A','B','C','D','E','F','G','H'],
  },
  {
    name: 'Almost certain (low entropy)',
    probs: [0.88, 0.04, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01],
    labels: ['A','B','C','D','E','F','G','H'],
  },
  {
    name: 'Certain (H = 0)',
    probs: [1.0, 0, 0, 0, 0, 0, 0, 0],
    labels: ['A','B','C','D','E','F','G','H'],
  },
  {
    name: 'Two outcomes (coin)',
    probs: [0.5, 0.5, 0, 0, 0, 0, 0, 0],
    labels: ['H','T','','','','','',''],
  },
  {
    name: 'Biased coin 70/30',
    probs: [0.7, 0.3, 0, 0, 0, 0, 0, 0],
    labels: ['H','T','','','','','',''],
  },
  {
    name: 'English letters (26)',
    probs: null, // filled in below
    labels: Array.from('ETAOINSHRDLCUMWFGYPBVKJXQZ'),
  },
];

// English letter frequencies (top 8 by frequency as fraction of total shown)
const englishFreqs = [0.127,0.091,0.082,0.075,0.070,0.067,0.063,0.061];
const englishSum = englishFreqs.reduce((a,b)=>a+b,0);
CONFIGS[7].probs = englishFreqs.map(f => f / englishSum);
CONFIGS[7].name = 'English letters (top 8, normalized)';

let configIdx = 0;
let currentProbs = [...CONFIGS[0].probs];
let targetProbs = [...CONFIGS[0].probs];
let morphT = 1.0; // 0..1, lerp progress
let phaseTimeout = null;
let running = true;

// H-value animation
let displayH = entropy(currentProbs);
let targetH = displayH;

// H over time for sparkline
const H_HISTORY = [];
const MAX_HISTORY = 200;

function lerp(a, b, t) { return a + (b - a) * t; }

function getDisplayProbs() {
  return currentProbs.map((p, i) => lerp(p, targetProbs[i], morphT));
}

// Bar chart layout
const BAR_AREA_X = 60;
const BAR_AREA_Y = 100;
const BAR_AREA_W = W - 120;
const BAR_AREA_H = H - 290;
const N_BARS = 8;
const BAR_GAP = 8;
const BAR_W = (BAR_AREA_W - BAR_GAP * (N_BARS - 1)) / N_BARS;

// H display area
const H_DISPLAY_Y = BAR_AREA_Y + BAR_AREA_H + 20;
const SPARKLINE_Y = H_DISPLAY_Y + 60;
const SPARKLINE_H = 60;

function draw() {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  const probs = getDisplayProbs();
  const h = entropy(probs);
  displayH = h;
  const maxEntropy = Math.log2(N_BARS); // = 3 bits for 8 bins

  const cfg = CONFIGS[configIdx < CONFIGS.length ? configIdx : 0];

  // Title
  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText('Shannon Entropy   H = −Σ p · log₂(p)', BAR_AREA_X, 36);

  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  ctx.fillText(cfg.name, BAR_AREA_X, 58);

  // Bars
  const maxProb = Math.max(...probs, 0.01);
  for (let i = 0; i < N_BARS; i++) {
    const p = probs[i];
    const bx = BAR_AREA_X + i * (BAR_W + BAR_GAP);
    const bh = (p / maxProb) * BAR_AREA_H * 0.9;
    const by = BAR_AREA_Y + BAR_AREA_H - bh;

    // Background
    ctx.fillStyle = DIM_BAR;
    ctx.fillRect(bx, BAR_AREA_Y, BAR_W, BAR_AREA_H);

    // Bar
    ctx.fillStyle = AMBER;
    ctx.fillRect(bx, by, BAR_W, bh);

    // Label
    ctx.fillStyle = DIMTEXT;
    ctx.font = '11px monospace';
    const label = cfg.labels[i] || '';
    ctx.fillText(label, bx + BAR_W / 2 - 4, BAR_AREA_Y + BAR_AREA_H + 16);

    // Probability
    if (p > 0.005) {
      ctx.fillStyle = '#888';
      ctx.font = '10px monospace';
      const pStr = p.toFixed(2);
      ctx.fillText(pStr, bx + BAR_W / 2 - 10, by - 4);
    }
  }

  // Axis line
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(BAR_AREA_X, BAR_AREA_Y + BAR_AREA_H);
  ctx.lineTo(BAR_AREA_X + BAR_AREA_W, BAR_AREA_Y + BAR_AREA_H);
  ctx.stroke();

  // H display — big number
  const hFrac = h / maxEntropy;
  const hBarW = (W - 120) * hFrac;

  // H bar background
  ctx.fillStyle = '#1a1510';
  ctx.fillRect(BAR_AREA_X, H_DISPLAY_Y, W - 120, 28);
  // H bar filled
  ctx.fillStyle = AMBER;
  ctx.fillRect(BAR_AREA_X, H_DISPLAY_Y, hBarW, 28);

  // H value text
  ctx.fillStyle = BG;
  ctx.font = 'bold 16px monospace';
  const hText = `H = ${h.toFixed(4)} bits`;
  const maxText = ` / ${maxEntropy.toFixed(3)} max`;
  if (hBarW > 200) {
    ctx.fillText(hText + maxText, BAR_AREA_X + 10, H_DISPLAY_Y + 20);
  } else {
    ctx.fillStyle = AMBER;
    ctx.fillText(hText + maxText, BAR_AREA_X + hBarW + 8, H_DISPLAY_Y + 20);
  }

  // Efficiency
  ctx.fillStyle = DIMTEXT;
  ctx.font = '11px monospace';
  ctx.fillText(`efficiency: ${(100 * hFrac).toFixed(1)}%  |  H = 0 → certain  |  H = ${maxEntropy.toFixed(2)} → uniform`, BAR_AREA_X, H_DISPLAY_Y + 44);

  // Sparkline of H over time
  if (H_HISTORY.length > 1) {
    ctx.fillStyle = '#111';
    ctx.fillRect(BAR_AREA_X, SPARKLINE_Y, W - 120, SPARKLINE_H);

    ctx.strokeStyle = AMBER;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (let i = 0; i < H_HISTORY.length; i++) {
      const sx = BAR_AREA_X + (i / MAX_HISTORY) * (W - 120);
      const sy = SPARKLINE_Y + SPARKLINE_H - (H_HISTORY[i] / maxEntropy) * SPARKLINE_H * 0.9;
      if (i === 0) ctx.moveTo(sx, sy);
      else ctx.lineTo(sx, sy);
    }
    ctx.stroke();

    ctx.fillStyle = DIMTEXT;
    ctx.font = '10px monospace';
    ctx.fillText('H over time', BAR_AREA_X + 4, SPARKLINE_Y + 12);
    ctx.fillText(`${maxEntropy.toFixed(1)} bits`, BAR_AREA_X + 4, SPARKLINE_Y + 26);
    ctx.fillText('0 bits', BAR_AREA_X + 4, SPARKLINE_Y + SPARKLINE_H - 4);
  }
}

let frame = 0;
function animate() {
  if (!running) return;
  morphT = Math.min(1.0, morphT + 0.02);
  frame++;
  if (frame % 3 === 0) {
    H_HISTORY.push(entropy(getDisplayProbs()));
    if (H_HISTORY.length > MAX_HISTORY) H_HISTORY.shift();
  }
  draw();
  animId = requestAnimationFrame(animate);
}

function nextConfig() {
  if (!running) return;
  configIdx = (configIdx + 1) % CONFIGS.length;
  currentProbs = getDisplayProbs();
  targetProbs = [...CONFIGS[configIdx].probs];
  morphT = 0;

  const cfg = CONFIGS[configIdx];
  const h = entropy(cfg.probs);
  window.__setStatus && window.__setStatus(`H = ${h.toFixed(3)} bits — ${cfg.name} — click to restart`);

  phaseTimeout = setTimeout(nextConfig, 2800);
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  if (phaseTimeout) clearTimeout(phaseTimeout);
  configIdx = 0;
  currentProbs = [...CONFIGS[0].probs];
  targetProbs = [...CONFIGS[0].probs];
  morphT = 1.0;
  H_HISTORY.length = 0;
  frame = 0;
  window.__setStatus && window.__setStatus('H = 3.000 bits — uniform distribution — click to restart');
  phaseTimeout = setTimeout(nextConfig, 2000);
  animate();
}

window.__programRestart = init;
init();
