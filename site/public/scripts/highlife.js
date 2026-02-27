// HighLife — Conway's Life + birth rule 6, enables replicators
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
const CELL = 8;
let W, H, grid, animId, gen, running = true;

function makeGrid(w, h) { return new Uint8Array(w * h); }

// HighLife replicator pattern
const REPLICATOR = [
  [0,3],[0,4],[0,5],[0,6],[0,7],
  [1,2],[1,7],[2,1],[2,7],[3,0],[3,7],
  [4,0],[4,6],[5,0],[5,5],[6,0],[7,1],[7,2],[7,3],[7,4],[7,5],
];

function step() {
  const next = makeGrid(W, H);
  for (let r = 0; r < H; r++) {
    for (let c = 0; c < W; c++) {
      let n = 0;
      for (let dr = -1; dr <= 1; dr++)
        for (let dc = -1; dc <= 1; dc++)
          if ((dr || dc)) n += grid[((r + dr + H) % H) * W + (c + dc + W) % W];
      const alive = grid[r * W + c];
      // HighLife: B36/S23 — born with 3 or 6, survives with 2 or 3
      next[r * W + c] = alive ? (n === 2 || n === 3 ? 1 : 0) : (n === 3 || n === 6 ? 1 : 0);
    }
  }
  return next;
}

function draw() {
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#7eb8d4';
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
  // Place replicator near center
  const or = Math.floor(H / 2) - 4, oc = Math.floor(W / 2) - 4;
  for (const [r, c] of REPLICATOR) {
    const nr = (or + r + H) % H, nc = (oc + c + W) % W;
    grid[nr * W + nc] = 1;
  }
  window.__setStatus && window.__setStatus('HighLife replicator — generation 0 — click to restart');
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
