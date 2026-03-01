// Chaos Game — Sierpinski Triangle from randomness
// Pick 3 vertices. Start anywhere. Repeatedly: pick a random vertex, move halfway.
// After a warmup, the Sierpinski triangle emerges. Structure from randomness.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

let animId;
let count = 0;
let px = 0, py = 0;

const WARMUP = 20;
const PTS_PER_FRAME = 400;
const TOTAL = 150000;

// Three warm colors, one per vertex
const COLORS = [
  [200, 100, 30],   // amber-orange
  [200, 60, 80],    // rose-red
  [180, 140, 40],   // golden-yellow
];

let vertices = [];

function buildVertices() {
  const W = canvas.width, H = canvas.height;
  const cx = W / 2;
  const margin = Math.min(W, H) * 0.08;
  const r = Math.min(W, H) * 0.46;
  // Equilateral triangle, apex at top
  vertices = [
    [cx, H / 2 - r],                              // top
    [cx - r * Math.cos(Math.PI / 6), H / 2 + r * 0.5],  // bottom-left
    [cx + r * Math.cos(Math.PI / 6), H / 2 + r * 0.5],  // bottom-right
  ];
}

function init() {
  cancelAnimationFrame(animId);
  count = 0;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  buildVertices();
  // Start at a random point inside the triangle (use centroid)
  const W = canvas.width, H = canvas.height;
  px = W / 2;
  py = H / 2;
  window.__setStatus && window.__setStatus('0 points — click to restart');
  run();
}

function run() {
  for (let i = 0; i < PTS_PER_FRAME; i++) {
    const vi = Math.floor(Math.random() * 3);
    const [vx, vy] = vertices[vi];
    px = (px + vx) / 2;
    py = (py + vy) / 2;
    count++;
    if (count <= WARMUP) continue;
    const [r, g, b] = COLORS[vi];
    // Slight alpha for density effect
    ctx.fillStyle = `rgba(${r},${g},${b},0.6)`;
    ctx.fillRect(Math.round(px), Math.round(py), 1, 1);
  }

  if (count < TOTAL) {
    const shown = Math.max(0, count - WARMUP);
    window.__setStatus && window.__setStatus(`${shown.toLocaleString()} points — click to restart`);
    animId = requestAnimationFrame(run);
  } else {
    window.__setStatus && window.__setStatus('complete — randomness, structure — click to restart');
  }
}

window.__programRestart = init;
init();
