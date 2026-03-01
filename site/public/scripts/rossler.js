// Rössler Attractor
// dx/dt = -y-z, dy/dt = x+ay, dz/dt = b+z(x-c)
// a=0.2, b=0.2, c=5.7
// Projects 3D onto 2D with slow rotation. Colors by z-value.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const a = 0.2, b = 0.2, c = 5.7;
const DT = 0.012;
const MAX_PTS = 4000;
const PTS_PER_FRAME = 8;

let x, y, z, pts, angle, step;

function rosslerStep(x, y, z) {
  const dx = -y - z;
  const dy = x + a * y;
  const dz = b + z * (x - c);
  return [x + dx * DT, y + dy * DT, z + dz * DT];
}

function project(x, y, z, angle) {
  const cosA = Math.cos(angle), sinA = Math.sin(angle);
  const rx = x * cosA - y * sinA;
  const ry = x * sinA + y * cosA;
  // Isometric-ish: tilt z down
  return [rx, ry * 0.5 - z * 0.55];
}

function toCanvas(px, py) {
  const W = canvas.width, H = canvas.height;
  const scale = Math.min(W, H) / 38;
  return [W / 2 + px * scale, H / 2 + py * scale + H * 0.05];
}

function zToColor(z) {
  // z ranges roughly from -2 to 25
  const t = Math.max(0, Math.min(1, (z + 2) / 27));
  // cold (deep blue) to warm (amber/white)
  const r = Math.floor(t < 0.5 ? t * 2 * 80 : 80 + (t - 0.5) * 2 * 170);
  const g = Math.floor(t < 0.5 ? t * 2 * 30 : 30 + (t - 0.5) * 2 * 116);
  const b2 = Math.floor(t < 0.5 ? 60 + t * 2 * 140 : 200 - (t - 0.5) * 2 * 150);
  return [r, g, b2];
}

function init() {
  cancelAnimationFrame(animId);
  x = 0.5; y = 0; z = 0.04;
  pts = [];
  angle = 0.4;
  step = 0;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  window.__setStatus && window.__setStatus('Rössler attractor — a=0.2 b=0.2 c=5.7 — click to restart');
  run();
}

function run() {
  angle += 0.003;

  for (let i = 0; i < PTS_PER_FRAME; i++) {
    [x, y, z] = rosslerStep(x, y, z);
    pts.push([x, y, z]);
    if (pts.length > MAX_PTS) pts.shift();
    step++;
  }

  ctx.fillStyle = 'rgba(15,15,15,0.18)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.lineWidth = 0.9;
  for (let i = 1; i < pts.length; i++) {
    const t = i / pts.length;
    const [px1, py1] = toCanvas(...project(...pts[i-1], angle));
    const [px2, py2] = toCanvas(...project(...pts[i], angle));
    const [r, g, bl] = zToColor(pts[i][2]);
    ctx.strokeStyle = `rgba(${r},${g},${bl},${0.3 + t * 0.7})`;
    ctx.beginPath();
    ctx.moveTo(px1, py1);
    ctx.lineTo(px2, py2);
    ctx.stroke();
  }

  window.__setStatus && window.__setStatus(`Rössler attractor — t=${(step * DT).toFixed(1)} — click to restart`);
  animId = requestAnimationFrame(run);
}

canvas.addEventListener('click', init);
window.__programRestart = init;
init();
