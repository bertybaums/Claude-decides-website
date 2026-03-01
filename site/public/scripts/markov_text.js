// Markov Chain — Musical Note Visualization
// States: musical notes A-G. Transitions weighted by music-like probabilities.
// Show states as circles, transitions as arrows with thickness = probability.
// Animate random walk: highlight current state and transition just taken.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

// Musical notes as states
const NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];
const N = NOTES.length;

// Transition matrix: music-inspired (pentatonic-leaning, stepwise motion preferred)
// Row = from, Col = to
const RAW = [
  // C    D    E    F    G    A    B
  [ 0.0, 0.35, 0.15, 0.15, 0.20, 0.05, 0.10 ], // from C
  [ 0.15, 0.0, 0.30, 0.15, 0.20, 0.15, 0.05 ], // from D
  [ 0.10, 0.20, 0.0, 0.30, 0.15, 0.15, 0.10 ], // from E
  [ 0.10, 0.10, 0.25, 0.0, 0.30, 0.15, 0.10 ], // from F
  [ 0.20, 0.15, 0.10, 0.15, 0.0, 0.25, 0.15 ], // from G
  [ 0.10, 0.15, 0.10, 0.10, 0.25, 0.0, 0.30 ], // from A
  [ 0.25, 0.05, 0.15, 0.10, 0.15, 0.20, 0.0 ], // from B
];

// Normalize rows
const TRANS = RAW.map(row => {
  const s = row.reduce((a, b) => a + b, 0);
  return row.map(v => v / s);
});

// Color per note (musical hue mapping)
const NOTE_HUES = [0, 30, 60, 120, 180, 240, 300]; // C=red, D=orange, ..., B=purple

let curState, stepCount, lastState, animT, walkHistory;
let nodePositions;

function computeLayout() {
  const W = canvas.width, H = canvas.height;
  const cx = W / 2, cy = H / 2;
  const r = Math.min(W, H) * 0.35;
  nodePositions = NOTES.map((_, i) => {
    const angle = (2 * Math.PI * i / N) - Math.PI / 2;
    return [cx + r * Math.cos(angle), cy + r * Math.sin(angle)];
  });
}

function sampleNext(state) {
  const row = TRANS[state];
  let r = Math.random(), cum = 0;
  for (let i = 0; i < N; i++) {
    cum += row[i];
    if (r < cum) return i;
  }
  return N - 1;
}

function drawArrow(x1, y1, x2, y2, prob, isActive, fromNode, toNode) {
  const NODE_R = nodeRadius();
  // Shorten line to avoid overlapping nodes
  const dx = x2 - x1, dy = y2 - y1;
  const d = Math.hypot(dx, dy);
  if (d < 1) return;
  const ux = dx / d, uy = dy / d;

  // Curve the arrow slightly for bidirectional clarity
  const midX = (x1 + x2) / 2 + uy * 18 * (fromNode < toNode ? 1 : -1);
  const midY = (y1 + y2) / 2 - ux * 18 * (fromNode < toNode ? 1 : -1);

  const sx = x1 + ux * (NODE_R + 2);
  const sy = y1 + uy * (NODE_R + 2);
  const ex = x2 - ux * (NODE_R + 8);
  const ey = y2 - uy * (NODE_R + 8);

  const alpha = isActive ? 0.95 : 0.12 + prob * 0.55;
  const lw = isActive ? 3.0 : 0.5 + prob * 3.5;

  ctx.globalAlpha = alpha;
  ctx.strokeStyle = isActive ? '#fff' : `hsl(${NOTE_HUES[fromNode]},70%,60%)`;
  ctx.lineWidth = lw;
  ctx.beginPath();
  ctx.moveTo(sx, sy);
  ctx.quadraticCurveTo(midX, midY, ex, ey);
  ctx.stroke();

  // Arrowhead
  const headLen = isActive ? 10 : 5 + prob * 6;
  const angle = Math.atan2(ey - midY, ex - midX);
  ctx.fillStyle = isActive ? '#fff' : `hsl(${NOTE_HUES[fromNode]},70%,60%)`;
  ctx.beginPath();
  ctx.moveTo(ex, ey);
  ctx.lineTo(ex - headLen * Math.cos(angle - 0.4), ey - headLen * Math.sin(angle - 0.4));
  ctx.lineTo(ex - headLen * Math.cos(angle + 0.4), ey - headLen * Math.sin(angle + 0.4));
  ctx.closePath();
  ctx.fill();
  ctx.globalAlpha = 1;
}

