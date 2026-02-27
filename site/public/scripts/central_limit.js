// Central Limit Theorem — sum of random variables approaches normal distribution
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

function init() {
  running = true;
  cancelAnimationFrame(animId);
  window.__setStatus && window.__setStatus('add n uniform random variables — histogram approaches normal — click to restart');
  draw(1);
  let n = 1;
  const interval = setInterval(() => {
    if (!running) { clearInterval(interval); return; }
    n++;
    draw(n);
    if (n >= 20) {
      clearInterval(interval);
      window.__setStatus && window.__setStatus('n=20 terms — bell curve emerged — click to restart');
    }
  }, 600);
  animId = { stop: () => clearInterval(interval) };
}

function draw(n) {
  const W = canvas.width, H = canvas.height;
  const SAMPLES = 5000;
  const BINS = 60;
  const padding = { t: 50, b: 40, l: 30, r: 30 };
  const plotW = W - padding.l - padding.r;
  const plotH = H - padding.t - padding.b;

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  // Generate samples: sum of n uniform [0,1] random variables
  const hist = new Array(BINS).fill(0);
  let minVal = 0, maxVal = n; // range is [0, n]

  for (let s = 0; s < SAMPLES; s++) {
    let sum = 0;
    for (let i = 0; i < n; i++) sum += Math.random();
    const bin = Math.min(BINS - 1, Math.floor((sum / n) * BINS));
    hist[bin]++;
  }

  const maxH = Math.max(...hist);
  const barW = plotW / BINS;

  // Draw histogram bars
  for (let b = 0; b < BINS; b++) {
    const barHeight = (hist[b] / maxH) * plotH;
    const t = hist[b] / maxH;
    ctx.fillStyle = `hsl(${200 + t * 30}, 60%, ${35 + t * 30}%)`;
    ctx.fillRect(padding.l + b * barW, padding.t + plotH - barHeight, barW - 0.5, barHeight);
  }

  // Normal curve overlay
  const mean = 0.5, std = 1 / Math.sqrt(12 * n);
  ctx.strokeStyle = '#c8922a';
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let px = 0; px < plotW; px++) {
    const x = px / plotW; // in [0, 1]
    const gaussian = Math.exp(-0.5 * ((x - mean) / std) ** 2) / (std * Math.sqrt(2 * Math.PI));
    // Scale to histogram height
    const normalized = gaussian / (1 / std / Math.sqrt(2 * Math.PI));
    const y = padding.t + plotH - normalized * plotH;
    px === 0 ? ctx.moveTo(padding.l + px, y) : ctx.lineTo(padding.l + px, y);
  }
  ctx.stroke();

  // Label
  ctx.fillStyle = '#888';
  ctx.font = '13px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(`n = ${n} uniform variables summed (${SAMPLES.toLocaleString()} samples)`, W / 2, padding.t - 25);
  ctx.fillStyle = '#c8922a';
  ctx.fillText('— normal curve overlay', W / 2, padding.t - 10);
}

window.__programRestart = () => {
  if (animId && animId.stop) animId.stop();
  init();
};
init();
