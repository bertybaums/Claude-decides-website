// Continued Fractions — convergents approaching famous numbers
// [a0; a1, a2, ...] — each convergent is the best rational approximation
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const AMBER = '#c8922a';
const BG = '#0f0f0f';
const WHITE = '#e8e4dc';
const DIMTEXT = '#6b6560';
const DIM = '#2a2520';

const W = canvas.width;
const H = canvas.height;

// Famous numbers with their continued fraction coefficients and true values
const NUMBERS = [
  {
    name: 'π',
    value: Math.PI,
    cf: [3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14],
    desc: 'π = [3; 7, 15, 1, 292, 1, 1, 1, ...]  — no visible pattern'
  },
  {
    name: 'e',
    value: Math.E,
    cf: [2, 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, 1, 1, 10],
    desc: 'e = [2; 1, 2, 1, 1, 4, 1, 1, 6, ...]  — beautiful pattern'
  },
  {
    name: '√2',
    value: Math.sqrt(2),
    cf: [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    desc: '√2 = [1; 2, 2, 2, 2, ...]  — periodic'
  },
  {
    name: 'φ',
    value: (1 + Math.sqrt(5)) / 2,
    cf: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    desc: 'φ = [1; 1, 1, 1, 1, ...]  — all ones — hardest to approximate'
  },
  {
    name: '√3',
    value: Math.sqrt(3),
    cf: [1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
    desc: '√3 = [1; 1, 2, 1, 2, 1, 2, ...]  — periodic period 2'
  },
];

// Compute convergents p_n/q_n from cf array up to index k
function convergents(cf, k) {
  const convs = [];
  let p_prev = 1, p_curr = cf[0];
  let q_prev = 0, q_curr = 1;
  convs.push({ p: p_curr, q: q_curr, value: p_curr / q_curr });
  for (let i = 1; i <= k && i < cf.length; i++) {
    const a = cf[i];
    const p_next = a * p_curr + p_prev;
    const q_next = a * q_curr + q_prev;
    p_prev = p_curr; p_curr = p_next;
    q_prev = q_curr; q_curr = q_next;
    convs.push({ p: p_curr, q: q_curr, value: p_curr / q_curr });
  }
  return convs;
}

let numberIdx = 0;
let convergentStep = 0;
let phaseTimeout = null;
let running = true;

// Number line display region
const NL_Y = H / 2;
const NL_X1 = 60;
const NL_X2 = W - 60;
const NL_W = NL_X2 - NL_X1;

// We'll show the convergents list on the left
const LIST_X = 50;
const LIST_Y = 80;

function worldToScreen(value, lo, hi) {
  return NL_X1 + ((value - lo) / (hi - lo)) * NL_W;
}

function draw() {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  const num = NUMBERS[numberIdx];
  const trueVal = num.value;
  const convs = convergents(num.cf, convergentStep);

  // Compute display range: zoom in around true value based on step
  const spread = Math.max(0.001, 2.0 / Math.pow(3, Math.min(convergentStep, 8)));
  const lo = trueVal - spread * 1.8;
  const hi = trueVal + spread * 1.8;

  // Title
  ctx.fillStyle = WHITE;
  ctx.font = 'bold 16px monospace';
  ctx.fillText(num.name, LIST_X, 36);
  ctx.font = '13px monospace';
  ctx.fillStyle = DIMTEXT;
  ctx.fillText(num.desc, LIST_X + 40, 36);

  // True value label
  ctx.fillStyle = WHITE;
  ctx.font = '12px monospace';
  ctx.fillText(`true value: ${trueVal.toFixed(10)}`, LIST_X, 58);

  // Number line
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(NL_X1, NL_Y);
  ctx.lineTo(NL_X2, NL_Y);
  ctx.stroke();

  // True value — bright white vertical line
  const trueScreen = worldToScreen(trueVal, lo, hi);
  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(trueScreen, NL_Y - 30);
  ctx.lineTo(trueScreen, NL_Y + 30);
  ctx.stroke();

  // Draw each convergent as a tick mark + line to number line
  for (let i = 0; i < convs.length; i++) {
    const c = convs[i];
    const cx = worldToScreen(c.value, lo, hi);
    if (cx < NL_X1 - 20 || cx > NL_X2 + 20) continue;

    const isLatest = i === convs.length - 1;
    const alpha = isLatest ? 1.0 : 0.3 + 0.7 * (i / convs.length);
    const above = i % 2 === 0; // alternate above/below

    ctx.save();
    ctx.globalAlpha = alpha;

    // Approach line from convergent to number line
    const tickLen = isLatest ? 20 : 12;
    const tickY = above ? NL_Y - tickLen : NL_Y + tickLen;

    ctx.strokeStyle = AMBER;
    ctx.lineWidth = isLatest ? 2 : 1;
    ctx.beginPath();
    ctx.moveTo(cx, NL_Y);
    ctx.lineTo(cx, tickY);
    ctx.stroke();

    // Label
    if (isLatest || i <= 4 || (i <= 8 && i % 2 === 0)) {
      ctx.fillStyle = AMBER;
      ctx.font = isLatest ? '13px monospace' : '10px monospace';
      const label = c.q > 1 ? `${c.p}/${c.q}` : `${c.p}`;
      const labelX = cx - label.length * (isLatest ? 4 : 3);
      const labelY = above ? tickY - 5 : tickY + 14;
      ctx.fillText(label, labelX, labelY);
    }

    ctx.restore();
  }

  // Range labels on number line
  ctx.fillStyle = DIMTEXT;
  ctx.font = '10px monospace';
  ctx.fillText(lo.toFixed(6), NL_X1, NL_Y + 45);
  ctx.fillText(hi.toFixed(6), NL_X2 - 60, NL_Y + 45);

  // Convergents table (right side)
  const TABLE_X = W / 2 + 20;
  const TABLE_Y = 80;
  ctx.fillStyle = DIMTEXT;
  ctx.font = '11px monospace';
  ctx.fillText('convergent    value           error', TABLE_X, TABLE_Y);
  ctx.fillStyle = '#333';
  ctx.beginPath();
  ctx.moveTo(TABLE_X, TABLE_Y + 5);
  ctx.lineTo(W - 30, TABLE_Y + 5);
  ctx.stroke();

  for (let i = 0; i < convs.length && i < 10; i++) {
    const c = convs[i];
    const err = Math.abs(c.value - trueVal);
    const isLatest = i === convs.length - 1;
    ctx.fillStyle = isLatest ? AMBER : DIMTEXT;
    ctx.font = isLatest ? 'bold 11px monospace' : '11px monospace';
    const frac = c.q > 1 ? `${c.p}/${c.q}` : `${c.p}`;
    const row = `${frac.padStart(12)}  ${c.value.toFixed(8).padStart(12)}  ${err.toExponential(2).padStart(8)}`;
    ctx.fillText(row, TABLE_X, TABLE_Y + 20 + i * 16);
  }

  // CF expansion display
  const cfShown = num.cf.slice(0, Math.max(1, convergentStep + 1));
  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  const cfStr = `[${cfShown[0]}; ${cfShown.slice(1).join(', ')}${convergentStep < num.cf.length - 1 ? ', ...' : ''}]`;
  ctx.fillText(cfStr, LIST_X, NL_Y + 80);

  // Step indicator
  ctx.fillStyle = DIMTEXT;
  ctx.font = '11px monospace';
  ctx.fillText(`convergent ${convergentStep + 1} of ${num.cf.length}`, LIST_X, NL_Y + 100);
}

function step() {
  if (!running) return;
  convergentStep++;
  const num = NUMBERS[numberIdx];

  if (convergentStep >= num.cf.length) {
    // Pause then move to next number
    const convs = convergents(num.cf, num.cf.length - 1);
    const last = convs[convs.length - 1];
    const err = Math.abs(last.value - num.value);
    window.__setStatus && window.__setStatus(`${num.name} ≈ ${last.p}/${last.q}  error ${err.toExponential(2)} — click to restart`);
    draw();
    phaseTimeout = setTimeout(() => {
      numberIdx = (numberIdx + 1) % NUMBERS.length;
      convergentStep = 0;
      scheduleStep();
    }, 2500);
    return;
  }

  draw();
  const convs = convergents(num.cf, convergentStep);
  const last = convs[convs.length - 1];
  const err = Math.abs(last.value - num.value);
  window.__setStatus && window.__setStatus(`${num.name} ≈ ${last.p}/${last.q}  error ${err.toExponential(2)} — click to restart`);
  scheduleStep();
}

function scheduleStep() {
  if (!running) return;
  const delay = convergentStep < 3 ? 1200 : 800;
  phaseTimeout = setTimeout(step, delay);
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  if (phaseTimeout) clearTimeout(phaseTimeout);
  numberIdx = 0;
  convergentStep = 0;
  draw();
  window.__setStatus && window.__setStatus('π = [3; 7, 15, 1, 292, ...] — click to restart');
  scheduleStep();
}

window.__programRestart = init;
init();
