// Day & Night — B3678/S34678 — symmetric under inversion of live/dead
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
const CELL = 6;
let W, H, grid, animId, gen, running = true;

const BORN_WITH = new Set([3, 6, 7, 8]);
const SURVIVES_WITH = new Set([3, 4, 6, 7, 8]);

function makeGrid(w, h) { return new Uint8Array(w * h); }

function step() {
  const next = makeGrid(W, H);
  for (let r = 0; r < H; r++) {
    for (let c = 0; c < W; c++) {
      let n = 0;
      for (let dr = -1; dr <= 1; dr++)
        for (let dc = -1; dc <= 1; dc++)
          if ((dr || dc)) n += grid[((r + dr + H) % H) * W + (c + dc + W) % W];
      const alive = grid[r * W + c];
      next[r * W + c] = alive ? (SURVIVES_WITH.has(n) ? 1 : 0) : (BORN_WITH.has(n) ? 1 : 0);
    }
  }
  return next;
}

function draw() {
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#a0c8e8';
  for (let r = 0; r < H; r++)
    for (let c = 0; c < W; c++)
      if (grid[r * W + c]) ctx.fillRect(c * CELL, r * CELL, CELL, CELL);
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  W = Math.floor(canvas.width / CELL);
  H = Math.floor(canvas.height / CELL);
  grid = makeGrid(W, H);
  gen = 0;
  for (let i = 0; i < W * H; i++) grid[i] = Math.random() < 0.45 ? 1 : 0;
  window.__setStatus && window.__setStatus('Day & Night — symmetric under life/death inversion — click to restart');
  run();
}

let lastTime = 0;
function run(ts = 0) {
  if (!running) return;
  if (ts - lastTime < 80) { animId = requestAnimationFrame(run); return; }
  lastTime = ts;
  draw();
  grid = step();
  gen++;
  window.__setStatus && window.__setStatus(`generation ${gen} — click to restart`);
  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
