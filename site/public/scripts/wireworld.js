// Wireworld — electron flow through wires, can build logic gates
// States: 0=empty, 1=electron head, 2=electron tail, 3=conductor
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
const CELL = 12;
let W, H, grid, next, animId, gen, running = true;

const COLORS = ['#0f0f0f', '#e8e840', '#e84040', '#1060a0'];

function makeGrid(w, h) { return new Uint8Array(w * h); }
function idx(x, y) { return y * W + x; }

// A simple circuit: two-lane wire loop with signal
function buildCircuit() {
  grid = makeGrid(W, H);

  const midY = Math.floor(H / 2);
  const left = 3, right = W - 4;
  const top = midY - 4, bot = midY + 4;

  // Draw a rectangular loop
  for (let x = left; x <= right; x++) {
    grid[idx(x, top)] = 3;
    grid[idx(x, bot)] = 3;
  }
  for (let y = top; y <= bot; y++) {
    grid[idx(left, y)] = 3;
    grid[idx(right, y)] = 3;
  }

  // Place two signals at different positions to demonstrate interaction
  grid[idx(left + 2, top)] = 1;
  grid[idx(left + 1, top)] = 2;

  grid[idx(right - 4, bot)] = 1;
  grid[idx(right - 5, bot)] = 2;
}

function step() {
  next = makeGrid(W, H);
  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      const s = grid[idx(x, y)];
      if (s === 0) {
        next[idx(x, y)] = 0;
      } else if (s === 1) {
        next[idx(x, y)] = 2; // head → tail
      } else if (s === 2) {
        next[idx(x, y)] = 3; // tail → conductor
      } else {
        // Conductor: becomes head if 1 or 2 neighboring heads
        let heads = 0;
        for (let dy = -1; dy <= 1; dy++)
          for (let dx = -1; dx <= 1; dx++)
            if ((dx || dy) && x + dx >= 0 && x + dx < W && y + dy >= 0 && y + dy < H)
              if (grid[idx(x + dx, y + dy)] === 1) heads++;
        next[idx(x, y)] = (heads === 1 || heads === 2) ? 1 : 3;
      }
    }
  }
  grid = next;
}

function draw() {
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  for (let y = 0; y < H; y++)
    for (let x = 0; x < W; x++) {
      const s = grid[idx(x, y)];
      if (s) {
        ctx.fillStyle = COLORS[s];
        ctx.fillRect(x * CELL + 1, y * CELL + 1, CELL - 2, CELL - 2);
      }
    }
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  W = Math.floor(canvas.width / CELL);
  H = Math.floor(canvas.height / CELL);
  gen = 0;
  buildCircuit();
  window.__setStatus && window.__setStatus('electrons flowing — yellow=head, red=tail, blue=wire — click to restart');
  run();
}

let lastTime = 0;
function run(ts = 0) {
  if (!running) return;
  if (ts - lastTime < 150) { animId = requestAnimationFrame(run); return; }
  lastTime = ts;
  draw();
  step();
  gen++;
  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
