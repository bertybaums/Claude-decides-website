// Double Pendulum — Deterministic Chaos
// Two hinged rods. Same equations as Newtonian mechanics.
// Nearby initial conditions diverge exponentially.
// Three pendulums started ±0.001° apart show the butterfly effect visually.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const G = 9.81;
const L1 = 1.0, L2 = 1.0;
const M1 = 1.0, M2 = 1.0;
const DT = 0.025;
const SCALE = 120;

// Three pendulums: base + two perturbations
const COLORS = ['#c8922a', '#4af', '#f46'];
const TRAIL_LEN = 400;

let pendulums, step;

function accel(th1, th2, om1, om2) {
  const d = th2 - th1;
  const sinD = Math.sin(d), cosD = Math.cos(d);
  const denom = 2 * M1 + M2 - M2 * Math.cos(2 * d);

  const num1 = -G * (2 * M1 + M2) * Math.sin(th1)
             - M2 * G * Math.sin(th1 - 2 * th2)
             - 2 * sinD * M2 * (om2 * om2 * L2 + om1 * om1 * L1 * cosD);
  const a1 = num1 / (L1 * denom);

  const num2 = 2 * sinD * (om1 * om1 * L1 * (M1 + M2)
             + G * (M1 + M2) * Math.cos(th1)
             + om2 * om2 * L2 * M2 * cosD);
  const a2 = num2 / (L2 * denom);

  return [a1, a2];
}

function rk4(th1, th2, om1, om2) {
  function deriv(t1, t2, o1, o2) {
    const [a1, a2] = accel(t1, t2, o1, o2);
    return [o1, o2, a1, a2];
  }
  const k1 = deriv(th1, th2, om1, om2);
  const k2 = deriv(th1 + DT/2*k1[0], th2 + DT/2*k1[1], om1 + DT/2*k1[2], om2 + DT/2*k1[3]);
  const k3 = deriv(th1 + DT/2*k2[0], th2 + DT/2*k2[1], om1 + DT/2*k2[2], om2 + DT/2*k2[3]);
  const k4 = deriv(th1 + DT*k3[0], th2 + DT*k3[1], om1 + DT*k3[2], om2 + DT*k3[3]);
  return [
    th1 + DT/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]),
    th2 + DT/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1]),
    om1 + DT/6*(k1[2]+2*k2[2]+2*k3[2]+k4[2]),
    om2 + DT/6*(k1[3]+2*k2[3]+2*k3[3]+k4[3]),
  ];
}

function tipPos(th1, th2) {
  const x1 = L1 * Math.sin(th1);
  const y1 = L1 * Math.cos(th1);
  const x2 = x1 + L2 * Math.sin(th2);
  const y2 = y1 + L2 * Math.cos(th2);
  return { x1, y1, x2, y2 };
}

function init() {
  cancelAnimationFrame(animId);
  step = 0;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const eps = 0.001 * Math.PI / 180; // ±0.001 degrees in radians
  const baseAngle = Math.PI * 0.75;
  pendulums = [
    { th1: baseAngle, th2: baseAngle * 0.9, om1: 0, om2: 0, trail: [] },
    { th1: baseAngle + eps, th2: baseAngle * 0.9, om1: 0, om2: 0, trail: [] },
    { th1: baseAngle - eps, th2: baseAngle * 0.9, om1: 0, om2: 0, trail: [] },
  ];

  window.__setStatus && window.__setStatus('chaotic — 3 pendulums, identical start ±0.001° — click to restart');
  run();
}

function run() {
  ctx.fillStyle = 'rgba(15,15,15,0.18)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const cx = canvas.width / 2;
  const cy = canvas.height * 0.38;

  for (let i = 0; i < pendulums.length; i++) {
    const p = pendulums[i];
    [p.th1, p.th2, p.om1, p.om2] = rk4(p.th1, p.th2, p.om1, p.om2);

    const { x1, y1, x2, y2 } = tipPos(p.th1, p.th2);
    const sx1 = cx + x1 * SCALE;
    const sy1 = cy + y1 * SCALE;
    const sx2 = cx + x2 * SCALE;
    const sy2 = cy + y2 * SCALE;

    // Trail
    p.trail.push([sx2, sy2]);
    if (p.trail.length > TRAIL_LEN) p.trail.shift();

    const col = COLORS[i];
    ctx.lineWidth = 1;
    for (let j = 1; j < p.trail.length; j++) {
      const t = j / p.trail.length;
      ctx.globalAlpha = t * 0.7;
      ctx.strokeStyle = col;
      ctx.beginPath();
      ctx.moveTo(p.trail[j-1][0], p.trail[j-1][1]);
      ctx.lineTo(p.trail[j][0], p.trail[j][1]);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;

    // Draw rods (only for first pendulum to avoid clutter)
    if (i === 0) {
      ctx.strokeStyle = 'rgba(200,200,200,0.5)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(cx, cy); ctx.lineTo(sx1, sy1); ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(sx1, sy1); ctx.lineTo(sx2, sy2); ctx.stroke();

      // Pivot dot
      ctx.fillStyle = '#888';
      ctx.beginPath();
      ctx.arc(cx, cy, 4, 0, Math.PI * 2);
      ctx.fill();

      // Joint dot
      ctx.fillStyle = '#aaa';
      ctx.beginPath();
      ctx.arc(sx1, sy1, 5, 0, Math.PI * 2);
      ctx.fill();

      // Tip dot
      ctx.fillStyle = col;
      ctx.beginPath();
      ctx.arc(sx2, sy2, 6, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  step++;
  const t = (step * DT).toFixed(1);
  window.__setStatus && window.__setStatus(`t=${t} — chaotic — 3 pendulums, identical start ±0.001° — click to restart`);
  animId = requestAnimationFrame(run);
}

canvas.addEventListener('click', init);
window.__programRestart = init;
init();
