// Euler's Identity — e^(iθ) traces the unit circle
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, theta, trail, running = true;

function init() {
  running = true;
  cancelAnimationFrame(animId);
  theta = 0;
  trail = [];
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  window.__setStatus && window.__setStatus("e^(iθ) = cos θ + i sin θ — click to restart");
  run();
}

function run(ts = 0) {
  if (!running) return;
  const W = canvas.width, H = canvas.height;
  const cx = W / 2, cy = H / 2;
  const R = Math.min(W, H) * 0.38;

  ctx.fillStyle = 'rgba(15,15,15,0.08)';
  ctx.fillRect(0, 0, W, H);

  // Axes
  ctx.strokeStyle = '#1a1a1a';
  ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(W, cy); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(cx, 0); ctx.lineTo(cx, H); ctx.stroke();

  // Unit circle
  ctx.strokeStyle = '#222';
  ctx.lineWidth = 1;
  ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.stroke();

  // Current point on circle
  const re = Math.cos(theta);
  const im = Math.sin(theta);
  const px = cx + re * R;
  const py = cy - im * R; // flip y

  // Trail
  trail.push({ x: px, y: py });
  if (trail.length > 300) trail.shift();
  for (let i = 1; i < trail.length; i++) {
    const t = i / trail.length;
    ctx.strokeStyle = `rgba(200, 146, 42, ${t * 0.6})`;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(trail[i-1].x, trail[i-1].y);
    ctx.lineTo(trail[i].x, trail[i].y);
    ctx.stroke();
  }

  // Radius line
  ctx.strokeStyle = '#c8922a';
  ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(px, py); ctx.stroke();

  // Projections
  ctx.strokeStyle = '#445';
  ctx.setLineDash([4, 4]);
  ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(px, cy); ctx.lineTo(px, py); ctx.stroke(); // imaginary
  ctx.beginPath(); ctx.moveTo(cx, py); ctx.lineTo(px, py); ctx.stroke(); // real
  ctx.setLineDash([]);

  // Point
  ctx.fillStyle = '#fff';
  ctx.beginPath(); ctx.arc(px, py, 5, 0, Math.PI * 2); ctx.fill();

  // Labels
  ctx.fillStyle = '#888';
  ctx.font = '11px monospace';
  ctx.textAlign = 'left';
  const deg = ((theta / Math.PI) * 180).toFixed(0);
  ctx.fillText(`θ = ${deg}°`, 10, 20);
  ctx.fillText(`cos θ = ${re.toFixed(3)}`, 10, 36);
  ctx.fillText(`sin θ = ${im.toFixed(3)}`, 10, 52);

  // Key points
  const keyPoints = [
    { angle: 0, label: '1', dx: 8, dy: -10 },
    { angle: Math.PI / 2, label: 'i', dx: 6, dy: -8 },
    { angle: Math.PI, label: '−1', dx: -30, dy: -10 },
    { angle: 3 * Math.PI / 2, label: '−i', dx: 6, dy: 16 },
  ];
  for (const kp of keyPoints) {
    const kx = cx + Math.cos(kp.angle) * R;
    const ky = cy - Math.sin(kp.angle) * R;
    ctx.fillStyle = '#444';
    ctx.beginPath(); ctx.arc(kx, ky, 3, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#666';
    ctx.fillText(kp.label, kx + kp.dx, ky + kp.dy);
  }

  // Euler's identity note
  ctx.fillStyle = '#c8922a';
  ctx.font = '13px monospace';
  ctx.textAlign = 'center';
  if (Math.abs(Math.PI - theta % (Math.PI * 2)) < 0.15) {
    ctx.fillText('e^(iπ) + 1 = 0', W / 2, H - 20);
  } else {
    ctx.fillText(`e^(i·${deg}°) = ${re.toFixed(3)} + ${im.toFixed(3)}i`, W / 2, H - 20);
  }

  theta += 0.02;
  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
