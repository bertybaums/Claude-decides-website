// Heat Equation / Diffusion
// ∂u/∂t = D · ∇²u
// Shows 2D diffusion: a bright spot spreads as heat flows outward.
// Pixel rendering. Colors: dark=cold (#0f0f0f), amber/white=hot.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const D = 0.22;  // diffusion coefficient
let grid, next, W, H, imageData, pixelBuf, step;

function initGrids() {
  W = canvas.width;
  H = canvas.height;
  grid = new Float32Array(W * H);
  next = new Float32Array(W * H);
  imageData = ctx.createImageData(W, H);
  pixelBuf = imageData.data;
}

function heatToColor(u) {
  // u in [0,1]: dark → deep amber → bright white
  const t = Math.max(0, Math.min(1, u));
  if (t < 0.4) {
    const s = t / 0.4;
    return [Math.floor(s * 200), Math.floor(s * 80), Math.floor(s * 10)];
  } else if (t < 0.75) {
    const s = (t - 0.4) / 0.35;
    return [200 + Math.floor(s * 55), 80 + Math.floor(s * 80), 10 + Math.floor(s * 60)];
  } else {
    const s = (t - 0.75) / 0.25;
    return [255, 160 + Math.floor(s * 95), 70 + Math.floor(s * 185)];
  }
}

function addSource(cx, cy, radius, intensity) {
  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      const d = Math.hypot(x - cx, y - cy);
      if (d < radius) {
        const v = intensity * Math.exp(-d * d / (2 * (radius / 2.5) * (radius / 2.5)));
        grid[y * W + x] = Math.max(grid[y * W + x], v);
      }
    }
  }
}

function diffuseStep() {
  for (let y = 1; y < H - 1; y++) {
    for (let x = 1; x < W - 1; x++) {
      const idx = y * W + x;
      const laplacian =
        grid[(y-1)*W + x] + grid[(y+1)*W + x] +
        grid[y*W + (x-1)] + grid[y*W + (x+1)] -
        4 * grid[idx];
      next[idx] = grid[idx] + D * laplacian;
      // Clamp
      if (next[idx] < 0) next[idx] = 0;
      if (next[idx] > 1) next[idx] = 1;
    }
  }
  // Neumann boundary (zero-flux)
  for (let x = 0; x < W; x++) {
    next[x] = next[W + x];
    next[(H-1)*W + x] = next[(H-2)*W + x];
  }
  for (let y = 0; y < H; y++) {
    next[y*W] = next[y*W + 1];
    next[y*W + W-1] = next[y*W + W-2];
  }
  // Swap
  const tmp = grid; grid = next; next = tmp;
}

function render() {
  for (let i = 0; i < W * H; i++) {
    const [r, g, b] = heatToColor(grid[i]);
    const o = i * 4;
    pixelBuf[o]   = r;
    pixelBuf[o+1] = g;
    pixelBuf[o+2] = b;
    pixelBuf[o+3] = 255;
  }
  ctx.putImageData(imageData, 0, 0);
}

let sources, srcTimer, srcInterval;

function init() {
  cancelAnimationFrame(animId);
  initGrids();
  step = 0;

  // Start with multiple heat sources
  sources = [
    [W * 0.5,  H * 0.5,  30, 1.0],
    [W * 0.25, H * 0.3,  18, 0.8],
    [W * 0.75, H * 0.7,  18, 0.8],
  ];
  for (const [cx, cy, r, v] of sources) addSource(cx, cy, r, v);

  window.__setStatus && window.__setStatus('t=0 — heat spreading — click to restart');
  run();
}

const STEPS_PER_FRAME = 3;

function run() {
  for (let i = 0; i < STEPS_PER_FRAME; i++) {
    diffuseStep();
    step++;
  }
  render();

  // Add a new random source every 400 steps to keep it interesting
  if (step % 400 === 0) {
    const cx = W * 0.15 + Math.random() * W * 0.7;
    const cy = H * 0.15 + Math.random() * H * 0.7;
    addSource(cx, cy, 20, 0.85);
  }

  window.__setStatus && window.__setStatus(`t=${step} — heat spreading — click to restart`);
  animId = requestAnimationFrame(run);
}

canvas.addEventListener('click', init);
window.__programRestart = init;
init();
