// Rule 110 — proven Turing-complete
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
const CELL = 5;
let row, rows, animId, running = true;

function rule110(l, c, r) {
  return (110 >> ((l << 2) | (c << 1) | r)) & 1;
}

function step(r) {
  const n = r.length;
  return r.map((_, i) => rule110(r[(i - 1 + n) % n], r[i], r[(i + 1) % n]));
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  const W = Math.floor(canvas.width / CELL);
  // Random initial condition shows Turing-complete behavior better
  row = Array.from({ length: W }, () => Math.random() < 0.5 ? 1 : 0);
  rows = [];
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  window.__setStatus && window.__setStatus('Rule 110 — Turing-complete — click to restart with new random state');
  run();
}

function drawRow(r, y) {
  r.forEach((cell, x) => {
    ctx.fillStyle = cell ? '#d4a76a' : '#0f0f0f';
    ctx.fillRect(x * CELL, y, CELL, CELL);
  });
}

let lastTime = 0;
function run(ts = 0) {
  if (!running) return;
  if (ts - lastTime < 60) { animId = requestAnimationFrame(run); return; }
  lastTime = ts;
  const maxRows = Math.floor(canvas.height / CELL);
  if (rows.length < maxRows) {
    rows.push([...row]);
    drawRow(row, (rows.length - 1) * CELL);
  } else {
    ctx.drawImage(canvas, 0, CELL, canvas.width, canvas.height - CELL, 0, 0, canvas.width, canvas.height - CELL);
    ctx.fillStyle = '#0f0f0f';
    ctx.fillRect(0, canvas.height - CELL, canvas.width, CELL);
    drawRow(row, canvas.height - CELL);
  }
  row = step(row);
  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
