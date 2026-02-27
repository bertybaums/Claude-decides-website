// Julia Sets — cycling through parameters
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

// Interesting Julia set parameters
const params = [
  { cr: -0.7, ci: 0.27015 },
  { cr: -0.4, ci: 0.6 },
  { cr: 0.285, ci: 0.01 },
  { cr: -0.835, ci: -0.2321 },
  { cr: -0.8, ci: 0.156 },
  { cr: 0.45, ci: 0.1428 },
];

let paramIdx = 0;
let phase = 0; // 0=render new, 1=hold, 2=transition

function julia(zr, zi, cr, ci, maxIter) {
  let i = 0;
  while (i < maxIter) {
    const zr2 = zr * zr, zi2 = zi * zi;
    if (zr2 + zi2 > 4) return i + 1 - Math.log2(Math.log2(Math.sqrt(zr2 + zi2)));
    const newZr = zr2 - zi2 + cr;
    zi = 2 * zr * zi + ci;
    zr = newZr;
    i++;
  }
  return -1;
}

function hsl(h, s, l) {
  const toRgb = (p, q, t) => {
    if (t < 0) t++; if (t > 1) t--;
    if (t < 1/6) return p + (q - p) * 6 * t;
    if (t < 0.5) return q;
    if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
    return p;
  };
  h /= 360; s /= 100; l /= 100;
  const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
  const p = 2 * l - q;
  return [toRgb(p, q, h + 1/3), toRgb(p, q, h), toRgb(p, q, h - 1/3)].map(x => Math.round(x * 255));
}

function renderJulia(cr, ci) {
  const W = canvas.width, H = canvas.height;
  const img = ctx.createImageData(W, H);
  const d = img.data;
  const maxIter = 150;
  const scale = 3.0 / Math.min(W, H);
  for (let py = 0; py < H; py++) {
    for (let px = 0; px < W; px++) {
      const zr = (px - W / 2) * scale;
      const zi = (py - H / 2) * scale;
      const m = julia(zr, zi, cr, ci, maxIter);
      const idx = (py * W + px) * 4;
      if (m < 0) { d[idx] = d[idx+1] = d[idx+2] = 8; }
      else {
        const t = m / maxIter;
        const [r, g, b] = hsl((200 + t * 280) % 360, 70, 45 + t * 30);
        d[idx] = r; d[idx+1] = g; d[idx+2] = b;
      }
      d[idx+3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
}

let holdFrames = 0;
const HOLD = 30;

function init() {
  running = true;
  cancelAnimationFrame(animId);
  paramIdx = 0;
  holdFrames = 0;
  window.__setStatus && window.__setStatus('Julia set cycling — click to restart');
  renderJulia(params[0].cr, params[0].ci);
  animId = requestAnimationFrame(tick);
}

function tick() {
  if (!running) return;
  holdFrames++;
  if (holdFrames >= HOLD) {
    holdFrames = 0;
    paramIdx = (paramIdx + 1) % params.length;
    const p = params[paramIdx];
    renderJulia(p.cr, p.ci);
    window.__setStatus && window.__setStatus(`c = ${p.cr} + ${p.ci}i — click to restart`);
  }
  animId = requestAnimationFrame(tick);
}

window.__programRestart = init;
init();
