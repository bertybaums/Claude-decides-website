// Lissajous Figures — x(t) = sin(a·t + δ), y(t) = sin(b·t)
// The ratio a:b determines the shape. When a/b is rational, the curve closes.
// The phase δ rotates the figure. Small changes in ratio produce wildly different forms.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

const PRESETS = [
  { a: 1, b: 1, d: 0,           label: 'a=1, b=1, δ=0' },
  { a: 1, b: 2, d: Math.PI / 4, label: 'a=1, b=2, δ=π/4' },
  { a: 2, b: 3, d: 0,           label: 'a=2, b=3, δ=0' },
  { a: 3, b: 4, d: Math.PI / 4, label: 'a=3, b=4, δ=π/4' },
  { a: 3, b: 5, d: Math.PI / 6, label: 'a=3, b=5, δ=π/6' },
  { a: 5, b: 6, d: Math.PI / 4, label: 'a=5, b=6, δ=π/4' },
  { a: 4, b: 5, d: 0,           label: 'a=4, b=5, δ=0' },
  { a: 5, b: 7, d: Math.PI / 3, label: 'a=5, b=7, δ=π/3' },
];

const STEPS = 2000;      // segments per full curve
const DRAW_PER_FRAME = 12;
const PAUSE_MS = 1500;
const FADE_MS = 600;

let presetIndex = 0;
let t = 0;            // current draw position in [0, 1]
let phase = 'drawing'; // 'drawing' | 'pausing' | 'fading'
let phaseStart = 0;

// Offscreen buffer for previous curve (to fade it)
let prevImage = null;

function getXY(preset, frac) {
  const tRad = frac * 2 * Math.PI * Math.max(preset.a, preset.b);
  const x = Math.sin(preset.a * tRad + preset.d);
  const y = Math.sin(preset.b * tRad);
  return [x, y];
}

function toCanvas(x, y) {
  const W = canvas.width, H = canvas.height;
  const margin = 0.1;
  const cx = W / 2 + x * W * (0.5 - margin);
  const cy = H / 2 - y * H * (0.5 - margin);
  return [cx, cy];
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  presetIndex = 0;
  t = 0;
  phase = 'drawing';
  phaseStart = 0;
  prevImage = null;

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  window.__setStatus && window.__setStatus('drawing — click to restart');
  run();
}

function startNextPreset(ts) {
  presetIndex = (presetIndex + 1) % PRESETS.length;
  t = 0;
  phase = 'drawing';
  phaseStart = ts;
  prevImage = null;
}

function run(ts = 0) {
  if (!running) return;

  const preset = PRESETS[presetIndex];

  if (phase === 'pausing') {
    if (ts - phaseStart >= PAUSE_MS) {
      // Save current canvas as image to fade from
      prevImage = ctx.getImageData(0, 0, canvas.width, canvas.height);
      phase = 'fading';
      phaseStart = ts;
    }
    animId = requestAnimationFrame(run);
    return;
  }

  if (phase === 'fading') {
    const fadeFrac = (ts - phaseStart) / FADE_MS;
    if (fadeFrac >= 1) {
      startNextPreset(ts);
    } else {
      // Fade out: overdraw background with increasing opacity
      ctx.putImageData(prevImage, 0, 0);
      ctx.fillStyle = `rgba(15,15,15,${fadeFrac})`;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
    animId = requestAnimationFrame(run);
    return;
  }

  // phase === 'drawing'
  if (t === 0) {
    // Fresh start for this preset
    ctx.fillStyle = '#0f0f0f';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  const prevFrac = t;
  const nextFrac = Math.min(t + DRAW_PER_FRAME / STEPS, 1);

  if (prevFrac >= 1) {
    phase = 'pausing';
    phaseStart = ts;
    animId = requestAnimationFrame(run);
    return;
  }

  // Draw segments from prevFrac to nextFrac
  ctx.lineWidth = 1.5;
  for (let i = 0; i < DRAW_PER_FRAME; i++) {
    const f1 = prevFrac + (i / DRAW_PER_FRAME) * (nextFrac - prevFrac);
    const f2 = prevFrac + ((i + 1) / DRAW_PER_FRAME) * (nextFrac - prevFrac);
    const [x1, y1] = toCanvas(...getXY(preset, f1));
    const [x2, y2] = toCanvas(...getXY(preset, f2));

    // Gradient: amber (#c8922a) at t=0 → white (#ffffff) at t=1
    const colorT = f2;
    const r = Math.floor(200 + colorT * 55);
    const g = Math.floor(146 + colorT * 109);
    const b = Math.floor(42  + colorT * 213);
    ctx.strokeStyle = `rgb(${r},${g},${b})`;

    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  t = nextFrac;

  window.__setStatus && window.__setStatus(
    `${preset.label} — click to restart`
  );

  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
