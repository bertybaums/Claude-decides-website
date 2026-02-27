// Langton's Ant — chaos then highway after ~10,000 steps
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
const CELL = 5;
let grid, ax, ay, dir, step, animId, running = true;

// Directions: 0=up, 1=right, 2=down, 3=left
const DX = [0, 1, 0, -1];
const DY = [-1, 0, 1, 0];

let W, H;

function init() {
  running = true;
  cancelAnimationFrame(animId);
  W = Math.floor(canvas.width / CELL);
  H = Math.floor(canvas.height / CELL);
  grid = new Uint8Array(W * H);
  ax = Math.floor(W / 2);
  ay = Math.floor(H / 2);
  dir = 0;
  step = 0;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  window.__setStatus && window.__setStatus('step 0 — click to restart');
  run();
}

function drawCell(x, y, white) {
  ctx.fillStyle = white ? '#e8e8e0' : '#0f0f0f';
  ctx.fillRect(x * CELL, y * CELL, CELL, CELL);
}

// Run multiple steps per frame to reach highway faster
const STEPS_PER_FRAME = 20;

function run(ts) {
  if (!running) return;
  for (let i = 0; i < STEPS_PER_FRAME; i++) {
    const idx = ay * W + ax;
    const wasWhite = grid[idx] === 1;
    // Turn
    dir = wasWhite ? (dir + 1) % 4 : (dir + 3) % 4; // right on white, left on black
    // Flip
    grid[idx] = wasWhite ? 0 : 1;
    drawCell(ax, ay, !wasWhite);
    // Move
    ax = (ax + DX[dir] + W) % W;
    ay = (ay + DY[dir] + H) % H;
    step++;
  }
  // Draw ant position
  ctx.fillStyle = '#c8922a';
  ctx.fillRect(ax * CELL, ay * CELL, CELL, CELL);

  window.__setStatus && window.__setStatus(`step ${step.toLocaleString()}${step > 10000 ? ' — highway phase' : step > 5000 ? ' — approaching order' : ' — chaos phase'} — click to restart`);
  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
