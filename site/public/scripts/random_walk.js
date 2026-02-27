// Random Walk — recurrent in 2D, transient in 3D
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

// Show multiple walks simultaneously
const NUM_WALKS = 5;
let walks;

function init() {
  running = true;
  cancelAnimationFrame(animId);

  const W = canvas.width, H = canvas.height;
  const cx = W / 2, cy = H / 2;

  walks = Array.from({ length: NUM_WALKS }, (_, i) => ({
    x: cx, y: cy,
    trail: [],
    hue: i * (360 / NUM_WALKS),
    steps: 0,
    returns: 0,
  }));

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  // Origin marker
  ctx.fillStyle = '#333';
  ctx.beginPath(); ctx.arc(cx, cy, 5, 0, Math.PI * 2); ctx.fill();

  window.__setStatus && window.__setStatus('2D random walk — provably returns to origin — click to restart');
  run();
}

const STEPS_PER_FRAME = 3;
const STEP_SIZE = 8;
const MAX_TRAIL = 200;

function run(ts) {
  if (!running) return;
  const W = canvas.width, H = canvas.height;
  const cx = W / 2, cy = H / 2;

  ctx.fillStyle = 'rgba(15,15,15,0.04)';
  ctx.fillRect(0, 0, W, H);

  for (const walk of walks) {
    for (let i = 0; i < STEPS_PER_FRAME; i++) {
      const dir = Math.floor(Math.random() * 4);
      const dx = [0, 0, 1, -1][dir] * STEP_SIZE;
      const dy = [1, -1, 0, 0][dir] * STEP_SIZE;

      // Wrap
      walk.x = ((walk.x + dx - 0) % W + W) % W;
      walk.y = ((walk.y + dy - 0) % H + H) % H;
      walk.steps++;

      walk.trail.push({ x: walk.x, y: walk.y });
      if (walk.trail.length > MAX_TRAIL) walk.trail.shift();

      // Count return visits to origin region
      if (Math.abs(walk.x - cx) < STEP_SIZE && Math.abs(walk.y - cy) < STEP_SIZE) {
        walk.returns++;
      }
    }

    // Draw trail
    for (let i = 1; i < walk.trail.length; i++) {
      const t = i / walk.trail.length;
      ctx.strokeStyle = `hsla(${walk.hue}, 70%, 60%, ${t * 0.6})`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(walk.trail[i-1].x, walk.trail[i-1].y);
      ctx.lineTo(walk.trail[i].x, walk.trail[i].y);
      ctx.stroke();
    }

    // Draw head
    ctx.fillStyle = `hsl(${walk.hue}, 70%, 70%)`;
    ctx.beginPath(); ctx.arc(walk.x, walk.y, 3, 0, Math.PI * 2); ctx.fill();
  }

  // Origin
  ctx.fillStyle = 'rgba(200,146,42,0.6)';
  ctx.beginPath(); ctx.arc(cx, cy, 5, 0, Math.PI * 2); ctx.fill();

  const totalSteps = walks[0].steps;
  window.__setStatus && window.__setStatus(`step ${totalSteps.toLocaleString()} — click to restart`);
  animId = requestAnimationFrame(run);
}

window.__programRestart = init;
init();
