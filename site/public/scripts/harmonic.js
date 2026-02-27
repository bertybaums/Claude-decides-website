// Harmonic Series — diverges infinitely slowly
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

function init() {
  running = true;
  cancelAnimationFrame(animId);

  const W = canvas.width, H = canvas.height;
  const padding = { t: 50, b: 50, l: 80, r: 20 };
  const plotW = W - padding.l - padding.r;
  const plotH = H - padding.t - padding.b;

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  // Precompute partial sums
  const N = 500;
  const sums = [];
  let s = 0;
  for (let i = 1; i <= N; i++) { s += 1 / i; sums.push(s); }

  const maxS = sums[N - 1];

  // Grid
  ctx.strokeStyle = '#1a1a1a';
  ctx.lineWidth = 1;
  for (let v = 1; v <= Math.ceil(maxS); v++) {
    const y = padding.t + (1 - (v / maxS)) * plotH;
    ctx.beginPath(); ctx.moveTo(padding.l, y); ctx.lineTo(W - padding.r, y); ctx.stroke();
    ctx.fillStyle = '#333';
    ctx.font = '10px monospace';
    ctx.textAlign = 'right';
    ctx.fillText(v, padding.l - 6, y + 3);
  }

  // Curve
  ctx.strokeStyle = '#c8922a';
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let i = 0; i < N; i++) {
    const x = padding.l + (i / (N - 1)) * plotW;
    const y = padding.t + (1 - sums[i] / maxS) * plotH;
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.stroke();

  // Axis labels
  ctx.fillStyle = '#555';
  ctx.font = '10px monospace';
  ctx.textAlign = 'left';
  ctx.fillText('n=1', padding.l, H - 10);
  ctx.textAlign = 'right';
  ctx.fillText(`n=${N}`, W - padding.r, H - 10);

  ctx.fillStyle = '#888';
  ctx.font = '11px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(`H(${N}) = ${maxS.toFixed(4)} (diverges — just incredibly slowly)`, W / 2, padding.t - 15);

  // Annotation: when does it reach 10?
  let when10 = Math.floor(Math.exp(10 - 0.5772) / 1);
  ctx.fillStyle = '#666';
  ctx.font = '10px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(`To reach H=10 needs ≈12,367 terms`, W / 2, padding.t - 2);

  window.__setStatus && window.__setStatus(`H(${N}) ≈ ${maxS.toFixed(4)} — diverges, incredibly slowly — click to redraw`);
}

window.__programRestart = init;
init();
