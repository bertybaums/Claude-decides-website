// Dragon Curve — infinite self-similar fold
// Fold a strip of paper in half repeatedly, always the same direction.
// Unfold and look at the edge: the Dragon Curve. At every scale, the same motif.
// The turns[i] formula encodes every fold without storing the sequence.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

let animId;
let orderIdx = 0;
const ORDERS = [3, 5, 7, 9, 11, 13, 14];

// Compute dragon curve points for given order
function dragonPoints(order, cx, cy, length) {
  const n = 1 << order;  // 2^order segments
  const turns = new Int8Array(n);

  // turns[i] = direction change at step i: +1 = left, -1 = right
  // Formula: turn[i] = 1 if bit above lowest set bit of (i+1) is 0, else -1
  for (let i = 0; i < n - 1; i++) {
    const ip1 = i + 1;
    // Bit just above the lowest set bit
    const bit = ((ip1 / (ip1 & -ip1)) >> 1) & 1;
    turns[i] = (bit === 0) ? 1 : -1;
  }

  const pts = new Float32Array((n + 1) * 2);
  let x = cx, y = cy;
  // Compute bounding box to auto-fit
  let dx = length, dy = 0;  // initial direction: right

  pts[0] = x; pts[1] = y;

  for (let i = 0; i < n; i++) {
    x += dx; y += dy;
    pts[(i + 1) * 2]     = x;
    pts[(i + 1) * 2 + 1] = y;
    if (i < n - 1) {
      const t = turns[i];
      // Rotate direction by 90 degrees: t=1 left (CCW), t=-1 right (CW)
      const ndx = -t * dy;
      const ndy =  t * dx;
      dx = ndx; dy = ndy;
    }
  }

  return pts;
}

function fitPoints(pts, W, H) {
  const n = pts.length / 2;
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  for (let i = 0; i < n; i++) {
    const x = pts[i * 2], y = pts[i * 2 + 1];
    if (x < minX) minX = x; if (x > maxX) maxX = x;
    if (y < minY) minY = y; if (y > maxY) maxY = y;
  }
  const pw = maxX - minX, ph = maxY - minY;
  const margin = 0.1;
  const scale = Math.min((W * (1 - 2 * margin)) / pw, (H * (1 - 2 * margin)) / ph);
  const offX = (W - pw * scale) / 2 - minX * scale;
  const offY = (H - ph * scale) / 2 - minY * scale;

  const scaled = new Float32Array(pts.length);
  for (let i = 0; i < pts.length; i += 2) {
    scaled[i]     = pts[i]     * scale + offX;
    scaled[i + 1] = pts[i + 1] * scale + offY;
  }
  return scaled;
}

let currentPts = null;
let drawIdx = 0;
let drawSpeed = 1;
let pauseUntil = 0;

function init() {
  cancelAnimationFrame(animId);
  orderIdx = 0;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  startOrder(ORDERS[orderIdx]);
}

function startOrder(order) {
  const W = canvas.width, H = canvas.height;
  const n = 1 << order;
  // Raw points: start at origin with step=1, then scale
  const raw = dragonPoints(order, 0, 0, 1);
  currentPts = fitPoints(raw, W, H);
  drawIdx = 0;
  // Speed: aim for ~2s to draw each order
  drawSpeed = Math.max(1, Math.floor(n / 120));
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);
  window.__setStatus && window.__setStatus(
    `order ${order} — ${n.toLocaleString()} segments — click to restart`
  );
  animId = requestAnimationFrame(frame);
}

function frame(ts) {
  if (pauseUntil > 0) {
    if (ts < pauseUntil) { animId = requestAnimationFrame(frame); return; }
    pauseUntil = 0;
    orderIdx = (orderIdx + 1) % ORDERS.length;
    startOrder(ORDERS[orderIdx]);
    return;
  }

  const pts = currentPts;
  const total = pts.length / 2 - 1;

  const end = Math.min(drawIdx + drawSpeed, total);

  ctx.lineWidth = 1;
  ctx.beginPath();
  for (let i = drawIdx; i < end; i++) {
    const t = i / total;
    // Gradient: amber → white
    const r = Math.round(200 + t * 55);
    const g = Math.round(130 + t * 125);
    const b = Math.round(20  + t * 235);
    ctx.strokeStyle = `rgb(${r},${g},${b})`;
    ctx.beginPath();
    ctx.moveTo(pts[i * 2], pts[i * 2 + 1]);
    ctx.lineTo(pts[(i + 1) * 2], pts[(i + 1) * 2 + 1]);
    ctx.stroke();
  }

  drawIdx = end;

  if (drawIdx >= total) {
    // Pause before cycling
    const order = ORDERS[orderIdx];
    const n = 1 << order;
    window.__setStatus && window.__setStatus(
      `order ${order} — ${n.toLocaleString()} segments — click to restart`
    );
    pauseUntil = ts + 2000;
    animId = requestAnimationFrame(frame);
    return;
  }

  animId = requestAnimationFrame(frame);
}

window.__programRestart = init;
init();
