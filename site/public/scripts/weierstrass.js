// Weierstrass Function — continuous everywhere, differentiable nowhere
// f(x) = Σ a^n · cos(b^n · π · x),  a=0.85, b=7
// Each new term adds finer and finer oscillations. The limit is a fractal curve:
// visually jagged at every scale, yet it passes through every x without a gap.
// The gap: a function can be a rule (the sum) without ever having a slope.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

const A = 0.85;
const B = 7;
const MAX_TERMS = 12;
const PAUSE_MS = 1500;
const X_MIN = 0, X_MAX = 2;
const Y_MIN = -3, Y_MAX = 3;

let currentTerms = 1;
let phase = 'drawing';  // 'drawing' | 'pausing'
let phaseStart = 0;

// History of all drawn curves (for fade effect)
let curveHistory = []; // each entry: { terms, imageData }

// Compute partial sum at x
function weierstrass(x, nTerms) {
  let sum = 0;
  for (let n = 0; n < nTerms; n++) {
    sum += Math.pow(A, n) * Math.cos(Math.pow(B, n) * Math.PI * x);
  }
  return sum;
}

function toCanvasX(x) {
  return (x - X_MIN) / (X_MAX - X_MIN) * canvas.width;
}

function toCanvasY(y) {
  return canvas.height - (y - Y_MIN) / (Y_MAX - Y_MIN) * canvas.height;
}

const SAMPLE_POINTS = 1200;

function getCurvePoints(nTerms) {
  const pts = [];
  for (let i = 0; i <= SAMPLE_POINTS; i++) {
    const x = X_MIN + (i / SAMPLE_POINTS) * (X_MAX - X_MIN);
    const y = weierstrass(x, nTerms);
    pts.push([toCanvasX(x), toCanvasY(y)]);
  }
  return pts;
}

function drawAllCurves(nTerms) {
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw faded previous curves
  for (let i = 0; i < curveHistory.length; i++) {
    const age = curveHistory.length - i; // 1 = most recent previous
    const alpha = Math.max(0.04, 0.25 / age);
    const pts = curveHistory[i];

    ctx.beginPath();
    ctx.moveTo(pts[0][0], pts[0][1]);
    for (let j = 1; j < pts.length; j++) {
      ctx.lineTo(pts[j][0], pts[j][1]);
    }
    // Faded amber for old curves
    ctx.strokeStyle = `rgba(200,146,42,${alpha})`;
    ctx.lineWidth = 0.7;
    ctx.stroke();
  }

  // Draw current (bright) curve
  const pts = getCurvePoints(nTerms);
  ctx.beginPath();
  ctx.moveTo(pts[0][0], pts[0][1]);
  for (let j = 1; j < pts.length; j++) {
    ctx.lineTo(pts[j][0], pts[j][1]);
  }

  // Color shifts from amber (1 term) toward bright white (12 terms)
  const t = (nTerms - 1) / (MAX_TERMS - 1);
  const r = Math.floor(200 + t * 55);
  const g = Math.floor(146 + t * 109);
  const b = Math.floor(42  + t * 213);
  ctx.strokeStyle = `rgb(${r},${g},${b})`;
  ctx.lineWidth = 1.5;
  ctx.stroke();

  // Grid lines (subtle)
  ctx.strokeStyle = 'rgba(60,60,60,0.4)';
  ctx.lineWidth = 0.5;
  // y=0 axis
  ctx.beginPath();
  ctx.moveTo(0, toCanvasY(0));
  ctx.lineTo(canvas.width, toCanvasY(0));
  ctx.stroke();

  return pts;
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  currentTerms = 1;
  phase = 'drawing';
  phaseStart = 0;
  curveHistory = [];

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  window.__setStatus && window.__setStatus('1 term — click to restart');
  run();
}

function run(ts = 0) {
  if (!running) return;

  if (phase === 'pausing') {
    if (ts - phaseStart >= PAUSE_MS) {
      // Save current curve to history before advancing
      curveHistory.push(getCurvePoints(currentTerms));
      // Keep history bounded
      if (curveHistory.length > MAX_TERMS) curveHistory.shift();

      currentTerms++;
      if (currentTerms > MAX_TERMS) {
        // Restart the cycle
        currentTerms = 1;
        curveHistory = [];
      }
      phase = 'drawing';
    }
    animId = requestAnimationFrame(run);
    return;
  }

  // phase === 'drawing'
  drawAllCurves(currentTerms);

  const highestFreq = Math.round(Math.pow(B, currentTerms - 1));
  window.__setStatus && window.__setStatus(
    `${currentTerms} term${currentTerms > 1 ? 's' : ''} — highest frequency: ${B}^${currentTerms-1}π = ${highestFreq}π — click to restart`
  );

  phase = 'pausing';
  phaseStart = ts;

  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
