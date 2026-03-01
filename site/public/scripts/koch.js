// Koch Snowflake — infinite perimeter, finite area
// Each iteration replaces every edge with 4 segments of 1/3 the length.
// The perimeter grows as (4/3)^N · initial, diverging to infinity.
// The area converges. Length and area decouple completely.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

const MAX_ITER = 5;
const PAUSE_MS = 2000;

let currentIter = 0;
let waitingUntil = 0;
let phase = 'drawing'; // 'drawing' | 'pausing'

// Koch segment: recurse down to depth=0, push line endpoints
function kochPoints(x1, y1, x2, y2, depth, pts) {
  if (depth === 0) {
    if (pts.length === 0) pts.push([x1, y1]);
    pts.push([x2, y2]);
    return;
  }
  // Trisect
  const ax = x1 + (x2 - x1) / 3;
  const ay = y1 + (y2 - y1) / 3;
  const bx = x1 + 2 * (x2 - x1) / 3;
  const by = y1 + 2 * (y2 - y1) / 3;
  // Bump peak: rotate (b-a) by -60 degrees around a
  const angle = -Math.PI / 3;
  const dx = bx - ax, dy = by - ay;
  const px = ax + dx * Math.cos(angle) - dy * Math.sin(angle);
  const py = ay + dx * Math.sin(angle) + dy * Math.cos(angle);

  kochPoints(x1, y1, ax, ay, depth - 1, pts);
  kochPoints(ax, ay, px, py, depth - 1, pts);
  kochPoints(px, py, bx, by, depth - 1, pts);
  kochPoints(bx, by, x2, y2, depth - 1, pts);
}

function buildSnowflake(iter) {
  const W = canvas.width, H = canvas.height;
  const cx = W / 2, cy = H / 2;
  const r = Math.min(W, H) * 0.38;

  // Equilateral triangle vertices (pointing up)
  const v0 = [cx, cy - r];
  const v1 = [cx + r * Math.sin(2 * Math.PI / 3), cy - r * Math.cos(2 * Math.PI / 3)];
  const v2 = [cx + r * Math.sin(4 * Math.PI / 3), cy - r * Math.cos(4 * Math.PI / 3)];

  const pts = [];
  kochPoints(v0[0], v0[1], v1[0], v1[1], iter, pts);
  const pts2 = [];
  kochPoints(v1[0], v1[1], v2[0], v2[1], iter, pts2);
  pts2.shift();
  const pts3 = [];
  kochPoints(v2[0], v2[1], v0[0], v0[1], iter, pts3);
  pts3.shift();

  return pts.concat(pts2, pts3);
}

// Animated drawing state
let allPoints = [];
let drawIndex = 0;
const DRAW_PER_FRAME = 80;

function drawIteration(iter) {
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  allPoints = buildSnowflake(iter);
  drawIndex = 0;
  phase = 'drawing';
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  currentIter = 0;
  phase = 'drawing';
  waitingUntil = 0;
  allPoints = [];
  drawIndex = 0;

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  drawIteration(0);
  window.__setStatus && window.__setStatus('iteration 0 — click to restart');
  run();
}

function run(ts = 0) {
  if (!running) return;

  if (phase === 'pausing') {
    if (ts >= waitingUntil) {
      currentIter++;
      if (currentIter > MAX_ITER) currentIter = 0;
      drawIteration(currentIter);
    }
    animId = requestAnimationFrame(run);
    return;
  }

  // phase === 'drawing'
  if (drawIndex >= allPoints.length) {
    // Done drawing — pause then advance
    phase = 'pausing';
    waitingUntil = ts + PAUSE_MS;

    const perimeterRatio = Math.pow(4 / 3, currentIter).toFixed(3);
    window.__setStatus && window.__setStatus(
      `iteration ${currentIter} — perimeter × (4/3)^${currentIter} = ${perimeterRatio} — click to restart`
    );
    animId = requestAnimationFrame(run);
    return;
  }

  // Draw a batch of segments
  const end = Math.min(drawIndex + DRAW_PER_FRAME, allPoints.length);

  ctx.beginPath();
  ctx.moveTo(allPoints[Math.max(0, drawIndex - 1)][0], allPoints[Math.max(0, drawIndex - 1)][1]);
  for (let i = drawIndex; i < end; i++) {
    ctx.lineTo(allPoints[i][0], allPoints[i][1]);
  }

  // Color: amber at iter 0, shifting toward white at iter 5
  const t = currentIter / MAX_ITER;
  const r = Math.floor(200 + t * 55);
  const g = Math.floor(146 + t * 109);
  const b = Math.floor(42 + t * 213);
  ctx.strokeStyle = `rgb(${r},${g},${b})`;
  ctx.lineWidth = Math.max(0.5, 1.5 - currentIter * 0.2);
  ctx.stroke();

  drawIndex = end;

  const perimeterRatio = Math.pow(4 / 3, currentIter).toFixed(3);
  window.__setStatus && window.__setStatus(
    `iteration ${currentIter} — perimeter × (4/3)^${currentIter} = ${perimeterRatio} — click to restart`
  );

  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
