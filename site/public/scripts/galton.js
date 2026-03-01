// Galton Board — Binomial Distribution
// Balls fall through rows of pegs, bouncing left or right randomly.
// Accumulate in bins forming the normal (bell) distribution.
// ~500 balls total. Animate each ball dropping.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const ROWS = 12;
const TOTAL_BALLS = 500;
const BINS = ROWS + 1;

let balls, bins, binMax, landed, launching, totalLaunched;

// Layout constants (computed in init)
let pegRadius, ballRadius, boardTop, boardBottom, pegSpacingX, pegSpacingY;
let binHeight, boardLeft, boardWidth, binW;

function pegPos(row, col) {
  // row 0 is top peg, col goes from 0 to row
  const cx = canvas.width / 2 + (col - row / 2) * pegSpacingX;
  const cy = boardTop + (row + 0.5) * pegSpacingY;
  return [cx, cy];
}

function binomial(n, k) {
  if (k < 0 || k > n) return 0;
  let r = 1;
  for (let i = 0; i < k; i++) {
    r = r * (n - i) / (i + 1);
  }
  return r;
}

function init() {
  cancelAnimationFrame(animId);
  const W = canvas.width, H = canvas.height;

  pegSpacingX = Math.min(W / (BINS + 2), 44);
  pegSpacingY = H * 0.5 / (ROWS + 1);
  pegRadius = 3;
  ballRadius = 4;
  boardTop = H * 0.06;
  boardBottom = H * 0.7;
  binHeight = H * 0.22;
  boardLeft = W / 2 - pegSpacingX * ROWS / 2;
  boardWidth = pegSpacingX * ROWS;
  binW = boardWidth / BINS;

  balls = [];
  bins = new Array(BINS).fill(0);
  binMax = 1;
  landed = 0;
  totalLaunched = 0;
  launching = true;

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  window.__setStatus && window.__setStatus('0 balls — bell curve forming — click to restart');
  run();
}

function launchBall() {
  if (totalLaunched >= TOTAL_BALLS) { launching = false; return; }
  const [cx, cy] = pegPos(0, 0);
  const startX = canvas.width / 2;
  balls.push({
    x: startX, y: boardTop - 20,
    vx: 0, vy: 1.5,
    row: -1, col: 0,  // which peg row we're approaching
    landed: false,
    targetRow: 0,
    path: [],  // sequence of L/R choices
    binIdx: null,
  });
  totalLaunched++;
}

function updateBall(b) {
  if (b.landed) return;

  // Animate toward target peg or bin
  const nextRow = b.path.length;

  if (nextRow < ROWS) {
    // Moving toward next row's peg
    const choice = b.path.length === 0 ? null : b.path[b.path.length - 1];
    // Determine which peg we're heading to
    const pegCol = b.path.filter(v => v === 1).length;
    const [tx, ty] = pegPos(nextRow, pegCol);

    b.vy += 0.15; // gravity
    b.x += (tx - b.x) * 0.15;
    b.y += b.vy;

    const dist = Math.hypot(b.x - tx, b.y - ty);
    if (dist < pegRadius + ballRadius + 2) {
      // Bounce off peg — random left or right
      const go = Math.random() < 0.5 ? 0 : 1;
      b.path.push(go);
      b.vy = 1.8;
      b.vx = (go === 0 ? -1 : 1) * 0.5;
    }
  } else {
    // Falling into bin
    const finalCol = b.path.filter(v => v === 1).length;
    const binCx = boardLeft + (finalCol + 0.5) * binW;
    const binTop = boardBottom;
    const stackY = binTop + binHeight - bins[finalCol] * (ballRadius * 2.2) - ballRadius;

    b.x += (binCx - b.x) * 0.12;
    b.vy += 0.2;
    b.y += b.vy;

    if (b.y >= stackY) {
      b.y = stackY;
      b.landed = true;
      b.binIdx = finalCol;
      bins[finalCol]++;
      if (bins[finalCol] > binMax) binMax = bins[finalCol];
      landed++;
    }
  }
}

let frameCount = 0;

function run() {
  const W = canvas.width, H = canvas.height;

  ctx.fillStyle = 'rgba(15,15,15,0.55)';
  ctx.fillRect(0, 0, W, H);

  // Draw pegs
  ctx.fillStyle = '#555';
  for (let row = 0; row < ROWS; row++) {
    for (let col = 0; col <= row; col++) {
      const [px, py] = pegPos(row, col);
      ctx.beginPath();
      ctx.arc(px, py, pegRadius, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // Draw bins (ground line)
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 1;
  for (let i = 0; i <= BINS; i++) {
    const bx = boardLeft + i * binW;
    ctx.beginPath();
    ctx.moveTo(bx, boardBottom);
    ctx.lineTo(bx, boardBottom + binHeight);
    ctx.stroke();
  }
  ctx.beginPath();
  ctx.moveTo(boardLeft, boardBottom);
  ctx.lineTo(boardLeft + boardWidth, boardBottom);
  ctx.stroke();

  // Draw expected binomial distribution (amber outline)
  const maxProb = binomial(ROWS, Math.floor(ROWS / 2)) / Math.pow(2, ROWS);
  ctx.strokeStyle = 'rgba(200,146,42,0.6)';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  for (let i = 0; i < BINS; i++) {
    const prob = binomial(ROWS, i) / Math.pow(2, ROWS);
    const bh = (prob / maxProb) * (binHeight - 4);
    const bx = boardLeft + (i + 0.5) * binW;
    const by = boardBottom + binHeight - bh;
    if (i === 0) ctx.moveTo(bx, by); else ctx.lineTo(bx, by);
  }
  ctx.stroke();

  // Draw accumulated balls in bins (solid fill)
  for (let i = 0; i < BINS; i++) {
    if (bins[i] === 0) continue;
    const fillH = Math.min(bins[i] * (ballRadius * 2.2), binHeight - 2);
    const bx = boardLeft + i * binW + 1;
    const bw = binW - 2;
    const by = boardBottom + binHeight - fillH;
    const frac = i / (BINS - 1);
    const r = Math.floor(150 + frac * 50 * Math.sin(frac * Math.PI));
    ctx.fillStyle = `rgb(${200 - i * 4},${100 + i * 4},${42})`;
    ctx.fillRect(bx, by, bw, fillH);
  }

  // Draw active balls
  for (const b of balls) {
    if (!b.landed) {
      ctx.fillStyle = '#e8e0d0';
      ctx.beginPath();
      ctx.arc(b.x, b.y, ballRadius, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // Launch new balls
  frameCount++;
  if (launching && frameCount % 4 === 0 && balls.filter(b => !b.landed).length < 15) {
    launchBall();
  }

  for (const b of balls) updateBall(b);

  window.__setStatus && window.__setStatus(`${landed} balls — bell curve forming — click to restart`);

  if (landed < TOTAL_BALLS || balls.some(b => !b.landed)) {
    animId = requestAnimationFrame(run);
  } else {
    window.__setStatus && window.__setStatus(`${landed} balls — normal distribution — click to restart`);
  }
}

canvas.addEventListener('click', init);
window.__programRestart = init;
init();
