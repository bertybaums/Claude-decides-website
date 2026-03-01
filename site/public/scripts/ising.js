// Ising Model — Metropolis algorithm on a spin lattice
// At the critical temperature Tc ≈ 2.269, order and disorder coexist
// at every scale simultaneously — the system becomes scale-invariant.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

const CELL = 3;
let W, H, grid;

// Critical temperature for 2D square Ising model
const TC = 2 / Math.log(1 + Math.sqrt(2)); // ≈ 2.2692

// Temperature stages: ordered, critical, disordered
const STAGES = [
  { label: '1.13 (ordered)', T: TC * 0.5 },
  { label: '2.27 (critical)', T: TC },
  { label: '4.54 (disordered)', T: TC * 2 },
];
const STAGE_DURATION = 5000; // ms each
let stageIndex = 0;
let stageStart = 0;

function initGrid() {
  W = Math.floor(canvas.width / CELL);
  H = Math.floor(canvas.height / CELL);
  grid = new Int8Array(W * H);
  // Start in random state
  for (let i = 0; i < W * H; i++) {
    grid[i] = Math.random() < 0.5 ? 1 : -1;
  }
}

function neighbor(i, dx, dy) {
  const x = (i % W + dx + W) % W;
  const y = (Math.floor(i / W) + dy + H) % H;
  return grid[y * W + x];
}

function magnetization() {
  let sum = 0;
  for (let i = 0; i < W * H; i++) sum += grid[i];
  return Math.abs(sum / (W * H));
}

const FLIPS_PER_FRAME = 15000;

function metropolisStep(T) {
  for (let k = 0; k < FLIPS_PER_FRAME; k++) {
    const i = (Math.random() * W * H) | 0;
    const s = grid[i];
    const sumNeigh =
      neighbor(i,  1,  0) + neighbor(i, -1,  0) +
      neighbor(i,  0,  1) + neighbor(i,  0, -1);
    const dE = 2 * s * sumNeigh;
    if (dE <= 0 || Math.random() < Math.exp(-dE / T)) {
      grid[i] = -s;
    }
  }
}

function render() {
  const imgData = ctx.createImageData(canvas.width, canvas.height);
  const d = imgData.data;

  for (let gy = 0; gy < H; gy++) {
    for (let gx = 0; gx < W; gx++) {
      const spin = grid[gy * W + gx];
      // spin up = amber #c8922a, spin down = #1a1a1a
      const r = spin === 1 ? 200 : 26;
      const g = spin === 1 ? 146 : 26;
      const b = spin === 1 ? 42  : 26;

      for (let py = 0; py < CELL; py++) {
        for (let px = 0; px < CELL; px++) {
          const ci = ((gy * CELL + py) * canvas.width + (gx * CELL + px)) * 4;
          d[ci]     = r;
          d[ci + 1] = g;
          d[ci + 2] = b;
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
  stageIndex = 0;
  stageStart = performance.now();
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  initGrid();
  window.__setStatus && window.__setStatus('initializing spins — click to restart');
  run();
}

let lastRender = 0;

function run(ts = 0) {
  if (!running) return;

  // Advance stage timer
  const elapsed = ts - stageStart;
  if (elapsed > STAGE_DURATION) {
    stageIndex = (stageIndex + 1) % STAGES.length;
    stageStart = ts;
  }

  const stage = STAGES[stageIndex];
  metropolisStep(stage.T);

  // Render every frame
  render();

  const mag = magnetization();
  window.__setStatus && window.__setStatus(
    `T=${stage.label} — magnetization=${mag.toFixed(2)} — click to restart`
  );

  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
