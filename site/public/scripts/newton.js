// Newton Fractal — basins of attraction for z³ - 1 = 0
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let running = true;

// Three roots of z³ = 1
const ROOTS = [
  { re: 1, im: 0 },
  { re: -0.5, im: Math.sqrt(3) / 2 },
  { re: -0.5, im: -Math.sqrt(3) / 2 },
];

const ROOT_COLORS = [
  [200, 60, 60],   // red
  [60, 180, 80],   // green
  [60, 100, 220],  // blue
];

function newtonStep(re, im) {
  // z - (z³ - 1) / (3z²)
  // z³
  const re3 = re * re * re - 3 * re * im * im;
  const im3 = 3 * re * re * im - im * im * im;
  // 3z²
  const re2_3 = 3 * (re * re - im * im);
  const im2_3 = 3 * (2 * re * im);
  // (z³ - 1) / (3z²)
  const dre = re3 - 1, dim = im3;
  const denom = re2_3 * re2_3 + im2_3 * im2_3;
  const qre = (dre * re2_3 + dim * im2_3) / denom;
  const qim = (dim * re2_3 - dre * im2_3) / denom;
  return { re: re - qre, im: im - qim };
}

function findRoot(re, im) {
  let maxIter = 40;
  for (let i = 0; i < maxIter; i++) {
    const n = newtonStep(re, im);
    re = n.re; im = n.im;
    for (let r = 0; r < ROOTS.length; r++) {
      const dr = re - ROOTS[r].re, di = im - ROOTS[r].im;
      if (dr * dr + di * di < 1e-8) return { root: r, iter: i };
    }
  }
  return { root: 0, iter: maxIter };
}

function render() {
  const W = canvas.width, H = canvas.height;
  const img = ctx.createImageData(W, H);
  const d = img.data;
  const scale = 3.0 / Math.min(W, H);

  for (let py = 0; py < H; py++) {
    for (let px = 0; px < W; px++) {
      const re = (px - W / 2) * scale;
      const im = (py - H / 2) * scale;
      const { root, iter } = findRoot(re, im);
      const brightness = 0.3 + 0.7 * (1 - iter / 40);
      const [r, g, b] = ROOT_COLORS[root].map(c => Math.floor(c * brightness));
      const idx = (py * W + px) * 4;
      d[idx] = r; d[idx+1] = g; d[idx+2] = b; d[idx+3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
}

function init() {
  window.__setStatus && window.__setStatus("Newton's method on z³=1 — three basins of attraction — click to re-render");
  render();
}

window.__programRestart = init;
init();
