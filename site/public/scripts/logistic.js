// Logistic Map — Bifurcation Diagram
// x → r·x·(1−x): period doubling route to chaos
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

function render() {
  const W = canvas.width, H = canvas.height;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const rMin = 2.5, rMax = 4.0;
  const burnIn = 500, samples = 300;

  ctx.fillStyle = 'rgba(200, 146, 42, 0.4)';

  for (let px = 0; px < W; px++) {
    const r = rMin + (px / W) * (rMax - rMin);
    let x = 0.5;
    // burn in
    for (let i = 0; i < burnIn; i++) x = r * x * (1 - x);
    // sample
    for (let i = 0; i < samples; i++) {
      x = r * x * (1 - x);
      const py = H - Math.floor(x * H);
      ctx.fillRect(px, py, 1, 1);
    }
  }

  // Axis labels
  ctx.fillStyle = '#555';
  ctx.font = '11px monospace';
  ctx.fillText('r = 2.5', 4, H - 6);
  ctx.fillText('r = 4.0', W - 50, H - 6);
  ctx.fillText('x = 1', 4, 14);

  // Mark bifurcation points
  const bifurcations = [3.0, 3.449, 3.544, 3.5644];
  ctx.strokeStyle = 'rgba(255,255,255,0.15)';
  ctx.setLineDash([3, 5]);
  for (const r of bifurcations) {
    const px = Math.floor((r - rMin) / (rMax - rMin) * W);
    ctx.beginPath();
    ctx.moveTo(px, 0);
    ctx.lineTo(px, H);
    ctx.stroke();
    ctx.fillStyle = '#444';
    ctx.fillText(`r≈${r}`, px + 2, 14);
  }
  ctx.setLineDash([]);
}

function init() {
  window.__setStatus && window.__setStatus('bifurcation diagram — period doubling to chaos — click to redraw');
  render();
}

window.__programRestart = init;
init();
