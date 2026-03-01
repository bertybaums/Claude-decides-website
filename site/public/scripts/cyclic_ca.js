// Cyclic Cellular Automaton — BZ-reaction-like waves
// N states. Each cell advances to (state+1)%N if any neighbor is already there.
// Otherwise it stays. Spiral waves emerge from noise — no central pacemaker needed.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

let animId;
let grid, next;
let step = 0;
let COLS, ROWS;
const CELL = 4;
const N_STATES = 16;  // more states = longer, more beautiful spirals

// Color palette: dark → teal → bright teal/cyan
function stateColor(s) {
  const t = s / (N_STATES - 1);
  if (t < 0.12) {
    // Near-black / very dark blue
    const v = t / 0.12;
    return [Math.round(v * 5), Math.round(v * 15), Math.round(v * 25)];
  } else if (t < 0.5) {
    // Dark to mid teal
    const v = (t - 0.12) / 0.38;
    return [0, Math.round(v * 120), Math.round(80 + v * 80)];
  } else {
    // Mid teal to bright cyan-white
    const v = (t - 0.5) / 0.5;
    return [Math.round(v * 180), Math.round(120 + v * 135), Math.round(160 + v * 95)];
  }
}

// Precompute palette
const PALETTE = [];
for (let s = 0; s < N_STATES; s++) {
  PALETTE.push(stateColor(s));
}

function buildGrid() {
  const W = canvas.width, H = canvas.height;
  COLS = Math.floor(W / CELL);
  ROWS = Math.floor(H / CELL);
  grid = new Uint8Array(COLS * ROWS);
  next = new Uint8Array(COLS * ROWS);

  // Sparse random seeds — mostly zeros with occasional bursts
  for (let i = 0; i < COLS * ROWS; i++) {
    grid[i] = Math.random() < 0.08 ? Math.floor(Math.random() * N_STATES) : 0;
  }
}

function idx(x, y) {
  return ((y + ROWS) % ROWS) * COLS + ((x + COLS) % COLS);
}

function stepGrid() {
  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      const s = grid[idx(x, y)];
      const target = (s + 1) % N_STATES;
      // Check 4 neighbors (von Neumann)
      if (
        grid[idx(x+1, y)] === target ||
        grid[idx(x-1, y)] === target ||
        grid[idx(x, y+1)] === target ||
        grid[idx(x, y-1)] === target
      ) {
        next[idx(x, y)] = target;
      } else {
        next[idx(x, y)] = s;
      }
    }
  }
  // Swap
  const tmp = grid;
  grid = next;
  next = tmp;
  step++;
}

function draw() {
  const W = canvas.width, H = canvas.height;
  const imageData = ctx.createImageData(W, H);
  const data = imageData.data;

  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      const s = grid[y * COLS + x];
      const [r, g, b] = PALETTE[s];
      // Fill CELL×CELL block
      for (let dy = 0; dy < CELL; dy++) {
        for (let dx = 0; dx < CELL; dx++) {
          const px = x * CELL + dx;
          const py = y * CELL + dy;
          if (px >= W || py >= H) continue;
          const i = (py * W + px) * 4;
          data[i]   = r;
          data[i+1] = g;
          data[i+2] = b;
          data[i+3] = 255;
        }
      }
    }
  }

  ctx.putImageData(imageData, 0, 0);
}

function frame() {
  stepGrid();
  stepGrid();
  draw();
  const label = step < 200 ? 'waves forming' : step < 800 ? 'spirals emerging' : 'self-organizing';
  window.__setStatus && window.__setStatus(`step ${step} — ${label} — click to restart`);
  animId = requestAnimationFrame(frame);
}

function init() {
  cancelAnimationFrame(animId);
  step = 0;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  buildGrid();
  window.__setStatus && window.__setStatus('step 0 — waves forming — click to restart');
  animId = requestAnimationFrame(frame);
}

window.__programRestart = init;
init();
