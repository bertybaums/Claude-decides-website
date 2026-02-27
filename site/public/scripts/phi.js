// Golden Ratio convergence — Fibonacci ratios approaching φ
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

function init() {
  const W = canvas.width, H = canvas.height;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  const PHI = (1 + Math.sqrt(5)) / 2;
  const N = 30;
  const padding = { t: 40, b: 50, l: 80, r: 40 };
  const plotW = W - padding.l - padding.r;
  const plotH = H - padding.t - padding.b;

  // Fibonacci sequence
  const fibs = [1n, 1n];
  for (let i = 2; i < N; i++) fibs.push(fibs[i-1] + fibs[i-2]);

  const ratios = [];
  for (let i = 1; i < N; i++) {
    ratios.push(Number(fibs[i]) / Number(fibs[i-1]));
  }

  const minR = 1.0, maxR = 2.0;

  // Grid lines
  ctx.strokeStyle = '#1a1a1a';
  ctx.lineWidth = 1;
  for (let r = 1.0; r <= 2.0; r += 0.1) {
    const y = padding.t + (1 - (r - minR) / (maxR - minR)) * plotH;
    ctx.beginPath(); ctx.moveTo(padding.l, y); ctx.lineTo(W - padding.r, y); ctx.stroke();
    ctx.fillStyle = '#333';
    ctx.font = '10px monospace';
    ctx.textAlign = 'right';
    ctx.fillText(r.toFixed(1), padding.l - 6, y + 3);
  }

  // φ line
  const phiY = padding.t + (1 - (PHI - minR) / (maxR - minR)) * plotH;
  ctx.strokeStyle = 'rgba(200, 146, 42, 0.4)';
  ctx.setLineDash([6, 4]);
  ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(padding.l, phiY); ctx.lineTo(W - padding.r, phiY); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#c8922a';
  ctx.textAlign = 'left';
  ctx.fillText('φ = 1.6180…', W - padding.r + 2, phiY + 3);

  // Plot ratios
  const xStep = plotW / (ratios.length - 1);
  ctx.strokeStyle = '#7eb8d4';
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let i = 0; i < ratios.length; i++) {
    const x = padding.l + i * xStep;
    const y = padding.t + (1 - (ratios[i] - minR) / (maxR - minR)) * plotH;
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.stroke();

  // Points
  ctx.fillStyle = '#7eb8d4';
  for (let i = 0; i < ratios.length; i++) {
    const x = padding.l + i * xStep;
    const y = padding.t + (1 - (ratios[i] - minR) / (maxR - minR)) * plotH;
    ctx.beginPath(); ctx.arc(x, y, 3, 0, Math.PI * 2); ctx.fill();
  }

  // Labels
  ctx.fillStyle = '#555';
  ctx.font = '10px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('F(n)/F(n-1)', W / 2, H - 10);
  ctx.fillText('n=1', padding.l, H - 28);
  ctx.fillText(`n=${N}`, W - padding.r, H - 28);

  ctx.fillStyle = '#888';
  ctx.font = '12px monospace';
  ctx.fillText(`φ = (1+√5)/2 = ${PHI.toFixed(10)}`, W / 2, padding.t - 12);

  window.__setStatus && window.__setStatus('Fibonacci ratios converging to φ — click to redraw');
}

window.__programRestart = init;
init();
