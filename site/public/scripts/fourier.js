// Fourier Series — building a square wave from sine waves
// A square wave can be described as a sum of odd harmonics: f(x) = (4/π)·Σ sin((2k-1)x)/(2k-1)
// Each sine wave added brings us closer to the ideal square wave.
// The Gibbs phenomenon: the approximation always overshoots by ~9% near the jump.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

let animId;
let currentHarmonics = 1;
let pauseUntil = 0;

const HARMONIC_STAGES = [1, 3, 7, 15, 31, 63];
let stageIdx = 0;

function squareWave(x) {
  // Ideal square wave: period 2π, amplitude 1
  const mod = ((x % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
  return mod < Math.PI ? 1 : -1;
}

function fourierApprox(x, n) {
  // n odd harmonics
  let sum = 0;
  for (let k = 1; k <= n; k++) {
    const harmonic = 2 * k - 1;
    sum += Math.sin(harmonic * x) / harmonic;
  }
  return (4 / Math.PI) * sum;
}

function drawWaves(n) {
  const W = canvas.width, H = canvas.height;

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  const cy = H / 2;
  const amplitude = H * 0.38;
  const periods = 2;
  const xScale = (periods * 2 * Math.PI) / W;

  // Draw grid lines (subtle)
  ctx.strokeStyle = 'rgba(200,146,42,0.08)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(0, cy);
  ctx.lineTo(W, cy);
  ctx.stroke();

  // Draw ideal square wave — faint
  ctx.strokeStyle = 'rgba(200,200,200,0.18)';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  let first = true;
  for (let px = 0; px <= W; px++) {
    const x = px * xScale;
    const y = cy - squareWave(x) * amplitude;
    if (first) { ctx.moveTo(px, y); first = false; }
    else ctx.lineTo(px, y);
  }
  ctx.stroke();

  // Draw Fourier approximation — bright amber
  ctx.strokeStyle = '#c8922a';
  ctx.lineWidth = 2;
  ctx.beginPath();
  first = true;
  let maxY = 0;
  for (let px = 0; px <= W; px++) {
    const x = px * xScale;
    const val = fourierApprox(x, n);
    const y = cy - val * amplitude;
    if (Math.abs(val) > maxY) maxY = Math.abs(val);
    if (first) { ctx.moveTo(px, y); first = false; }
    else ctx.lineTo(px, y);
  }
  ctx.stroke();

  // Mark the Gibbs overshoot near the first discontinuity
  // The overshoot occurs just before x=π
  const gibbsX = (Math.PI - 0.05) / xScale;
  const gibbsVal = fourierApprox(Math.PI - 0.05, n);
  const gibbsY = cy - gibbsVal * amplitude;
  if (n >= 7) {
    ctx.strokeStyle = 'rgba(200,146,42,0.5)';
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 4]);
    ctx.beginPath();
    ctx.moveTo(gibbsX, cy - amplitude);      // top of ideal
    ctx.lineTo(gibbsX, gibbsY);             // actual overshoot
    ctx.stroke();
    ctx.setLineDash([]);
  }

  // Harmonic count label
  ctx.fillStyle = 'rgba(200,146,42,0.5)';
  ctx.font = `${Math.round(W * 0.018)}px monospace`;
  ctx.fillText(`${n} harmonic${n > 1 ? 's' : ''}`, 14, 22);
}

function init() {
  cancelAnimationFrame(animId);
  stageIdx = 0;
  currentHarmonics = HARMONIC_STAGES[0];
  pauseUntil = 0;
  drawWaves(currentHarmonics);
  window.__setStatus && window.__setStatus(`${currentHarmonics} harmonic — click to restart`);
  animId = requestAnimationFrame(frame);
}

function frame(ts) {
  if (pauseUntil > 0) {
    if (ts < pauseUntil) { animId = requestAnimationFrame(frame); return; }
    pauseUntil = 0;
    stageIdx = (stageIdx + 1) % HARMONIC_STAGES.length;
    currentHarmonics = HARMONIC_STAGES[stageIdx];
    drawWaves(currentHarmonics);
    window.__setStatus && window.__setStatus(
      `${currentHarmonics} harmonic${currentHarmonics > 1 ? 's' : ''} — click to restart`
    );
    pauseUntil = ts + 2200;
    animId = requestAnimationFrame(frame);
    return;
  }

  // First frame: start the first pause
  drawWaves(currentHarmonics);
  pauseUntil = ts + 2200;
  animId = requestAnimationFrame(frame);
}

window.__programRestart = init;
init();
