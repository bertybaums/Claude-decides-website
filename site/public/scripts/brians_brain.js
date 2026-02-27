// Brian's Brain — 3-state automaton, produces streams of gliders
// States: 0=dead, 1=firing, 2=refractory
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
const CELL = 7;
let W, H, grid, animId, gen, running = true;

function makeGrid(w, h) {
  return Array.from({ length: h }, () => new Uint8Array(w));
}

function step() {
  const next = makeGrid(W, H);
  for (let r = 0; r < H; r++) {
    for (let c = 0; c < W; c++) {
      const s = grid[r][c];
      if (s === 1) {
        next[r][c] = 2; // firing → refractory
      } else if (s === 2) {
        next[r][c] = 0; // refractory → dead
      } else {
        // dead: fires if exactly 2 neighbors are firing
        let firing = 0;
        for (let dr = -1; dr <= 1; dr++)
          for (let dc = -1; dc <= 1; dc++)
            if ((dr || dc) && grid[(r + dr + H) % H][(c + dc + W) % W] === 1)
              firing++;
        next[r][c] = firing === 2 ? 1 : 0;
      }
    }
  }
  grid = next;
}

const COLORS = ['#0f0f0f', '#e8e8e8', '#555'];

function draw() {
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  for (let r = 0; r < H; r++)
    for (let c = 0; c < W; c++) {
      const s = grid[r][c];
      if (s) {
        ctx.fillStyle = COLORS[s];
        ctx.fillRect(c * CELL + 1, r * CELL + 1, CELL - 1, CELL - 1);
      }
    }
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  W = Math.floor(canvas.width / CELL);
  H = Math.floor(canvas.height / CELL);
  grid = makeGrid(W, H);
  gen = 0;
  // Random initialization
  for (let r = 0; r < H; r++)
    for (let c = 0; c < W; c++)
      grid[r][c] = Math.random() < 0.3 ? (Math.random() < 0.5 ? 1 : 2) : 0;
  window.__setStatus && window.__setStatus('generation 0 — click to restart');
  run();
}

let lastTime = 0;
function run(ts = 0) {
  if (!running) return;
  if (ts - lastTime < 60) { animId = requestAnimationFrame(run); return; }
  lastTime = ts;
  draw();
  step();
  gen++;
  window.__setStatus && window.__setStatus(`generation ${gen} — click to restart`);
  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
