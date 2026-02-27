// Lorenz Attractor — butterfly effect
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

// Lorenz parameters
const sigma = 10, rho = 28, beta = 8/3;
const dt = 0.005;

let x, y, z, points, projAngle;

function lorenzStep() {
  const dx = sigma * (y - x);
  const dy = x * (rho - z) - y;
  const dz = x * y - beta * z;
  x += dx * dt;
  y += dy * dt;
  z += dz * dt;
  return [x, y, z];
}

function project(x, y, z) {
  // Simple orthographic projection with rotation
  const cosA = Math.cos(projAngle), sinA = Math.sin(projAngle);
  const px = x * cosA - y * sinA;
  const py = (x * sinA + y * cosA) * 0.5 - z * 0.7;
  return [px, py];
}

function toCanvas(px, py) {
  const W = canvas.width, H = canvas.height;
  const scale = Math.min(W, H) / 80;
  return [W / 2 + px * scale, H / 2 + py * scale + 60];
}

const MAX_POINTS = 3000;

function init() {
  running = true;
  cancelAnimationFrame(animId);
  x = 0.1; y = 0; z = 0;
  projAngle = 0.3;
  points = [];
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  window.__setStatus && window.__setStatus('drawing attractor — click to restart');
  run();
}

let lastTime = 0;
const PTS_PER_FRAME = 15;

function run(ts = 0) {
  if (!running) return;
  if (ts - lastTime < 20) { animId = requestAnimationFrame(run); return; }
  lastTime = ts;

  projAngle += 0.002;

  for (let i = 0; i < PTS_PER_FRAME; i++) {
    const [nx, ny, nz] = lorenzStep();
    points.push([nx, ny, nz]);
    if (points.length > MAX_POINTS) points.shift();
  }

  ctx.fillStyle = 'rgba(15,15,15,0.15)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.lineWidth = 0.8;
  for (let i = 1; i < points.length; i++) {
    const t = i / points.length;
    const [p1x, p1y] = toCanvas(...project(...points[i-1]));
    const [p2x, p2y] = toCanvas(...project(...points[i]));
    // Color: blue to orange
    const r = Math.floor(t * 200);
    const g = Math.floor(t * 100);
    const b = Math.floor((1 - t) * 200 + t * 50);
    ctx.strokeStyle = `rgba(${r},${g},${b},0.7)`;
    ctx.beginPath();
    ctx.moveTo(p1x, p1y);
    ctx.lineTo(p2x, p2y);
    ctx.stroke();
  }

  window.__setStatus && window.__setStatus(`t=${(points.length * dt).toFixed(2)} — σ=10 ρ=28 β=8/3 — click to restart`);
  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
