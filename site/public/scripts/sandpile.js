// Abelian Sandpile (BTW Model) — self-organized criticality
// Drop grains at the center. When a cell reaches 4, it topples: loses 4 grains,
// each neighbor gains 1. Boundary grains fall off. The emergent pattern is a mandala.
// Avalanche sizes follow a power law — no characteristic scale. The system self-tunes.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

// Grid size — must be odd so center is exact
const GSIZE = 121;
const CELL = Math.floor(Math.min(
  canvas.width / GSIZE,
  canvas.height / GSIZE
));
let OFFX, OFFY;

let grid;
let totalGrains = 0;
let largestAvalanche = 0;

// Colors for 0–3 grains
const COLORS = [
  [15,  15,  15],   // 0 — black
  [40,  30,  10],   // 1 — very dim warm
  [100, 65,  15],   // 2 — medium amber
  [200, 146, 42],   // 3 — bright amber
];

function initGrid() {
  grid = new Int32Array(GSIZE * GSIZE);
  totalGrains = 0;
  largestAvalanche = 0;
  OFFX = Math.floor((canvas.width  - GSIZE * CELL) / 2);
  OFFY = Math.floor((canvas.height - GSIZE * CELL) / 2);
}

const cx = Math.floor(GSIZE / 2);
const cy = Math.floor(GSIZE / 2);

function dropGrain() {
  grid[cy * GSIZE + cx]++;
  totalGrains++;
}

// Topple all unstable cells — returns number of cells toppled (avalanche size)
function topple() {
  let avalanche = 0;
  let changed = true;
  while (changed) {
    changed = false;
    for (let r = 0; r < GSIZE; r++) {
      for (let c = 0; c < GSIZE; c++) {
        const idx = r * GSIZE + c;
        if (grid[idx] >= 4) {
          const n = Math.floor(grid[idx] / 4);
          grid[idx] -= 4 * n;
          changed = true;
          avalanche += n;
          if (r > 0)         grid[(r - 1) * GSIZE + c] += n;
          if (r < GSIZE - 1) grid[(r + 1) * GSIZE + c] += n;
          if (c > 0)         grid[r * GSIZE + (c - 1)] += n;
          if (c < GSIZE - 1) grid[r * GSIZE + (c + 1)] += n;
          // Boundary: grains that go off edge are simply lost (grid boundary = sink)
        }
      }
    }
  }
  return avalanche;
}

const DROPS_PER_FRAME = 5;

// Render using imageData for speed
function render(flashCells) {
  const imgData = ctx.createImageData(canvas.width, canvas.height);
  const d = imgData.data;

  // Background
  for (let i = 0; i < d.length; i += 4) {
    d[i] = 15; d[i+1] = 15; d[i+2] = 15; d[i+3] = 255;
  }

  for (let r = 0; r < GSIZE; r++) {
    for (let c = 0; c < GSIZE; c++) {
      const val = Math.min(grid[r * GSIZE + c], 3);
      const [R, G, B] = COLORS[val];

      const x0 = OFFX + c * CELL;
      const y0 = OFFY + r * CELL;

      for (let py = 0; py < CELL; py++) {
        for (let px = 0; px < CELL; px++) {
          const ci = ((y0 + py) * canvas.width + (x0 + px)) * 4;
          if (ci < 0 || ci + 3 >= d.length) continue;
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

function init() {
  running = true;
  cancelAnimationFrame(animId);
  initGrid();

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  window.__setStatus && window.__setStatus('0 grains — click to restart');
  run();
}

function run() {
  if (!running) return;

  for (let i = 0; i < DROPS_PER_FRAME; i++) {
    dropGrain();
    const av = topple();
    if (av > largestAvalanche) largestAvalanche = av;
  }

  render();

  window.__setStatus && window.__setStatus(
    `${totalGrains.toLocaleString()} grains dropped — largest avalanche: ${largestAvalanche.toLocaleString()} — click to restart`
  );

  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
