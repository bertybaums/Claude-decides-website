// Hilbert Curve — space-filling curve
// A continuous path that visits every point in a square grid exactly once.
// At each iteration, the curve is 4× as long and fills the space 4× more densely.
// In the limit: a curve of infinite length that passes through every point in a square.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

let animId;
let orderIdx = 0;
const ORDERS = [1, 2, 3, 4, 5, 6];

// Map Hilbert index d to (x,y) in n×n grid
function d2xy(n, d) {
  let x = 0, y = 0, s = 1;
  while (s < n) {
    const rx = (d & 2) ? 1 : 0;
    const ry = ((d & 1) ^ rx) ? 1 : 0;
    if (!ry) {
      if (rx) { x = s - 1 - x; y = s - 1 - y; }
      const tmp = x; x = y; y = tmp;
    }
    x += s * rx;
    y += s * ry;
    d >>= 2;
    s *= 2;
  }
  return [x, y];
}

function buildCurve(order) {
  const n = 1 << order;  // grid size
  const total = n * n;
  const pts = new Float32Array(total * 2);
  for (let d = 0; d < total; d++) {
    const [x, y] = d2xy(n, d);
    pts[d * 2]     = x;
    pts[d * 2 + 1] = y;
  }
  return { pts, n, total };
}

function scalePts(pts, total, n, W, H) {
  const margin = 0.06;
  const available = Math.min(W * (1 - 2 * margin), H * (1 - 2 * margin));
  const cellSize = available / (n - 1 + 0.001);
  const offX = (W - available) / 2;
  const offY = (H - available) / 2;

  const scaled = new Float32Array(total * 2);
  for (let i = 0; i < total; i++) {
    scaled[i * 2]     = offX + pts[i * 2]     * cellSize;
    scaled[i * 2 + 1] = offY + pts[i * 2 + 1] * cellSize;
  }
  return scaled;
}

let currentPts = null;
let currentTotal = 0;
let drawIdx = 0;
let drawSpeed = 1;
let pauseUntil = 0;
let currentOrder = 1;

function init() {
  cancelAnimationFrame(animId);
  orderIdx = 0;
  pauseUntil = 0;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  startOrder(ORDERS[0]);
}

function startOrder(order) {
  const W = canvas.width, H = canvas.height;
  const { pts, n, total } = buildCurve(order);
  currentPts = scalePts(pts, total, n, W, H);
  currentTotal = total;
  drawIdx = 0;
  currentOrder = order;

  // Speed: aim for ~1.5s to draw each order
  drawSpeed = Math.max(1, Math.floor(total / 90));

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  const gridN = n;
  window.__setStatus && window.__setStatus(
    `Order ${order} — ${gridN}×${gridN} grid, ${total.toLocaleString()} points — click to restart`
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
  const total = currentTotal;
  const end = Math.min(drawIdx + drawSpeed, total - 1);

  ctx.lineWidth = currentOrder <= 3 ? 2 : currentOrder <= 5 ? 1.5 : 1;
  for (let i = drawIdx; i < end; i++) {
    const t = i / (total - 1);
    // Gradient: amber → white
    const r = Math.round(200 + t * 55);
    const g = Math.round(130 + t * 125);
    const b = Math.round(20  + t * 235);
    ctx.strokeStyle = `rgb(${r},${g},${b})`;
    ctx.beginPath();
    ctx.moveTo(pts[i * 2],       pts[i * 2 + 1]);
    ctx.lineTo(pts[(i+1) * 2],   pts[(i+1) * 2 + 1]);
    ctx.stroke();
  }

  drawIdx = end;

  if (drawIdx >= total - 1) {
    const n = 1 << currentOrder;
    window.__setStatus && window.__setStatus(
      `Order ${currentOrder} — ${n}×${n} grid, ${total.toLocaleString()} points — click to restart`
    );
    pauseUntil = ts + 2000;
    animId = requestAnimationFrame(frame);
    return;
  }

  animId = requestAnimationFrame(frame);
}

window.__programRestart = init;
init();
