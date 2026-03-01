// Prime Factorization — Sieve of Eratosthenes animation
// Color each number by its smallest prime factor; primes glow amber
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const AMBER = '#c8922a';
const BG = '#0f0f0f';
const WHITE = '#e8e4dc';
const DIMTEXT = '#6b6560';

const W = canvas.width;
const H = canvas.height;

const MAX_N = 300;
const COLS = 20;
const ROWS = Math.ceil(MAX_N / COLS);

// Cell layout
const MARGIN = 50;
const GRID_W = W - 2 * MARGIN;
const GRID_H = H - MARGIN - 80;
const CELL_W = Math.floor(GRID_W / COLS);
const CELL_H = Math.floor(GRID_H / ROWS);
const GRID_X = MARGIN + (GRID_W - CELL_W * COLS) / 2;
const GRID_Y = 70;

// Prime factor colors (each prime gets a fixed hue)
const PRIME_COLORS = {};
const PRIME_HUE_START = [
  [2,  '#c8922a'], // amber
  [3,  '#4a9a4a'], // green
  [5,  '#4a70cc'], // blue
  [7,  '#cc4499'], // pink
  [11, '#cc7744'], // orange
  [13, '#44aacc'], // cyan
  [17, '#aa44cc'], // purple
  [19, '#88cc44'], // lime
  [23, '#cc4444'], // red
  [29, '#44ccaa'], // teal
];
for (const [p, c] of PRIME_HUE_START) PRIME_COLORS[p] = c;

function hexToRgb(hex) {
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return [r,g,b];
}

// Factorize n: return {smallestPrime, factors}
function factorize(n) {
  if (n < 2) return { smallestPrime: null, factors: [] };
  const factors = [];
  let temp = n;
  for (let p = 2; p * p <= temp; p++) {
    while (temp % p === 0) {
      factors.push(p);
      temp = Math.floor(temp / p);
    }
  }
  if (temp > 1) factors.push(temp);
  return { smallestPrime: factors[0] || null, factors };
}

// Pre-compute factorizations
const factData = [];
for (let n = 2; n <= MAX_N; n++) {
  factData.push({ n, ...factorize(n) });
}

// Sieve state
const cellState = new Array(MAX_N + 1).fill('unvisited'); // 'unvisited', 'prime', 'composite'
const smallestFactor = new Array(MAX_N + 1).fill(null);

// Cell coordinates
function cellXY(n) {
  const idx = n - 2;
  const col = idx % COLS;
  const row = Math.floor(idx / COLS);
  return [GRID_X + col * CELL_W, GRID_Y + row * CELL_H];
}

function cellColor(n) {
  const state = cellState[n];
  if (state === 'unvisited') return '#1a1a1a';
  const sp = smallestFactor[n];
  if (state === 'prime') {
    return AMBER; // primes always amber
  }
  // Composite: color of smallest prime factor
  if (sp && PRIME_COLORS[sp]) {
    const [r,g,b] = hexToRgb(PRIME_COLORS[sp]);
    return `rgb(${Math.round(r*0.5)},${Math.round(g*0.5)},${Math.round(b*0.5)})`;
  }
  return '#333';
}

let currentPrime = 2;
let sieveStep = 0; // 0=find prime, 1=mark multiples
let multiples = [];
let multIdx = 0;
let running = true;
let phaseTimeout = null;
let highlightN = null;

let primeCount = 0;

