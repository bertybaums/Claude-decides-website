// Knight's Tour — Warnsdorff's Heuristic
// Start at a random square. Always move to neighbor with fewest onward moves.
// Draw path stroke by stroke. Color from dark (start) to bright (end).
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const BOARD = 8;
const MOVES = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]];

let path, drawStep, cellW, cellH, offX, offY, failed;

function validMoves(visited, r, c) {
  const result = [];
  for (const [dr, dc] of MOVES) {
    const nr = r + dr, nc = c + dc;
    if (nr >= 0 && nr < BOARD && nc >= 0 && nc < BOARD && !visited[nr * BOARD + nc]) {
      result.push([nr, nc]);
    }
  }
  return result;
}

function warnsdorff(sr, sc) {
  const visited = new Uint8Array(BOARD * BOARD);
  const p = [[sr, sc]];
  visited[sr * BOARD + sc] = 1;

  for (let step = 1; step < BOARD * BOARD; step++) {
    const [r, c] = p[p.length - 1];
    const moves = validMoves(visited, r, c);
    if (moves.length === 0) return p; // failed

    // Sort by number of onward moves (Warnsdorff)
    moves.sort((m1, m2) => {
      // Temporarily mark current to not double-count
      visited[m1[0] * BOARD + m1[1]] = 1;
      const d1 = validMoves(visited, m1[0], m1[1]).length;
      visited[m1[0] * BOARD + m1[1]] = 0;

      visited[m2[0] * BOARD + m2[1]] = 1;
      const d2 = validMoves(visited, m2[0], m2[1]).length;
      visited[m2[0] * BOARD + m2[1]] = 0;

      return d1 - d2;
    });

    const [nr, nc] = moves[0];
    visited[nr * BOARD + nc] = 1;
    p.push([nr, nc]);
  }
  return p;
}

function stepColor(i, total) {
  const t = i / Math.max(1, total - 1);
  // Dark amber → bright gold
  const r = Math.floor(80 + t * 175);
  const g = Math.floor(40 + t * 160);
  const b = Math.floor(0 + t * 40);
  return `rgb(${r},${g},${b})`;
}

function squareCenter(r, c) {
  return [offX + (c + 0.5) * cellW, offY + (r + 0.5) * cellH];
}

function drawBoard() {
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (let r = 0; r < BOARD; r++) {
    for (let c = 0; c < BOARD; c++) {
      const isLight = (r + c) % 2 === 0;
      ctx.fillStyle = isLight ? '#1e1e1e' : '#141414';
      ctx.fillRect(offX + c * cellW, offY + r * cellH, cellW, cellH);
    }
  }

  // Grid lines
  ctx.strokeStyle = '#2a2a2a';
  ctx.lineWidth = 0.5;
  for (let i = 0; i <= BOARD; i++) {
    ctx.beginPath();
    ctx.moveTo(offX + i * cellW, offY);
    ctx.lineTo(offX + i * cellW, offY + BOARD * cellH);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(offX, offY + i * cellH);
    ctx.lineTo(offX + BOARD * cellW, offY + i * cellH);
    ctx.stroke();
  }
}

function init() {
  cancelAnimationFrame(animId);
  const W = canvas.width, H = canvas.height;
  const boardSize = Math.min(W, H) * 0.85;
  cellW = boardSize / BOARD;
  cellH = boardSize / BOARD;
  offX = (W - boardSize) / 2;
  offY = (H - boardSize) / 2;

  // Random starting square
  const sr = Math.floor(Math.random() * BOARD);
  const sc = Math.floor(Math.random() * BOARD);
  path = warnsdorff(sr, sc);
  failed = path.length < BOARD * BOARD;
  drawStep = 0;

  drawBoard();
  window.__setStatus && window.__setStatus(`step 0/${BOARD*BOARD} — start (${sr},${sc}) — click to restart`);
  run();
}

const STEPS_PER_FRAME = 2;

function run() {
  for (let s = 0; s < STEPS_PER_FRAME && drawStep < path.length - 1; s++) {
    const [r1, c1] = path[drawStep];
    const [r2, c2] = path[drawStep + 1];
    const [x1, y1] = squareCenter(r1, c1);
    const [x2, y2] = squareCenter(r2, c2);

    ctx.strokeStyle = stepColor(drawStep, path.length);
    ctx.lineWidth = 2.5;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();

    // Draw dot at current position
    ctx.fillStyle = stepColor(drawStep + 1, path.length);
    ctx.beginPath();
    ctx.arc(x2, y2, 4, 0, Math.PI * 2);
    ctx.fill();

    drawStep++;
  }

  // Draw start marker
  if (path.length > 0) {
    const [sr, sc] = path[0];
    const [sx, sy] = squareCenter(sr, sc);
    ctx.strokeStyle = '#888';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(sx, sy, 7, 0, Math.PI * 2);
    ctx.stroke();
  }

  const status = failed
    ? `partial tour — ${path.length}/${BOARD*BOARD} — click to restart`
    : `step ${drawStep}/${BOARD*BOARD} — click to restart`;
  window.__setStatus && window.__setStatus(status);

  if (drawStep < path.length - 1) {
    animId = requestAnimationFrame(run);
  } else {
    const complete = path.length === BOARD * BOARD ? 'complete tour' : `partial: ${path.length}/64`;
    window.__setStatus && window.__setStatus(`${complete} — Warnsdorff's heuristic — click to restart`);
  }
}

canvas.addEventListener('click', init);
window.__programRestart = init;
init();
