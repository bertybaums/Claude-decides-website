// Monte Carlo π — throw random darts to estimate π
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

let inside, total;
const MAX_DARTS = 20000;
const DARTS_PER_FRAME = 200;

function init() {
  running = true;
  cancelAnimationFrame(animId);
  inside = 0; total = 0;

  const W = canvas.width, H = canvas.height;
  const size = Math.min(W, H) - 80;
  const ox = (W - size) / 2;
  const oy = (H - size) / 2 + 20;

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  // Draw square
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 1;
  ctx.strokeRect(ox, oy, size, size);

  // Draw circle
  ctx.strokeStyle = '#444';
  ctx.beginPath();
  ctx.arc(ox + size / 2, oy + size / 2, size / 2, 0, Math.PI * 2);
  ctx.stroke();

  window.__setStatus && window.__setStatus('throwing darts — click to restart');
  run();
}

function run() {
  if (!running) return;
  if (total >= MAX_DARTS) {
    window.__setStatus && window.__setStatus(`π ≈ ${(4 * inside / total).toFixed(6)} (${total.toLocaleString()} darts) — click to restart`);
    return;
  }

  const W = canvas.width, H = canvas.height;
  const size = Math.min(W, H) - 80;
  const ox = (W - size) / 2;
  const oy = (H - size) / 2 + 20;
  const r = size / 2;
  const cx = ox + r, cy = oy + r;

  for (let i = 0; i < DARTS_PER_FRAME && total < MAX_DARTS; i++) {
    const x = Math.random();
    const y = Math.random();
    const dx = x - 0.5, dy = y - 0.5;
    const inCircle = dx * dx + dy * dy <= 0.25;

    const px = ox + x * size;
    const py = oy + y * size;
    ctx.fillStyle = inCircle ? 'rgba(200,146,42,0.6)' : 'rgba(80,100,150,0.4)';
    ctx.fillRect(px, py, 1.5, 1.5);

    if (inCircle) inside++;
    total++;
  }

  const piApprox = (4 * inside / total).toFixed(6);

  // Status bar
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, 20);
  ctx.fillStyle = '#888';
  ctx.font = '11px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(`darts: ${total.toLocaleString()}  inside: ${inside.toLocaleString()}  π ≈ 4×(${inside}/${total}) = ${piApprox}`, W / 2, 14);

  window.__setStatus && window.__setStatus(`π ≈ ${piApprox} — click to restart`);
  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
