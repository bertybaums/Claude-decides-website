// Harmonic Overtones — the physics inside musical tuning
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, t = 0, running = true;

const FUNDAMENTAL = 110; // Hz (A2)
const OVERTONES = 8;

function init() {
  running = true;
  cancelAnimationFrame(animId);
  t = 0;
  window.__setStatus && window.__setStatus('overtone series — 1f, 2f, 3f, 4f… — click to restart');
  run();
}

const NOTE_NAMES = ['A', 'A', 'E', 'A', 'C#', 'E', 'G♭', 'A'];
const INTERVAL_RATIOS = ['1:1', '2:1', '3:2', '4:3', '5:4', '6:5', '7:6', '8:7'];

function run(ts = 0) {
  if (!running) return;
  const W = canvas.width, H = canvas.height;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  t += 0.03;

  const waveH = H * 0.55;
  const waveY = H * 0.4;

  // Draw individual overtones
  for (let h = 1; h <= OVERTONES; h++) {
    const amplitude = 1 / h;
    const freq = h; // relative to fundamental
    const y0 = H * 0.08 + (h - 1) * (H * 0.06);
    const trackH = H * 0.045;

    // Color
    const hue = (h - 1) * 40;
    ctx.strokeStyle = `hsl(${hue}, 70%, 55%)`;
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (let px = 0; px < W; px++) {
      const x = px / W * 4 * Math.PI;
      const y = y0 + trackH / 2 - Math.sin(x * freq + t * freq) * trackH * 0.4;
      px === 0 ? ctx.moveTo(px, y) : ctx.lineTo(px, y);
    }
    ctx.stroke();

    // Labels
    ctx.fillStyle = `hsl(${hue}, 70%, 55%)`;
    ctx.font = '10px monospace';
    ctx.textAlign = 'left';
    ctx.fillText(`${h}f  ${NOTE_NAMES[h-1]}  (${FUNDAMENTAL * h}Hz)`, 4, y0 + 3);
  }

  // Draw composite wave
  ctx.strokeStyle = '#c8922a';
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let px = 0; px < W; px++) {
    const x = px / W * 4 * Math.PI;
    let y = 0;
    for (let h = 1; h <= OVERTONES; h++) y += Math.sin(x * h + t * h) / h;
    const cy = waveY + waveH / 2 - y * waveH * 0.18;
    px === 0 ? ctx.moveTo(px, cy) : ctx.lineTo(px, cy);
  }
  ctx.stroke();

  ctx.fillStyle = '#666';
  ctx.font = '11px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(`Σ sin(nt)/n for n=1…${OVERTONES}  —  Fourier series approximation`, W / 2, H - 10);

  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