function drawGrid(extraHighlight = null) {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText('Prime Factorization — Sieve of Eratosthenes', MARGIN, 32);

  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  ctx.fillText(`primes ≤ ${MAX_N}: ${primeCount} found so far`, MARGIN, 52);

  for (let n = 2; n <= MAX_N; n++) {
    const [x, y] = cellXY(n);
    const state = cellState[n];
    const isHighlight = n === highlightN || (extraHighlight && extraHighlight.includes(n));
    const isPrime = state === 'prime';

    // Background
    ctx.fillStyle = cellColor(n);
    ctx.fillRect(x + 1, y + 1, CELL_W - 2, CELL_H - 2);

    // Highlight glow
    if (isHighlight) {
      ctx.strokeStyle = '#ffffff88';
      ctx.lineWidth = 2;
      ctx.strokeRect(x + 1, y + 1, CELL_W - 2, CELL_H - 2);
    }

    // Number label
    if (CELL_W >= 20 && CELL_H >= 16) {
      ctx.fillStyle = isPrime ? BG : (state === 'unvisited' ? DIMTEXT : '#444');
      ctx.font = `${Math.min(10, CELL_W - 4)}px monospace`;
      ctx.textAlign = 'center';
      ctx.fillText(String(n), x + CELL_W / 2, y + CELL_H / 2 + 4);
      ctx.textAlign = 'left';
    }
  }

  // Legend
  const LX = MARGIN;
  const LY = GRID_Y + ROWS * CELL_H + 12;
  ctx.fillStyle = AMBER;
  ctx.fillRect(LX, LY, 14, 14);
  ctx.fillStyle = WHITE;
  ctx.font = '11px monospace';
  ctx.fillText('prime', LX + 18, LY + 11);

  for (let i = 0; i < Math.min(5, PRIME_HUE_START.length); i++) {
    const [p, c] = PRIME_HUE_START[i];
    const [r,g,b] = hexToRgb(c);
    ctx.fillStyle = `rgb(${Math.round(r*0.5)},${Math.round(g*0.5)},${Math.round(b*0.5)})`;
    ctx.fillRect(LX + 70 + i * 55, LY, 14, 14);
    ctx.fillStyle = DIMTEXT;
    ctx.fillText(`÷${p}`, LX + 88 + i * 55, LY + 11);
  }
}

function findNextUnmarkedPrime() {
  for (let n = currentPrime; n <= MAX_N; n++) {
    if (cellState[n] === 'unvisited') return n;
  }
  return null;
}

function sieveAdvance() {
  if (!running) return;

  if (currentPrime > MAX_N) {
    // Done — mark remaining unvisited as prime
    for (let n = 2; n <= MAX_N; n++) {
      if (cellState[n] === 'unvisited') {
        cellState[n] = 'prime';
        smallestFactor[n] = n;
        primeCount++;
      }
    }
    drawGrid();
    window.__setStatus && window.__setStatus(`sieve complete — ${primeCount} primes ≤ ${MAX_N} — click to restart`);
    return;
  }

  if (cellState[currentPrime] !== 'unvisited') {
    currentPrime++;
    phaseTimeout = setTimeout(sieveAdvance, 10);
    return;
  }

  // Mark current as prime
  cellState[currentPrime] = 'prime';
  smallestFactor[currentPrime] = currentPrime;
  primeCount++;
  highlightN = currentPrime;

  // Collect multiples to mark
  multiples = [];
  for (let m = currentPrime * currentPrime; m <= MAX_N; m += currentPrime) {
    if (cellState[m] === 'unvisited') {
      multiples.push(m);
    }
  }

  drawGrid();
  window.__setStatus && window.__setStatus(`prime ${currentPrime} — marking multiples — click to restart`);

  let mi = 0;
  function markNext() {
    if (!running) return;
    if (mi >= multiples.length) {
      currentPrime++;
      highlightN = null;
      const delay = currentPrime < 20 ? 300 : currentPrime < 50 ? 150 : 60;
      phaseTimeout = setTimeout(sieveAdvance, delay);
      return;
    }
    const m = multiples[mi];
    cellState[m] = 'composite';
    smallestFactor[m] = currentPrime;
    mi++;
    drawGrid([m]);
    phaseTimeout = setTimeout(markNext, currentPrime < 5 ? 80 : currentPrime < 20 ? 30 : 10);
  }

  const primeDelay = currentPrime < 10 ? 500 : currentPrime < 30 ? 300 : 150;
  phaseTimeout = setTimeout(markNext, primeDelay);
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  if (phaseTimeout) clearTimeout(phaseTimeout);
  cellState.fill('unvisited');
  smallestFactor.fill(null);
  currentPrime = 2;
  multiples = [];
  multIdx = 0;
  highlightN = null;
  primeCount = 0;
  drawGrid();
  window.__setStatus && window.__setStatus(`${MAX_N} — primes in amber — click to restart`);
  phaseTimeout = setTimeout(sieveAdvance, 600);
}

window.__programRestart = init;
init();
