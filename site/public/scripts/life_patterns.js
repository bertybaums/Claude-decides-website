// Conway's Life Pattern Showcase
// Shows classic patterns in sequence, each on a clean canvas.
// Glider → Glider Gun → R-pentomino → Acorn
// Amber cells on dark background. Auto-advance.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

// Pattern definitions (relative cell coords [row, col])
const PATTERNS = [
  {
    name: 'Glider',
    steps: 80,
    cells: [[0,1],[1,2],[2,0],[2,1],[2,2]],
    zoom: 14,
    startR: 3, startC: 3,
  },
  {
    name: 'Gosper Glider Gun',
    steps: 200,
    cells: [
      [5,1],[5,2],[6,1],[6,2],
      [5,11],[6,11],[7,11],[4,12],[8,12],[3,13],[9,13],[3,14],[9,14],
      [6,15],[4,16],[8,16],[5,17],[6,17],[7,17],[6,18],
      [3,21],[4,21],[5,21],[3,22],[4,22],[5,22],[2,23],[6,23],
      [1,25],[2,25],[6,25],[7,25],
      [3,35],[4,35],[3,36],[4,36],
    ],
    zoom: 7,
    startR: 2, startC: 2,
  },
  {
    name: 'R-pentomino',
    steps: 250,
    cells: [[0,1],[0,2],[1,0],[1,1],[2,1]],
    zoom: 8,
    startR: null, startC: null, // centered
  },
  {
    name: 'Acorn',
    steps: 350,
    cells: [[0,1],[1,3],[2,0],[2,1],[2,4],[2,5],[2,6]],
    zoom: 8,
    startR: null, startC: null,
  },
];

let patIdx, cells, step, frameCount;

function initPattern() {
  const pat = PATTERNS[patIdx];
  const W = canvas.width, H = canvas.height;
  const COLS = Math.floor(W / pat.zoom);
  const ROWS = Math.floor(H / pat.zoom);

  cells = new Set();

  let baseR, baseC;
  if (pat.startR !== null) {
    baseR = pat.startR; baseC = pat.startC;
  } else {
    // Find bounding box of pattern, center it
    const rs = pat.cells.map(([r]) => r);
    const cs = pat.cells.map(([, c]) => c);
    const minR = Math.min(...rs), maxR = Math.max(...rs);
    const minC = Math.min(...cs), maxC = Math.max(...cs);
    baseR = Math.floor((ROWS - (maxR - minR)) / 2) - minR;
    baseC = Math.floor((COLS - (maxC - minC)) / 2) - minC;
  }

  for (const [r, c] of pat.cells) {
    cells.add((baseR + r) * 4096 + (baseC + c));
  }

  step = 0;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);
}

function countNeighbors(r, c) {
  let n = 0;
  for (let dr = -1; dr <= 1; dr++) {
    for (let dc = -1; dc <= 1; dc++) {
      if (dr === 0 && dc === 0) continue;
      if (cells.has((r + dr) * 4096 + (c + dc))) n++;
    }
  }
  return n;
}

function lifeStep() {
  const candidates = new Map();
  for (const key of cells) {
    const r = Math.floor(key / 4096);
    const c = key % 4096;
    for (let dr = -1; dr <= 1; dr++) {
      for (let dc = -1; dc <= 1; dc++) {
        const k = (r + dr) * 4096 + (c + dc);
        candidates.set(k, (candidates.get(k) || 0) + (dr === 0 && dc === 0 ? 0 : 0));
      }
    }
  }

  // Gather all cells to check: live cells and their neighbors
  const toCheck = new Set();
  for (const key of cells) {
    const r = Math.floor(key / 4096);
    const c = key % 4096;
    for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
      toCheck.add((r + dr) * 4096 + (c + dc));
    }
  }

  const next = new Set();
  for (const key of toCheck) {
    const r = Math.floor(key / 4096);
    const c = key % 4096;
    const alive = cells.has(key);
    const n = countNeighbors(r, c);
    if (alive && (n === 2 || n === 3)) next.add(key);
    if (!alive && n === 3) next.add(key);
  }
  cells = next;
}

function renderCells() {
  const pat = PATTERNS[patIdx];
  const W = canvas.width, H = canvas.height;
  const Z = pat.zoom;
  const COLS = Math.floor(W / Z);
  const ROWS = Math.floor(H / Z);

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = '#c8922a';
  for (const key of cells) {
    const r = Math.floor(key / 4096);
    const c = key % 4096;
    if (r >= 0 && r < ROWS && c >= 0 && c < COLS) {
      ctx.fillRect(c * Z + 1, r * Z + 1, Z - 1, Z - 1);
    }
  }

  // Pattern name label
  ctx.fillStyle = 'rgba(255,255,255,0.5)';
  ctx.font = `${Math.floor(canvas.height * 0.04)}px monospace`;
  ctx.fillText(pat.name, 10, canvas.height - 10);
}

function init() {
  cancelAnimationFrame(animId);
  patIdx = 0;
  initPattern();
  run();
}

function advance() {
  patIdx = (patIdx + 1) % PATTERNS.length;
  initPattern();
}

const STEPS_PER_FRAME = 1;

function run() {
  const pat = PATTERNS[patIdx];

  for (let i = 0; i < STEPS_PER_FRAME; i++) {
    lifeStep();
    step++;
  }
  renderCells();

  window.__setStatus && window.__setStatus(
    `${pat.name} — step ${step}/${pat.steps} — click for next`
  );

  if (step >= pat.steps) {
    setTimeout(() => {
      advance();
      animId = requestAnimationFrame(run);
    }, 800);
  } else {
    animId = requestAnimationFrame(run);
  }
}

canvas.addEventListener('click', () => {
  cancelAnimationFrame(animId);
  patIdx = (patIdx + 1) % PATTERNS.length;
  initPattern();
  animId = requestAnimationFrame(run);
});

window.__programRestart = init;
init();
