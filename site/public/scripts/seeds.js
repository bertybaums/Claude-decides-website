// Seeds — B2/S0: born with 2 neighbors, no survival
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
const CELL = 6;
let W, H, grid, animId, gen, running = true;

function makeGrid(w, h) { return new Uint8Array(w * h); }

function step() {
  const next = makeGrid(W, H);
  for (let r = 0; r < H; r++) {
    for (let c = 0; c < W; c++) {
      let n = 0;
      for (let dr = -1; dr <= 1; dr++)
        for (let dc = -1; dc <= 1; dc++)
          if ((dr || dc)) n += grid[((r + dr + H) % H) * W + (c + dc + W) % W];
      // B2/S: born with exactly 2, no cell survives
      next[r * W + c] = grid[r * W + c] === 0 && n === 2 ? 1 : 0;
    }
  }
  return next;
}

function draw() {
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#d4e8a0';
  for (let r = 0; r < H; r++)
    for (let c = 0; c < W; c++)
      if (grid[r * W + c]) ctx.fillRect(c * CELL + 1, r * CELL + 1, CELL - 1, CELL - 1);
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  W = Math.floor(canvas.width / CELL);
  H = Math.floor(canvas.height / CELL);
  grid = makeGrid(W, H);
  gen = 0;
  // Sparse random seed
  for (let i = 0; i < W * H * 0.05; i++) {
    const r = Math.floor(Math.random() * H);
    const c = Math.floor(Math.random() * W);
    grid[r * W + c] = 1;
  }
  window.__setStatus && window.__setStatus('Seeds — no cell survives past one generation — click to restart');
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
