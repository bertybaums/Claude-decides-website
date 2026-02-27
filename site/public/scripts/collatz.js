// Collatz Conjecture — stopping times as animated bar chart
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

function collatzSteps(n) {
  let steps = 0;
  while (n !== 1) {
    n = n % 2 === 0 ? n / 2 : 3 * n + 1;
    steps++;
  }
  return steps;
}

const MAX_N = 500;
let data, maxSteps, currentN;

function init() {
  running = true;
  cancelAnimationFrame(animId);
  data = new Array(MAX_N + 1).fill(0);
  maxSteps = 0;
  currentN = 2;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  window.__setStatus && window.__setStatus('computing stopping times — click to restart');
  run();
}

function run() {
  if (!running) return;

  // Compute a batch
  const batch = 5;
  for (let i = 0; i < batch && currentN <= MAX_N; i++, currentN++) {
    data[currentN] = collatzSteps(currentN);
    if (data[currentN] > maxSteps) maxSteps = data[currentN];
  }

  // Draw
  const W = canvas.width, H = canvas.height;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  const barW = W / MAX_N;
  for (let i = 2; i <= currentN; i++) {
    const barH = (data[i] / (maxSteps || 1)) * (H - 30);
    const t = data[i] / (maxSteps || 1);
    // Color by height
    const r = Math.floor(200 * t);
    const g = Math.floor(100 * (1 - t) + 50 * t);
    const b = Math.floor(50 * (1 - t));
    ctx.fillStyle = `rgb(${r},${g},${b})`;
    ctx.fillRect((i - 2) * barW, H - 30 - barH, Math.max(1, barW - 0.5), barH);
  }

  // Axis
  ctx.fillStyle = '#444';
  ctx.font = '11px monospace';
  ctx.fillText('n=2', 2, H - 15);
  ctx.fillText(`n=${MAX_N}`, W - 40, H - 15);
  ctx.fillText(`max ${maxSteps} steps`, 2, 16);

  // Highlight famous numbers
  if (maxSteps > 0) {
    // 27 takes 111 steps
    const px27 = (27 - 2) / MAX_N * W;
    ctx.strokeStyle = '#c8922a44';
    ctx.beginPath(); ctx.moveTo(px27, 0); ctx.lineTo(px27, H - 30); ctx.stroke();
    ctx.fillStyle = '#c8922a';
    ctx.fillText('27', px27 + 2, 28);
  }

  if (currentN <= MAX_N) {
    animId = requestAnimationFrame(run);
    window.__setStatus && window.__setStatus(`n = ${currentN} — click to restart`);
  } else {
    window.__setStatus && window.__setStatus(`all ${MAX_N} stopping times — n=27 highlighted — click to restart`);
  }
}

window.__programRestart = init;
init();
