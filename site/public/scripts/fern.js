// Barnsley Fern — iterated function system
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

// Four affine transformations and their probabilities
const transforms = [
  { a: 0,     b: 0,     c: 0,    d: 0.16, e: 0, f: 0,    p: 0.01 },
  { a: 0.85,  b: 0.04,  c:-0.04, d: 0.85, e: 0, f: 1.60, p: 0.85 },
  { a: 0.20,  b:-0.26,  c: 0.23, d: 0.22, e: 0, f: 1.60, p: 0.07 },
  { a:-0.15,  b: 0.28,  c: 0.26, d: 0.24, e: 0, f: 0.44, p: 0.07 },
];

function chooseTransform() {
  const r = Math.random();
  let cum = 0;
  for (const t of transforms) {
    cum += t.p;
    if (r < cum) return t;
  }
  return transforms[3];
}

let px = 0, py = 0;
let count = 0;

function toCanvas(x, y) {
  const W = canvas.width, H = canvas.height;
  return [
    Math.floor((x + 2.5) / 5.5 * W * 0.9 + W * 0.05),
    Math.floor(H - (y / 10) * H * 0.95 - H * 0.02),
  ];
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  px = 0; py = 0; count = 0;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  window.__setStatus && window.__setStatus('drawing fern — click to restart');
  run();
}

const PTS = 500;
function run() {
  if (!running) return;
  for (let i = 0; i < PTS; i++) {
    const t = chooseTransform();
    const nx = t.a * px + t.b * py + t.e;
    const ny = t.c * px + t.d * py + t.f;
    px = nx; py = ny;
    const [cx, cy] = toCanvas(px, py);
    if (count > 10) {
      const g = Math.floor(80 + (py / 10) * 120);
      ctx.fillStyle = `rgb(0,${g},0)`;
      ctx.fillRect(cx, cy, 1, 1);
    }
    count++;
  }
  if (count < 150000) {
    animId = requestAnimationFrame(run);
    window.__setStatus && window.__setStatus(`${count.toLocaleString()} points — click to restart`);
  } else {
    window.__setStatus && window.__setStatus('complete — four rules, one fern — click to restart');
  }
}

window.__programRestart = init;
init();
