// Boids — Craig Reynolds' flocking simulation (1986)
// Three rules: separation, alignment, cohesion
// No central control — the flock emerges from local interactions
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const N = 120;
const MAX_SPEED = 2.5;
const MAX_FORCE = 0.08;
const SEP_RADIUS = 28;
const ALI_RADIUS = 55;
const COH_RADIUS = 55;
const SEP_WEIGHT = 1.8;
const ALI_WEIGHT = 1.0;
const COH_WEIGHT = 0.9;

let boids = [];

function normalize(x, y) {
  const m = Math.hypot(x, y);
  return m < 1e-9 ? [0, 0] : [x / m, y / m];
}

function limit(x, y, max) {
  const m = Math.hypot(x, y);
  return m > max ? [x / m * max, y / m * max] : [x, y];
}

function makeBoid() {
  const angle = Math.random() * Math.PI * 2;
  const speed = 1.0 + Math.random() * 1.5;
  return {
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: Math.cos(angle) * speed,
    vy: Math.sin(angle) * speed,
  };
}

function updateBoid(b, all) {
  let sx = 0, sy = 0, nSep = 0;
  let ax = 0, ay = 0, nAli = 0;
  let cx = 0, cy = 0, nCoh = 0;

  for (const o of all) {
    if (o === b) continue;
    const dx = o.x - b.x, dy = o.y - b.y;
    const d = Math.hypot(dx, dy);

    if (d < SEP_RADIUS && d > 0) {
      sx -= dx / d;
      sy -= dy / d;
      nSep++;
    }
    if (d < ALI_RADIUS) {
      ax += o.vx; ay += o.vy; nAli++;
    }
    if (d < COH_RADIUS) {
      cx += o.x; cy += o.y; nCoh++;
    }
  }

  let stx = 0, sty = 0;
  if (nSep > 0) {
    [stx, sty] = normalize(sx / nSep, sy / nSep);
    stx = stx * MAX_SPEED - b.vx;
    sty = sty * MAX_SPEED - b.vy;
    [stx, sty] = limit(stx, sty, MAX_FORCE);
  }

  let atx = 0, aty = 0;
  if (nAli > 0) {
    [atx, aty] = normalize(ax / nAli, ay / nAli);
    atx = atx * MAX_SPEED - b.vx;
    aty = aty * MAX_SPEED - b.vy;
    [atx, aty] = limit(atx, aty, MAX_FORCE);
  }

  let ctx2 = 0, cty = 0;
  if (nCoh > 0) {
    [ctx2, cty] = normalize(cx / nCoh - b.x, cy / nCoh - b.y);
    ctx2 = ctx2 * MAX_SPEED - b.vx;
    cty = cty * MAX_SPEED - b.vy;
    [ctx2, cty] = limit(ctx2, cty, MAX_FORCE);
  }

  b.vx += SEP_WEIGHT * stx + ALI_WEIGHT * atx + COH_WEIGHT * ctx2;
  b.vy += SEP_WEIGHT * sty + ALI_WEIGHT * aty + COH_WEIGHT * cty;
  [b.vx, b.vy] = limit(b.vx, b.vy, MAX_SPEED);

  b.x = (b.x + b.vx + canvas.width) % canvas.width;
  b.y = (b.y + b.vy + canvas.height) % canvas.height;
}

function drawBoid(b) {
  const angle = Math.atan2(b.vy, b.vx);
  // Color by heading: hue from 0-360
  const hue = ((angle + Math.PI) / (Math.PI * 2)) * 360;
  ctx.save();
  ctx.translate(b.x, b.y);
  ctx.rotate(angle);
  ctx.fillStyle = `hsl(${hue}, 90%, 65%)`;
  ctx.beginPath();
  ctx.moveTo(8, 0);
  ctx.lineTo(-5, 3.5);
  ctx.lineTo(-3, 0);
  ctx.lineTo(-5, -3.5);
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

function init() {
  cancelAnimationFrame(animId);
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  boids = Array.from({ length: N }, makeBoid);
  window.__setStatus && window.__setStatus(`${N} boids — 3 rules — click to restart`);
  run();
}

function run() {
  // Fade trail
  ctx.fillStyle = 'rgba(15,15,15,0.35)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (const b of boids) updateBoid(b, boids);
  for (const b of boids) drawBoid(b);

  window.__setStatus && window.__setStatus(`${N} boids — 3 rules — click to restart`);
  animId = requestAnimationFrame(run);
}

canvas.addEventListener('click', init);
window.__programRestart = init;
init();
