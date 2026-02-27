// L-Systems — rewriting rules produce botanical forms
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

const systems = [
  {
    name: 'Fractal Tree',
    axiom: 'F',
    rules: { F: 'FF+[+F-F-F]-[-F+F+F]' },
    angle: 25, len: 6, iterations: 5, startAngle: -90,
  },
  {
    name: 'Koch Snowflake',
    axiom: 'F++F++F',
    rules: { F: 'F-F++F-F' },
    angle: 60, len: 5, iterations: 4, startAngle: 0,
  },
  {
    name: 'Dragon Curve',
    axiom: 'FX',
    rules: { X: 'X+YF+', Y: '-FX-Y' },
    angle: 90, len: 7, iterations: 12, startAngle: 0,
  },
  {
    name: 'Sierpiński Triangle',
    axiom: 'F-G-G',
    rules: { F: 'F-G+F+G-F', G: 'GG' },
    angle: 120, len: 4, iterations: 6, startAngle: 0,
  },
];

let sysIdx = 0;

function expand(system, iters) {
  let s = system.axiom;
  for (let i = 0; i < iters; i++) {
    s = s.split('').map(c => system.rules[c] || c).join('');
    if (s.length > 200000) break;
  }
  return s;
}

function getBounds(instructions, system) {
  let x = 0, y = 0, angle = system.startAngle * Math.PI / 180;
  const stack = [];
  let minX = 0, maxX = 0, minY = 0, maxY = 0;
  const a = system.angle * Math.PI / 180;
  const l = system.len;
  for (const c of instructions) {
    if (c === 'F' || c === 'G') {
      x += Math.cos(angle) * l; y += Math.sin(angle) * l;
      if (x < minX) minX = x; if (x > maxX) maxX = x;
      if (y < minY) minY = y; if (y > maxY) maxY = y;
    } else if (c === '+') angle += a;
    else if (c === '-') angle -= a;
    else if (c === '[') stack.push({ x, y, angle });
    else if (c === ']') { const s = stack.pop(); x = s.x; y = s.y; angle = s.angle; }
  }
  return { minX, maxX, minY, maxY };
}

function draw(sysObj) {
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const instructions = expand(sysObj, sysObj.iterations);
  const bounds = getBounds(instructions, sysObj);
  const W = canvas.width, H = canvas.height;
  const padding = 40;
  const bw = bounds.maxX - bounds.minX || 1;
  const bh = bounds.maxY - bounds.minY || 1;
  const scale = Math.min((W - padding * 2) / bw, (H - padding * 2) / bh);

  let x = (W - padding * 2) / 2 + padding - (bounds.minX + bw / 2) * scale;
  let y = (H - padding * 2) / 2 + padding - (bounds.minY + bh / 2) * scale;
  let angle = sysObj.startAngle * Math.PI / 180;
  const stack = [];
  const a = sysObj.angle * Math.PI / 180;
  const l = sysObj.len * scale;

  ctx.strokeStyle = '#3a8a3a';
  ctx.lineWidth = 0.8;
  ctx.beginPath();
  ctx.moveTo(x, y);

  for (const c of instructions) {
    if (c === 'F' || c === 'G') {
      const nx = x + Math.cos(angle) * l;
      const ny = y + Math.sin(angle) * l;
      ctx.lineTo(nx, ny);
      x = nx; y = ny;
    } else if (c === '+') { angle += a; ctx.moveTo(x, y); }
    else if (c === '-') { angle -= a; ctx.moveTo(x, y); }
    else if (c === '[') { stack.push({ x, y, angle }); ctx.moveTo(x, y); }
    else if (c === ']') {
      const s = stack.pop(); x = s.x; y = s.y; angle = s.angle;
      ctx.moveTo(x, y);
    }
  }
  ctx.stroke();
}

function init() {
  running = true;
  draw(systems[sysIdx]);
  window.__setStatus && window.__setStatus(`${systems[sysIdx].name} — click to cycle through systems`);
}

// Click cycles through L-systems
window.__programRestart = () => {
  sysIdx = (sysIdx + 1) % systems.length;
  init();
};
init();
