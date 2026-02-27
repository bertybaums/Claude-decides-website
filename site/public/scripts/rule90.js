// Rule 90 — Sierpiński triangle via XOR of neighbors
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
const CELL = 4;
let row, rows, animId, running = true;

function rule90(l, c, r) {
  return (l ^ r); // Rule 90: XOR of neighbors
}

function step(r) {
  const n = r.length;
  return r.map((_, i) => rule90(r[(i - 1 + n) % n], r[i], r[(i + 1) % n]));
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  const W = Math.floor(canvas.width / CELL);
  row = new Array(W).fill(0);
  row[Math.floor(W / 2)] = 1;
  rows = [];
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  window.__setStatus && window.__setStatus('Rule 90 — Sierpiński triangle from XOR — click to restart');
  run();
}

function drawRow(r, y) {
  r.forEach((cell, x) => {
    ctx.fillStyle = cell ? '#7eb8d4' : '#0f0f0f';
    ctx.fillRect(x * CELL, y, CELL, CELL);
  });
}

let lastTime = 0;
function run(ts = 0) {
  if (!running) return;
  if (ts - lastTime < 50) { animId = requestAnimationFrame(run); return; }
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
