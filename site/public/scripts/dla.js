// Diffusion-Limited Aggregation — growing fractal cluster
// Particles random-walk from the boundary until they touch the cluster and stick.
// The branching geometry emerges from the physics of diffusion — tips grow faster
// because they intercept more random walkers.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

let animId;

// Work at reduced resolution for performance, scale up to canvas
const SCALE = 2;
let GW, GH;
let grid;         // Uint8Array: 0=empty, 1=cluster
let clusterCount = 0;
let maxDist = 0;   // furthest particle from center (for release radius)

const TARGET = 2500;

let cx, cy;

function gridIdx(x, y) { return y * GW + x; }

function init() {
  cancelAnimationFrame(animId);
  const W = canvas.width, H = canvas.height;
  GW = Math.floor(W / SCALE);
  GH = Math.floor(H / SCALE);
  grid = new Uint8Array(GW * GH);
  clusterCount = 0;

  cx = Math.floor(GW / 2);
  cy = Math.floor(GH / 2);

  // Seed particle at center
  grid[gridIdx(cx, cy)] = 1;
  clusterCount = 1;
  maxDist = 5;

  // Draw background
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  // Draw seed
  drawParticle(cx, cy, 0);

  window.__setStatus && window.__setStatus('0 particles — click to restart');
  animId = requestAnimationFrame(frame);
}

// Color by normalized distance from center: warm amber → cool blue-white
function particleColor(dist, maxD) {
  const t = Math.min(1, dist / (maxD * 0.85 + 1));
  const r = Math.round(200 - t * 70);
  const g = Math.round(110 + t * 80);
  const b = Math.round(20 + t * 200);
  return `rgb(${r},${g},${b})`;
}

function drawParticle(gx, gy, dist) {
  ctx.fillStyle = particleColor(dist, maxDist);
  ctx.fillRect(gx * SCALE, gy * SCALE, SCALE, SCALE);
}

function dist2(x, y) {
  const dx = x - cx, dy = y - cy;
  return Math.sqrt(dx * dx + dy * dy);
}

// Try to add one particle; returns true if it stuck
function addOneParticle() {
  const releaseR = Math.min(maxDist + 8, Math.min(GW, GH) / 2 - 2);
  const killR = releaseR + 15;

  // Release from random point on a circle of radius releaseR
  const angle = Math.random() * 2 * Math.PI;
  let px = Math.round(cx + releaseR * Math.cos(angle));
  let py = Math.round(cy + releaseR * Math.sin(angle));

  // Clamp to grid
  px = Math.max(1, Math.min(GW - 2, px));
  py = Math.max(1, Math.min(GH - 2, py));

  const MAX_STEPS = 5000;
  for (let step = 0; step < MAX_STEPS; step++) {
    // Random walk step
    const dir = Math.floor(Math.random() * 4);
    if (dir === 0) px++;
    else if (dir === 1) px--;
    else if (dir === 2) py++;
    else py--;

    // Boundary wrap / kill
    if (px <= 0 || px >= GW - 1 || py <= 0 || py >= GH - 1) return false;
    const d = dist2(px, py);
    if (d > killR) return false;

    // Check 4 neighbors for cluster contact
    if (
      grid[gridIdx(px+1, py)] ||
      grid[gridIdx(px-1, py)] ||
      grid[gridIdx(px, py+1)] ||
      grid[gridIdx(px, py-1)]
    ) {
      // Stick!
      grid[gridIdx(px, py)] = 1;
      clusterCount++;
      const particleDist = d;
      if (particleDist > maxDist) maxDist = particleDist;
      drawParticle(px, py, particleDist);
      return true;
    }
  }
  return false;
}

const BATCH = 3;

function frame() {
  if (clusterCount >= TARGET) {
    window.__setStatus && window.__setStatus(`${clusterCount} particles — fractal complete — click to restart`);
    return;
  }

  for (let i = 0; i < BATCH; i++) {
    addOneParticle();
  }

  window.__setStatus && window.__setStatus(`${clusterCount} particles — click to restart`);
  animId = requestAnimationFrame(frame);
}

window.__programRestart = init;
init();
