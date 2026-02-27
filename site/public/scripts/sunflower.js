// Sunflower Spiral — golden angle phyllotaxis
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

const PHI = (1 + Math.sqrt(5)) / 2;
const GOLDEN_ANGLE = 2 * Math.PI * (2 - PHI); // ≈ 137.508°

let animId, n, running = true;

function init() {
  running = true;
  cancelAnimationFrame(animId);
  n = 0;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  window.__setStatus && window.__setStatus('golden angle ≈ 137.508° — Fibonacci spirals emerge — click to restart');
  run();
}

const TOTAL = 800;

function run() {
  if (!running) return;
  const W = canvas.width, H = canvas.height;
  const cx = W / 2, cy = H / 2;
  const maxR = Math.min(W, H) / 2 - 10;

  const batch = 5;
  for (let i = 0; i < batch && n < TOTAL; i++, n++) {
    const r = maxR * Math.sqrt(n / TOTAL);
    const theta = n * GOLDEN_ANGLE;
    const x = cx + r * Math.cos(theta);
    const y = cy + r * Math.sin(theta);

    const t = n / TOTAL;
    const hue = 30 + t * 40; // yellow to orange
    const size = 2 + (1 - t) * 2;
    ctx.fillStyle = `hsl(${hue}, 80%, 60%)`;
    ctx.beginPath();
    ctx.arc(x, y, size, 0, Math.PI * 2);
    ctx.fill();
  }

  if (n < TOTAL) {
    animId = requestAnimationFrame(run);
  } else {
    window.__setStatus && window.__setStatus(`${TOTAL} seeds at golden angle — click to restart`);
  }
}

window.__programRestart = init;
init();
