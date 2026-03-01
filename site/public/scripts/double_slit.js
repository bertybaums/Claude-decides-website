// Double-Slit Interference
// Two coherent wave sources at the slits → interference pattern on a screen.
// Intensity = (amplitude₁ + amplitude₂)² — bright where waves reinforce,
// dark where they cancel. Same pattern appears for light, electrons, atoms.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const AMBER = '#c8922a';
const BG = '#0f0f0f';
const WHITE = '#e8e4dc';
const DIMTEXT = '#6b6560';

const W = canvas.width;
const H = canvas.height;

// Physical parameters (in pixel units)
const WAVELENGTH = 28;      // lambda — wave spacing
const SLIT_SEP = 60;        // distance between slits
const BARRIER_X = Math.floor(W * 0.38);
const SLIT_Y1 = H / 2 - SLIT_SEP / 2;
const SLIT_Y2 = H / 2 + SLIT_SEP / 2;
const SLIT_WIDTH = 4;       // slit opening height

// Pre-compute the static interference pattern (right of barrier)
// and the incident wave (left of barrier)
let imageData = null;
let waveTime = 0;
let running = true;

function amplitude(x, y, t) {
  // Left of barrier: plane wave moving right
  if (x < BARRIER_X - 2) {
    const k = 2 * Math.PI / WAVELENGTH;
    const omega = k; // speed = 1
    return Math.sin(k * x - omega * t);
  }
  return 0;
}

function diffracted(x, y, t) {
  // Right of barrier: two point sources at slits
  const k = 2 * Math.PI / WAVELENGTH;
  const omega = k;

  const r1 = Math.hypot(x - BARRIER_X, y - SLIT_Y1);
  const r2 = Math.hypot(x - BARRIER_X, y - SLIT_Y2);

  const d1 = Math.max(r1, 1);
  const d2 = Math.max(r2, 1);

  const a1 = Math.sin(k * r1 - omega * t) / Math.sqrt(d1);
  const a2 = Math.sin(k * r2 - omega * t) / Math.sqrt(d2);

  return (a1 + a2);
}

// Precompute intensity map (time-averaged) for persistent glow
function buildIntensityMap() {
  const imap = new Float32Array(W * H);
  const k = 2 * Math.PI / WAVELENGTH;

  // Sample multiple phases for time-averaged intensity
  const nPhases = 16;
  for (let tp = 0; tp < nPhases; tp++) {
    const t = tp * WAVELENGTH / nPhases;
    const omega = k;

    for (let y = 0; y < H; y++) {
      for (let x = BARRIER_X + 2; x < W; x++) {
        const r1 = Math.hypot(x - BARRIER_X, y - SLIT_Y1);
        const r2 = Math.hypot(x - BARRIER_X, y - SLIT_Y2);
        const d1 = Math.max(r1, 1);
        const d2 = Math.max(r2, 1);
        const a1 = Math.sin(k * r1 - omega * t) / Math.sqrt(d1);
        const a2 = Math.sin(k * r2 - omega * t) / Math.sqrt(d2);
        const A = a1 + a2;
        imap[y * W + x] += A * A / nPhases;
      }
    }
  }

  // Normalize
  let maxI = 0;
  for (let i = 0; i < imap.length; i++) if (imap[i] > maxI) maxI = imap[i];
  const scale = maxI > 0 ? 1 / maxI : 1;
  for (let i = 0; i < imap.length; i++) imap[i] *= scale;

  return imap;
}

// Build the intensity map once
let intensityMap = null;
let buildStarted = false;

function buildAndDraw() {
  if (!buildStarted) {
    buildStarted = true;
    window.__setStatus && window.__setStatus('computing interference pattern...');
    // Build async-ish via setTimeout to let status update
    setTimeout(() => {
      intensityMap = buildIntensityMap();
      window.__setStatus && window.__setStatus('interference pattern — click to restart');
      animId = requestAnimationFrame(animate);
    }, 20);
  }
}

function isBarrier(x, y) {
  if (x < BARRIER_X - 1 || x > BARRIER_X + 1) return false;
  // Is this in a slit?
  if (Math.abs(y - SLIT_Y1) < SLIT_WIDTH / 2) return false;
  if (Math.abs(y - SLIT_Y2) < SLIT_WIDTH / 2) return false;
  return true;
}

