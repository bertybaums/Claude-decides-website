// Rule 30 — 1D cellular automaton
// Wolfram: output indistinguishable from random; used in Mathematica's RNG for years.

const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
const CELL = 6;
let running = true;
let row, rows, animId;

function rule30(l, c, r) {
  return (30 >> ((l << 2) | (c << 1) | r)) & 1;
}

function step(r) {
  const n = r.length;
  return r.map((_, i) => rule30(r[(i - 1 + n) % n], r[i], r[(i + 1) % n]));
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
  window.__setStatus && window.__setStatus('running — click to restart');
  run();
}

function drawRow(r, y) {
  r.forEach((cell, x) => {
    ctx.fillStyle = cell ? '#c8922a' : '#0f0f0f';
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
    // scroll
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
