// Chladni Figures — vibrational modes of a square plate
// f(x,y) = cos(m·π·x)·cos(n·π·y) + cos(n·π·x)·cos(m·π·y)
// Sand collects at nodal lines where |f(x,y)| ≈ 0.
// These patterns were first shown by Ernst Chladni with a violin bow and sand.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

let animId;
let modeIndex = 0;
let cycleTimer = null;

const MODES = [
  { m: 1, n: 2, label: 'two lines' },
  { m: 1, n: 3, label: 'three regions' },
  { m: 2, n: 3, label: 'six lobes' },
  { m: 1, n: 4, label: 'four regions' },
  { m: 3, n: 4, label: 'twelve lobes' },
  { m: 2, n: 5, label: 'ten regions' },
];

const SAND_THRESHOLD = 0.08;  // |f| below this = sand

function renderMode(m, n) {
  const W = canvas.width, H = canvas.height;
  const imageData = ctx.createImageData(W, H);
  const data = imageData.data;
  const PI = Math.PI;

  for (let py = 0; py < H; py++) {
    for (let px = 0; px < W; px++) {
      // Map pixel to [0,1] x [0,1]
      const x = px / (W - 1);
      const y = py / (H - 1);

      const val = Math.cos(m * PI * x) * Math.cos(n * PI * y)
                + Math.cos(n * PI * x) * Math.cos(m * PI * y);

      const absVal = Math.abs(val);
      const idx = (py * W + px) * 4;

      if (absVal < SAND_THRESHOLD) {
        // Sand region: dark brownish-gray
        const t = absVal / SAND_THRESHOLD;
        data[idx]   = Math.round(30 + t * 20);
        data[idx+1] = Math.round(25 + t * 15);
        data[idx+2] = Math.round(20 + t * 10);
      } else {
        // Plate region: warm amber-ish glow, brighter further from nodal line
        const t = Math.min(1, (absVal - SAND_THRESHOLD) / (1 - SAND_THRESHOLD));
        const bright = t * t; // gamma
        data[idx]   = Math.round(15 + bright * 185);   // red channel: amber
        data[idx+1] = Math.round(10 + bright * 100);   // green: muted
        data[idx+2] = Math.round(5  + bright * 20);    // blue: very low
      }
      data[idx+3] = 255;
    }
  }

  ctx.putImageData(imageData, 0, 0);
}

function showMode(idx) {
  const mode = MODES[idx];
  renderMode(mode.m, mode.n);
  window.__setStatus && window.__setStatus(
    `Mode (${mode.m},${mode.n}) — ${mode.label} — click to restart`
  );
}

function startCycle() {
  showMode(modeIndex);
  cycleTimer = setInterval(() => {
    modeIndex = (modeIndex + 1) % MODES.length;
    showMode(modeIndex);
  }, 3000);
}

function init() {
  cancelAnimationFrame(animId);
  clearInterval(cycleTimer);
  modeIndex = 0;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  startCycle();
}

window.__programRestart = init;
init();
