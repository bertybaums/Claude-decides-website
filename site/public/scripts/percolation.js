// Percolation — does a path exist from top to bottom?
// Each cell is open with probability p. Below pc ≈ 0.5927, almost surely no path.
// Above it, almost surely yes. At pc, clusters at every scale — critical phenomenon.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

const COLS = 100;
const ROWS = 70;
let CELL_W, CELL_H;

const P_VALUES = [0.30, 0.45, 0.593, 0.65, 0.80];
const P_LABELS = ['0.30 (sparse)', '0.45 (subcritical)', '0.593 (critical)', '0.65 (supercritical)', '0.80 (dense)'];
const STAGE_DURATION = 3500; // ms each stage

let pIndex = 0;
let grid = null;       // 0=blocked, 1=open, 2=percolating
let bfsQueue = [];
let bfsVisited = null;
let bfsDone = false;
let percolates = false;
let stageStart = 0;
let phase = 'filling'; // 'filling' | 'bfs' | 'result'

const BFS_PER_FRAME = 80;

function buildGrid(p) {
  grid = new Uint8Array(COLS * ROWS);
  for (let i = 0; i < COLS * ROWS; i++) {
    grid[i] = Math.random() < p ? 1 : 0; // 1=open, 0=blocked
  }
}

function startBFS() {
  bfsVisited = new Uint8Array(COLS * ROWS);
  bfsQueue = [];
  percolates = false;

  // Seed from top row open cells
  for (let c = 0; c < COLS; c++) {
    const idx = 0 * COLS + c;
    if (grid[idx] === 1) {
      bfsQueue.push(idx);
      bfsVisited[idx] = 1;
      grid[idx] = 2; // mark as percolating cluster
    }
  }
  bfsDone = bfsQueue.length === 0;
}

function bfsStep() {
  if (bfsQueue.length === 0) {
    bfsDone = true;
    return;
  }
  const next = [];
  for (const idx of bfsQueue) {
    const r = Math.floor(idx / COLS);
    const c = idx % COLS;
    const neighbors = [
      r > 0      ? (r - 1) * COLS + c : -1,
      r < ROWS-1 ? (r + 1) * COLS + c : -1,
      c > 0      ? r * COLS + (c - 1) : -1,
      c < COLS-1 ? r * COLS + (c + 1) : -1,
    ];
    for (const ni of neighbors) {
      if (ni < 0) continue;
      if (!bfsVisited[ni] && grid[ni] === 1) {
        bfsVisited[ni] = 1;
        grid[ni] = 2;
        next.push(ni);
        if (Math.floor(ni / COLS) === ROWS - 1) percolates = true;
      }
    }
  }
  bfsQueue = next;
  if (bfsQueue.length === 0) bfsDone = true;
}

function render() {
  CELL_W = canvas.width / COLS;
  CELL_H = canvas.height / ROWS;

  const imgData = ctx.createImageData(canvas.width, canvas.height);
  const d = imgData.data;

  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const val = grid[r * COLS + c];
      let R, G, B;
      if (val === 0) {
        // blocked — near black
        R = 26; G = 26; B = 26;
      } else if (val === 1) {
        // open, not yet in percolating cluster — dim gray
        R = 60; G = 60; B = 60;
      } else {
        // percolating cluster — amber
        R = 200; G = 146; B = 42;
      }

      const x0 = Math.floor(c * CELL_W);
      const y0 = Math.floor(r * CELL_H);
      const x1 = Math.floor((c + 1) * CELL_W);
      const y1 = Math.floor((r + 1) * CELL_H);

      for (let py = y0; py < y1; py++) {
        for (let px = x0; px < x1; px++) {
          const ci = (py * canvas.width + px) * 4;
          d[ci]     = R;
          d[ci + 1] = G;
          d[ci + 2] = B;
          d[ci + 3] = 255;
        }
      }
    }
  }
  ctx.putImageData(imgData, 0, 0);
}

function startStage(idx, ts) {
  pIndex = idx % P_VALUES.length;
  stageStart = ts;
  phase = 'filling';
  buildGrid(P_VALUES[pIndex]);
  render();
  startBFS();
  phase = 'bfs';
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  pIndex = 0;

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  window.__setStatus && window.__setStatus('generating grid — click to restart');
  run();
}

function run(ts = 0) {
  if (!running) return;

  if (phase === 'bfs') {
    // Run BFS steps
    for (let i = 0; i < BFS_PER_FRAME && !bfsDone; i++) {
      bfsStep();
    }
    render();

    const p = P_VALUES[pIndex];
    const label = P_LABELS[pIndex];
    window.__setStatus && window.__setStatus(
      `p=${label}${bfsDone ? (percolates ? ' — percolates!' : ' — no path') : ' — searching...'} — click to restart`
    );

    if (bfsDone) {
      phase = 'result';
      stageStart = ts;
    }
  } else if (phase === 'result') {
    if (ts - stageStart >= STAGE_DURATION) {
      startStage(pIndex + 1, ts);
    }
    const label = P_LABELS[pIndex];
    window.__setStatus && window.__setStatus(
      `p=${label} — ${percolates ? 'percolates!' : 'no path'} — click to restart`
    );
  }

  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
