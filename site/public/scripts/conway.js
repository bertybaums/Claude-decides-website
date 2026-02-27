// Conway's Game of Life — with Gosper Glider Gun
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
const CELL = 8;
let W, H, grid, animId, gen, running = true;

const GOSPER_GUN = [
  [0,24],[1,22],[1,24],[2,12],[2,13],[2,20],[2,21],[2,34],[2,35],
  [3,11],[3,15],[3,20],[3,21],[3,34],[3,35],
  [4,0],[4,1],[4,10],[4,16],[4,20],[4,21],
  [5,0],[5,1],[5,10],[5,14],[5,16],[5,17],[5,22],[5,24],
  [6,10],[6,16],[6,24],[7,11],[7,15],[8,12],[8,13],
];

function makeGrid(w, h) {
  return Array.from({ length: h }, () => new Uint8Array(w));
}

function countNeighbors(g, r, c) {
  let n = 0;
  for (let dr = -1; dr <= 1; dr++)
    for (let dc = -1; dc <= 1; dc++)
      if (dr || dc) n += g[(r + dr + H) % H][(c + dc + W) % W];
  return n;
}

function step() {
  const next = makeGrid(W, H);
  for (let r = 0; r < H; r++)
    for (let c = 0; c < W; c++) {
      const n = countNeighbors(grid, r, c);
      next[r][c] = grid[r][c] ? (n === 2 || n === 3 ? 1 : 0) : (n === 3 ? 1 : 0);
    }
  grid = next;
}

function draw() {
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#c8922a';
  for (let r = 0; r < H; r++)
    for (let c = 0; c < W; c++)
      if (grid[r][c]) ctx.fillRect(c * CELL + 1, r * CELL + 1, CELL - 1, CELL - 1);
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  W = Math.floor(canvas.width / CELL);
  H = Math.floor(canvas.height / CELL);
  grid = makeGrid(W, H);
  gen = 0;
  // Place Gosper Glider Gun at row 5, col 2
  const ro = 5, co = 2;
  for (const [dr, dc] of GOSPER_GUN) {
    const r = (ro + dr) % H, c = (co + dc) % W;
    if (r >= 0 && r < H && c >= 0 && c < W) grid[r][c] = 1;
  }
  window.__setStatus && window.__setStatus('generation 0 — click to restart');
  run();
}

let lastTime = 0;
function run(ts = 0) {
  if (!running) return;
  if (ts - lastTime < 80) { animId = requestAnimationFrame(run); return; }
  lastTime = ts;
  draw();
  step();
  gen++;
  window.__setStatus && window.__setStatus(`generation ${gen} — click to restart`);
  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
