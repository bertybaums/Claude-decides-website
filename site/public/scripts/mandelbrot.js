// Mandelbrot Set — rendered with smooth coloring
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

let animId, running = true;

// Smooth coloring palette
function hslToRgb(h, s, l) {
  h /= 360; s /= 100; l /= 100;
  let r, g, b;
  if (s === 0) { r = g = b = l; }
  else {
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1; if (t > 1) t -= 1;
      if (t < 1/6) return p + (q - p) * 6 * t;
      if (t < 1/2) return q;
      if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
      return p;
    };
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r = hue2rgb(p, q, h + 1/3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1/3);
  }
  return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
}

function mandelbrot(cr, ci, maxIter) {
  let zr = 0, zi = 0, i = 0;
  while (i < maxIter) {
    const zr2 = zr * zr, zi2 = zi * zi;
    if (zr2 + zi2 > 4) {
      // Smooth iteration count
      return i + 1 - Math.log2(Math.log2(Math.sqrt(zr2 + zi2)));
    }
    zi = 2 * zr * zi + ci;
    zr = zr2 - zi2 + cr;
    i++;
  }
  return -1; // in set
}

function render(cx, cy, zoom) {
  const W = canvas.width, H = canvas.height;
  const imageData = ctx.createImageData(W, H);
  const data = imageData.data;
  const maxIter = 200;
  const scale = 3.5 / (zoom * Math.min(W, H));

  for (let py = 0; py < H; py++) {
    for (let px = 0; px < W; px++) {
      const cr = (px - W / 2) * scale + cx;
      const ci = (py - H / 2) * scale + cy;
      const m = mandelbrot(cr, ci, maxIter);
      const idx = (py * W + px) * 4;
      if (m < 0) {
        data[idx] = data[idx+1] = data[idx+2] = 10;
      } else {
        const t = m / maxIter;
        const h = (270 + t * 360 * 3) % 360;
        const s = 80;
        const l = 50 + t * 25;
        const [r, g, b] = hslToRgb(h, s, l);
        data[idx] = r; data[idx+1] = g; data[idx+2] = b;
      }
      data[idx+3] = 255;
    }
  }
  ctx.putImageData(imageData, 0, 0);
}

// Slow zoom animation targeting interesting point
const targets = [
  { cx: -0.7453, cy: 0.1127, zoom: 1, zEnd: 80 },
  { cx: -0.5, cy: 0, zoom: 1, zEnd: 1 },
  { cx: 0.28693186889504513, cy: 0.01348248493612587, zoom: 1, zEnd: 60 },
];

let targetIdx = 0;
let currentZoom = 1;
let target = targets[0];

function init() {
  running = true;
  cancelAnimationFrame(animId);
  targetIdx = 0;
  target = targets[0];
  currentZoom = 1;
  window.__setStatus && window.__setStatus('rendering — click to restart');
  render(target.cx, target.cy, currentZoom);
  animLoop();
}

let lastTime = 0;
function animLoop(ts = 0) {
  if (!running) return;
  if (ts - lastTime < 150) { animId = requestAnimationFrame(animLoop); return; }
  lastTime = ts;

  currentZoom *= 1.05;
  if (currentZoom > target.zEnd) {
    targetIdx = (targetIdx + 1) % targets.length;
    target = targets[targetIdx];
    currentZoom = 1;
  }
  render(target.cx, target.cy, currentZoom);
  window.__setStatus && window.__setStatus(`zoom ×${currentZoom.toFixed(1)} — click to restart`);
  animId = requestAnimationFrame(animLoop);
}

window.__programRestart = init;
init();
