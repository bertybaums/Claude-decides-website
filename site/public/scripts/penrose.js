// Penrose Tiling — Aperiodic Order (P2: kite and dart via substitution)
// Uses the substitution/inflation method on Robinson triangles.
// Each inflation step subdivides tiles into smaller tiles.
// Thick rhombuses (golden gnomons) and thin rhombuses (golden triangles).
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

// Golden ratio
const PHI = (1 + Math.sqrt(5)) / 2;

// We use Robinson triangles (half-rhombus triangles):
// THICK triangle: isoceles with apex 36°, base angles 72°
// THIN triangle:  isoceles with apex 108°, base angles 36°

// A triangle is { type: 'thick'|'thin', a, b, c } where a is apex, b,c are base
// Substitution rules:
//   thick → thick + thin
//   thin  → thick + thin (different arrangement)

function subdivide(tris) {
  const result = [];
  for (const { type, a, b, c } of tris) {
    if (type === 'thick') {
      // Thick: split with point p on AC at distance b->a/phi from b
      const p = [
        a[0] + (b[0] - a[0]) / PHI,
        a[1] + (b[1] - a[1]) / PHI,
      ];
      result.push({ type: 'thick', a: c, b: p, c: b });
      result.push({ type: 'thin',  a: p, b: c, c: a });
    } else {
      // Thin: split with two new points
      const p = [
        b[0] + (a[0] - b[0]) / PHI,
        b[1] + (a[1] - b[1]) / PHI,
      ];
      const q = [
        b[0] + (c[0] - b[0]) / PHI,
        b[1] + (c[1] - b[1]) / PHI,
      ];
      result.push({ type: 'thin',  a: a, b: p, c: b });
      result.push({ type: 'thick', a: q, b: p, c: a });
      result.push({ type: 'thin',  a: c, b: q, c: a });
    }
  }
  return result;
}

// Build initial wheel of thick triangles (10 triangles in a ring)
function makeWheel(cx, cy, r) {
  const tris = [];
  for (let i = 0; i < 10; i++) {
    const angle = (Math.PI / 5) * i - Math.PI / 2;
    const nextAngle = angle + Math.PI / 5;
    const a = [cx, cy];
    const b = [cx + r * Math.cos(angle), cy + r * Math.sin(angle)];
    const c = [cx + r * Math.cos(nextAngle), cy + r * Math.sin(nextAngle)];
    tris.push({ type: i % 2 === 0 ? 'thick' : 'thin', a, b, c });
  }
  return tris;
}

let tris, thickCount, thinCount, drawn, step;

function init() {
  cancelAnimationFrame(animId);
  const W = canvas.width, H = canvas.height;
  const R = Math.min(W, H) * 0.52;
  tris = makeWheel(W / 2, H / 2, R);

  // Inflate 5 times for a dense tiling
  for (let i = 0; i < 5; i++) {
    tris = subdivide(tris);
  }

  thickCount = tris.filter(t => t.type === 'thick').length;
  thinCount  = tris.filter(t => t.type === 'thin').length;

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  drawn = 0;
  window.__setStatus && window.__setStatus(`aperiodic — ${tris.length} tiles — never repeats — click to restart`);
  run();
}

const TILES_PER_FRAME = 60;

function run() {
  const end = Math.min(drawn + TILES_PER_FRAME, tris.length);
  for (let i = drawn; i < end; i++) {
    const { type, a, b, c } = tris[i];
    // Color: thick = warm amber, thin = cooler blue-grey
    ctx.fillStyle = type === 'thick' ? 'rgba(200,146,42,0.85)' : 'rgba(70,130,180,0.75)';
    ctx.strokeStyle = '#0f0f0f';
    ctx.lineWidth = 0.8;
    ctx.beginPath();
    ctx.moveTo(a[0], a[1]);
    ctx.lineTo(b[0], b[1]);
    ctx.lineTo(c[0], c[1]);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  }
  drawn = end;

  const ratio = thinCount > 0 ? (thickCount / thinCount).toFixed(3) : '?';
  window.__setStatus && window.__setStatus(
    `aperiodic — ${drawn}/${tris.length} tiles — thick/thin ratio → φ=${ratio} — click to restart`
  );

  if (drawn < tris.length) {
    animId = requestAnimationFrame(run);
  } else {
    window.__setStatus && window.__setStatus(
      `aperiodic — ${tris.length} tiles — thick/thin = ${ratio} (φ≈1.618) — click to restart`
    );
  }
}

canvas.addEventListener('click', init);
window.__programRestart = init;
init();
