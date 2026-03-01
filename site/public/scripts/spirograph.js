// Spirograph — Hypotrochoids and Epitrochoids
// x(t) = (R-r)cos(t) + d·cos((R-r)t/r)
// y(t) = (R-r)sin(t) - d·sin((R-r)t/r)
// Cycles through different parameter sets, each drawn then fading.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

// Curated parameter sets (R, r, d, label)
const CURVES = [
  [105, 41,  90, 'R=105 r=41 d=90'],
  [80,  25,  65, 'R=80 r=25 d=65'],
  [120, 30,  80, 'R=120 r=30 d=80'],
  [100, 37,  95, 'R=100 r=37 d=95'],
  [90,  18,  70, 'R=90 r=18 d=70'],
  [110, 44,  60, 'R=110 r=44 d=60'],
  [95,  19,  88, 'R=95 r=19 d=88'],
  [85,  34,  42, 'R=85 r=34 d=42'],
];

let curveIdx, t, tMax, curvePoints, phase, fadeAlpha;

function hypotrochoid(R, r, d, t) {
  const x = (R - r) * Math.cos(t) + d * Math.cos((R - r) / r * t);
  const y = (R - r) * Math.sin(t) - d * Math.sin((R - r) / r * t);
  return [x, y];
}

function computeTMax(R, r) {
  // Full period is LCM(R,r)/r * 2π
  function gcd(a, b) { return b === 0 ? a : gcd(b, a % b); }
  const lcm = R * r / gcd(R, r);
  return (lcm / r) * Math.PI * 2;
}

function toCanvas(x, y) {
  const W = canvas.width, H = canvas.height;
  const scale = Math.min(W, H) * 0.44 / 120;
  return [W / 2 + x * scale, H / 2 + y * scale];
}

function colorAtT(t, tMax) {
  const frac = t / tMax;
  // Warm amber to white gradient
  const r = Math.floor(200 + frac * 55);
  const g = Math.floor(100 + frac * 130);
  const b = Math.floor(30 + frac * 210);
  return `rgb(${r},${g},${b})`;
}

function nextCurve() {
  curveIdx = (curveIdx + 1) % CURVES.length;
  const [R, r, d] = CURVES[curveIdx];
  tMax = computeTMax(R, r);
  t = 0;
  curvePoints = [];
  phase = 'drawing';
  fadeAlpha = 1.0;
}

function init() {
  cancelAnimationFrame(animId);
  curveIdx = -1;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  nextCurve();
  run();
}

const DT = 0.04;
const STEPS_PER_FRAME = 12;

function run() {
  const [R, r, d, label] = CURVES[curveIdx];

  if (phase === 'drawing') {
    for (let i = 0; i < STEPS_PER_FRAME; i++) {
      if (t > tMax) { phase = 'holding'; setTimeout(() => { phase = 'fading'; }, 1200); break; }
      const pt = hypotrochoid(R, r, d, t);
      curvePoints.push([pt, t / tMax]);
      t += DT;
    }

    // Redraw entire curve each frame with color gradient
    ctx.fillStyle = '#0f0f0f';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (curvePoints.length > 1) {
      for (let i = 1; i < curvePoints.length; i++) {
        const [p1, f1] = curvePoints[i - 1];
        const [p2, f2] = curvePoints[i];
        const [cx1, cy1] = toCanvas(...p1);
        const [cx2, cy2] = toCanvas(...p2);
        ctx.strokeStyle = colorAtT(f1 * tMax, tMax);
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(cx1, cy1);
        ctx.lineTo(cx2, cy2);
        ctx.stroke();
      }
    }
    window.__setStatus && window.__setStatus(`${label} — drawing — click to restart`);
  } else if (phase === 'holding') {
    window.__setStatus && window.__setStatus(`${label} — complete — click to restart`);
  } else if (phase === 'fading') {
    fadeAlpha -= 0.018;
    if (fadeAlpha <= 0) {
      nextCurve();
    } else {
      ctx.fillStyle = `rgba(15,15,15,${0.06})`;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
    window.__setStatus && window.__setStatus(`${label} — fading — click to restart`);
  }

  animId = requestAnimationFrame(run);
}

canvas.addEventListener('click', init);
window.__programRestart = init;
init();