function nodeRadius() {
  return Math.min(canvas.width, canvas.height) * 0.07;
}

function drawScene() {
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const NR = nodeRadius();

  // Draw all transitions (arrows)
  for (let from = 0; from < N; from++) {
    for (let to = 0; to < N; to++) {
      if (from === to) continue;
      const prob = TRANS[from][to];
      if (prob < 0.04) continue;
      const [x1, y1] = nodePositions[from];
      const [x2, y2] = nodePositions[to];
      const isActive = from === lastState && to === curState && animT > 0;
      drawArrow(x1, y1, x2, y2, prob, isActive, from, to);
    }
  }

  // Draw nodes
  for (let i = 0; i < N; i++) {
    const [x, y] = nodePositions[i];
    const isCurrent = i === curState;
    const isLast = i === lastState;
    const hue = NOTE_HUES[i];

    // Glow for current
    if (isCurrent) {
      ctx.fillStyle = `hsla(${hue},80%,50%,0.25)`;
      ctx.beginPath();
      ctx.arc(x, y, NR * 1.5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Node circle
    ctx.fillStyle = isCurrent
      ? `hsl(${hue},90%,65%)`
      : isLast
        ? `hsl(${hue},50%,35%)`
        : `hsl(${hue},40%,22%)`;
    ctx.strokeStyle = isCurrent ? '#fff' : `hsl(${hue},60%,45%)`;
    ctx.lineWidth = isCurrent ? 2.5 : 1;
    ctx.beginPath();
    ctx.arc(x, y, NR, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    // Label
    ctx.fillStyle = isCurrent ? '#000' : '#ddd';
    ctx.font = `bold ${Math.floor(NR * 0.85)}px serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(NOTES[i], x, y);
  }

  // Walk history strip at bottom
  const histY = canvas.height - 22;
  ctx.fillStyle = 'rgba(15,15,15,0.7)';
  ctx.fillRect(0, histY - 10, canvas.width, 32);

  const histMax = Math.floor(canvas.width / 22);
  const hist = walkHistory.slice(-histMax);
  for (let i = 0; i < hist.length; i++) {
    const hue = NOTE_HUES[hist[i]];
    const x = canvas.width / 2 + (i - hist.length / 2) * 22;
    ctx.fillStyle = `hsl(${hue},80%,${i === hist.length - 1 ? 70 : 40}%)`;
    ctx.font = `${i === hist.length - 1 ? 'bold ' : ''}14px monospace`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(NOTES[hist[i]], x, histY);
  }
}

function init() {
  cancelAnimationFrame(animId);
  computeLayout();
  curState = Math.floor(Math.random() * N);
  lastState = -1;
  stepCount = 0;
  animT = 0;
  walkHistory = [curState];

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  window.__setStatus && window.__setStatus(`step 0 — walking the chain — click to restart`);
  run();
}

let frameDelay = 0;

function run() {
  frameDelay++;
  animT = Math.min(1, animT + 0.05);

  drawScene();

  if (animT >= 1 && frameDelay >= 28) {
    // Take next step
    lastState = curState;
    curState = sampleNext(curState);
    stepCount++;
    walkHistory.push(curState);
    animT = 0;
    frameDelay = 0;
  }

  window.__setStatus && window.__setStatus(
    `step ${stepCount} — ${NOTES[lastState >= 0 ? lastState : curState]} → ${NOTES[curState]} — walking the chain — click to restart`
  );
  animId = requestAnimationFrame(run);
}

canvas.addEventListener('click', init);
window.__programRestart = init;
init();