function animate(ts) {
  if (!running || !intensityMap) return;
  waveTime += 0.6;

  const data = ctx.createImageData(W, H);
  const d = data.data;
  const k = 2 * Math.PI / WAVELENGTH;

  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      const idx = (y * W + x) * 4;

      if (isBarrier(x, y)) {
        // Barrier — solid dim
        d[idx] = 40; d[idx+1] = 35; d[idx+2] = 30; d[idx+3] = 255;
        continue;
      }

      let r = 0, g = 0, b = 0;

      if (x < BARRIER_X - 2) {
        // Incident plane wave — animated
        const A = Math.sin(k * x - waveTime);
        // Map to blue-white wave
        const intensity = (A + 1) / 2;
        r = Math.round(20 + intensity * 60);
        g = Math.round(40 + intensity * 80);
        b = Math.round(80 + intensity * 140);
      } else if (x >= BARRIER_X + 2) {
        // Diffracted region — blend static intensity with animated wave
        const staticI = intensityMap[y * W + x] || 0;

        // Animated wave amplitude at this point
        const r1 = Math.hypot(x - BARRIER_X, y - SLIT_Y1);
        const r2 = Math.hypot(x - BARRIER_X, y - SLIT_Y2);
        const d1 = Math.max(r1, 1);
        const d2 = Math.max(r2, 1);
        const a1 = Math.sin(k * r1 - waveTime) / Math.sqrt(d1);
        const a2 = Math.sin(k * r2 - waveTime) / Math.sqrt(d2);
        const wave = (a1 + a2);
        const wNorm = Math.max(0, Math.min(1, (wave * 0.5 + 1) * 0.5));

        // Combine: static intensity for glow + animated wave for movement
        const combined = staticI * 0.7 + wNorm * staticI * 0.5;
        const t = Math.min(1, combined);

        // Color: amber at bright bands
        r = Math.round(t * 200 + wNorm * 30);
        g = Math.round(t * 146 + wNorm * 20);
        b = Math.round(t * 42 + wNorm * 15);
      } else {
        r = 15; g = 12; b = 10;
      }

      d[idx] = r; d[idx+1] = g; d[idx+2] = b; d[idx+3] = 255;
    }
  }

  ctx.putImageData(data, 0, 0);

  // Overlay text
  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText('Double-Slit Interference', 20, 26);

  ctx.fillStyle = DIMTEXT;
  ctx.font = '11px monospace';
  ctx.fillText(`λ = ${WAVELENGTH}px   slit sep = ${SLIT_SEP}px`, 20, 46);

  // Labels
  ctx.fillStyle = '#4488cc';
  ctx.font = '11px monospace';
  ctx.fillText('incident', 20, H / 2);
  ctx.fillText('wave', 20, H / 2 + 14);

  ctx.fillStyle = AMBER;
  ctx.fillText('interference', BARRIER_X + 20, H / 2 - SLIT_SEP * 0.8);
  ctx.fillText('pattern', BARRIER_X + 20, H / 2 - SLIT_SEP * 0.8 + 14);

  // Barrier label
  ctx.fillStyle = '#555';
  ctx.font = '10px monospace';
  ctx.save();
  ctx.translate(BARRIER_X - 8, H / 2 - SLIT_SEP * 1.6);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText('barrier', 0, 0);
  ctx.restore();

  // Slit markers
  ctx.strokeStyle = '#ffffff44';
  ctx.lineWidth = 1;
  ctx.setLineDash([2, 3]);
  for (const sy of [SLIT_Y1, SLIT_Y2]) {
    ctx.beginPath();
    ctx.moveTo(BARRIER_X, sy);
    ctx.lineTo(W - 10, sy);
    ctx.stroke();
  }
  ctx.setLineDash([]);

  // Screen profile bar on right edge
  const SCREEN_X = W - 14;
  const maxI = Math.max(...Array.from({length: H}, (_, y) => intensityMap[y * W + Math.min(W - 20, W - 1)] || 0));
  for (let y = 0; y < H; y++) {
    const iVal = intensityMap[y * W + W - 20] || 0;
    const t = maxI > 0 ? iVal / maxI : 0;
    ctx.fillStyle = `rgba(200, 146, 42, ${t * 0.9})`;
    ctx.fillRect(SCREEN_X, y, 12, 1);
  }
  ctx.fillStyle = DIMTEXT;
  ctx.font = '9px monospace';
  ctx.fillText('screen', SCREEN_X - 12, 16);

  window.__setStatus && window.__setStatus('interference pattern — click to restart');
  animId = requestAnimationFrame(animate);
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  buildStarted = false;
  intensityMap = null;
  waveTime = 0;

  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText('Double-Slit Interference', 20, 26);
  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  ctx.fillText('computing...', 20, 50);

  buildAndDraw();
}

window.__programRestart = init;
init();
