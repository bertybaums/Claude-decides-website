// Rule 184 — Traffic Cellular Automaton
// 1 = car, 0 = empty space. A car moves forward if the next cell is empty.
// Rule 184: (0,0,0)→0, (0,0,1)→0, (0,1,0)→0, (0,1,1)→1,
//           (1,0,0)→1, (1,0,1)→0, (1,1,0)→1, (1,1,1)→1
// This models single-lane traffic with wrap-around boundary conditions.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const AMBER = '#c8922a';
const BG = '#0f0f0f';
const WHITE = '#e8e4dc';
const DIMTEXT = '#6b6560';

const W = canvas.width;
const H = canvas.height;

const RULE = 184;
const RULE_TABLE = Array.from({length: 8}, (_, i) => (RULE >> i) & 1);

function rule184Step(row) {
  const n = row.length;
  const next = new Uint8Array(n);
  for (let i = 0; i < n; i++) {
    const left = row[(i - 1 + n) % n];
    const center = row[i];
    const right = row[(i + 1) % n];
    const idx = (left << 2) | (center << 1) | right;
    next[i] = RULE_TABLE[idx];
  }
  return next;
}

// Multiple lanes with different densities
const N_LANES = 28;
const CELL_LENGTH = 100;
const DENSITY = 0.38; // fraction of cells with cars

// Each lane has slightly different initial density to show variety
const DENSITIES = Array.from({length: N_LANES}, (_, i) =>
  Math.max(0.15, Math.min(0.75, DENSITY + (i - N_LANES / 2) * 0.008))
);

const HEADER_H = 60;
const LANE_H = Math.floor((H - HEADER_H - 20) / N_LANES);
const CELL_W = Math.floor((W - 60) / CELL_LENGTH);
const GRID_X = 30;
const GRID_Y = HEADER_H;

let lanes = [];
let stepCount = 0;
let running = true;
let phaseTimeout = null;

function initLanes() {
  lanes = DENSITIES.map(d => {
    const lane = new Uint8Array(CELL_LENGTH);
    for (let i = 0; i < CELL_LENGTH; i++) {
      lane[i] = Math.random() < d ? 1 : 0;
    }
    return lane;
  });
}

// Density wave detection — count transitions (density waves move backward)
function countCars(lane) {
  return lane.reduce((s, c) => s + c, 0);
}

// Draw a single lane
function drawLane(laneIdx, lane) {
  const y = GRID_Y + laneIdx * LANE_H;
  for (let i = 0; i < CELL_LENGTH; i++) {
    const x = GRID_X + i * CELL_W;
    if (lane[i] === 1) {
      // Car: amber with slight variation
      const brightness = 0.7 + 0.3 * Math.sin(i * 0.5 + laneIdx * 0.3);
      ctx.fillStyle = `rgba(200, 146, 42, ${brightness})`;
      ctx.fillRect(x, y + 1, CELL_W - 1, LANE_H - 2);
    } else {
      // Empty: very dark
      ctx.fillStyle = '#111';
      ctx.fillRect(x, y + 1, CELL_W - 1, LANE_H - 2);
    }
  }
}

// Draw all lanes
function draw() {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText('Rule 184 — Traffic Automaton', GRID_X, 28);

  const totalCars = lanes.reduce((s, l) => s + countCars(l), 0);
  const totalCells = N_LANES * CELL_LENGTH;
  const avgDensity = totalCars / totalCells;

  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  ctx.fillText(`step ${stepCount}   density ${(avgDensity * 100).toFixed(1)}%   ${N_LANES} lanes × ${CELL_LENGTH} cells`, GRID_X, 48);

  for (let i = 0; i < N_LANES; i++) {
    drawLane(i, lanes[i]);
  }

  // Lane index labels
  ctx.fillStyle = DIMTEXT;
  ctx.font = '9px monospace';
  if (LANE_H >= 12) {
    ctx.fillText('↑ low density', W - 95, GRID_Y + 10);
    ctx.fillText('↓ high density', W - 100, GRID_Y + N_LANES * LANE_H - 4);
  }
}

function step() {
  if (!running) return;
  lanes = lanes.map(rule184Step);
  stepCount++;
  draw();

  const delay = stepCount < 10 ? 200 : 60;
  phaseTimeout = setTimeout(step, delay);

  if (stepCount % 5 === 0) {
    const d = lanes[Math.floor(N_LANES / 2)];
    const cars = countCars(d);
    const density = (cars / CELL_LENGTH * 100).toFixed(0);
    window.__setStatus && window.__setStatus(`step ${stepCount} — density ${density}% — traffic jams forming — click to restart`);
  }
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  if (phaseTimeout) clearTimeout(phaseTimeout);
  stepCount = 0;
  initLanes();
  draw();
  window.__setStatus && window.__setStatus(`density ${(DENSITY * 100).toFixed(0)}% — traffic jams forming — click to restart`);
  phaseTimeout = setTimeout(step, 400);
}

window.__programRestart = init;
init();
