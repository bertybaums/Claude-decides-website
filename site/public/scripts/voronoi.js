// Voronoi Diagram — nearest-seed partitioning of the plane
// Each point in the plane belongs to whichever seed it is closest to.
// Seeds drift slowly; the diagram ripples and reconfigures continuously.
// Every rearrangement is local — a flip between two cells — yet the whole changes.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

const N_SEEDS = 24;
const DRIFT_SPEED = 0.4; // pixels per frame
const RENDER_INTERVAL = 30; // ms between full redraws (pixel-level is expensive)

// Warm/cool palette — 24 distinct colors
const PALETTE = [
  [180,  90,  20],  // burnt orange
  [220, 140,  40],  // amber
  [200,  60,  40],  // rust
  [160,  40,  80],  // crimson
  [100,  50, 140],  // violet
  [ 60,  80, 160],  // slate blue
  [ 40, 120, 160],  // steel blue
  [ 30, 140, 120],  // teal
  [ 60, 160,  80],  // sage
  [120, 160,  50],  // olive
  [180, 120,  30],  // gold
  [210,  80,  60],  // coral
  [150,  30, 100],  // magenta
  [ 80,  40, 160],  // purple
  [ 40, 100, 180],  // cerulean
  [ 20, 160, 140],  // jade
  [ 80, 180,  80],  // green
  [160, 180,  40],  // yellow-green
  [200, 100,  50],  // terracotta
  [220,  60,  80],  // rose
  [120,  40, 160],  // indigo
  [ 40, 140, 200],  // sky
  [ 30, 180, 120],  // mint
  [200, 160,  60],  // honey
];

let seeds = [];

function initSeeds() {
  seeds = [];
  for (let i = 0; i < N_SEEDS; i++) {
    seeds.push({
      x:  Math.random() * canvas.width,
      y:  Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * DRIFT_SPEED * 2,
      vy: (Math.random() - 0.5) * DRIFT_SPEED * 2,
      color: PALETTE[i % PALETTE.length],
    });
  }
}

function updateSeeds() {
  for (const s of seeds) {
    s.x += s.vx;
    s.y += s.vy;
    // Bounce off edges
    if (s.x < 0)              { s.x = 0;              s.vx = Math.abs(s.vx); }
    if (s.x > canvas.width)   { s.x = canvas.width;   s.vx = -Math.abs(s.vx); }
    if (s.y < 0)              { s.y = 0;              s.vy = Math.abs(s.vy); }
    if (s.y > canvas.height)  { s.y = canvas.height;  s.vy = -Math.abs(s.vy); }
  }
}

function renderVoronoi() {
  const W = canvas.width, H = canvas.height;
  const imgData = ctx.createImageData(W, H);
  const d = imgData.data;

  // Precompute seed positions as flat arrays for speed
  const sx = new Float32Array(N_SEEDS);
  const sy = new Float32Array(N_SEEDS);
  for (let i = 0; i < N_SEEDS; i++) { sx[i] = seeds[i].x; sy[i] = seeds[i].y; }

  for (let py = 0; py < H; py++) {
    for (let px = 0; px < W; px++) {
      let minDist = Infinity;
      let minI = 0;
      for (let i = 0; i < N_SEEDS; i++) {
        const dx = px - sx[i];
        const dy = py - sy[i];
        const dist = dx * dx + dy * dy;
        if (dist < minDist) { minDist = dist; minI = i; }
      }

      // Shade: darken toward region edge (Euclidean distance to second-nearest)
      let secondDist = Infinity;
      for (let i = 0; i < N_SEEDS; i++) {
        if (i === minI) continue;
        const dx = px - sx[i];
        const dy = py - sy[i];
        const dist = dx * dx + dy * dy;
        if (dist < secondDist) secondDist = dist;
      }

      const edgeness = Math.sqrt(minDist) / (Math.sqrt(minDist) + Math.sqrt(secondDist));
      // edgeness near 0.5 = cell boundary
      const dark = edgeness < 0.45 ? (0.45 - edgeness) / 0.45 : 0;
      const bright = 1 - dark * 0.7;

      const [R, G, B] = seeds[minI].color;
      const ci = (py * W + px) * 4;
      d[ci]     = Math.floor(R * bright * 0.6); // darken for dark bg aesthetic
      d[ci + 1] = Math.floor(G * bright * 0.6);
      d[ci + 2] = Math.floor(B * bright * 0.6);
      d[ci + 3] = 255;
    }
  }

  ctx.putImageData(imgData, 0, 0);

  // Draw seed points on top
  for (let i = 0; i < N_SEEDS; i++) {
    const [R, G, B] = seeds[i].color;
    ctx.fillStyle = `rgb(${Math.min(255, R + 60)},${Math.min(255, G + 60)},${Math.min(255, B + 60)})`;
    ctx.beginPath();
    ctx.arc(seeds[i].x, seeds[i].y, 3, 0, 2 * Math.PI);
    ctx.fill();

    // Bright core dot
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(seeds[i].x, seeds[i].y, 1.2, 0, 2 * Math.PI);
    ctx.fill();
  }
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  initSeeds();

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  window.__setStatus && window.__setStatus(`${N_SEEDS} seeds — nearest wins — click to restart`);
  run();
}

let lastRender = 0;

function run(ts = 0) {
  if (!running) return;

  updateSeeds();

  if (ts - lastRender >= RENDER_INTERVAL) {
    renderVoronoi();
    lastRender = ts;
    window.__setStatus && window.__setStatus(`${N_SEEDS} seeds — nearest wins — click to restart`);
  }

  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
