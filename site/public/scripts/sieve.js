// Sieve of Eratosthenes — animated elimination
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId, running = true;

const LIMIT = 400;
const CELL = 18;
let state, currentPrime, composites;

function init() {
  running = true;
  clearTimeout(animId);

  const W = canvas.width;
  const cols = Math.floor(W / CELL);

  state = new Array(LIMIT + 1).fill('unknown');
  state[0] = state[1] = 'composite';
  currentPrime = 2;
  composites = new Set([0, 1]);

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw all numbers
  for (let n = 2; n <= LIMIT; n++) {
    drawCell(n, 'unknown');
  }

  window.__setStatus && window.__setStatus('sieve starting — click to restart');
  setTimeout(sieveStep, 400);
}

function cellPos(n) {
  const W = canvas.width;
  const cols = Math.floor(W / CELL);
  const c = (n - 2) % cols;
  const r = Math.floor((n - 2) / cols);
  return [c * CELL, r * CELL + 2, CELL - 1, CELL - 1];
}

function drawCell(n, status) {
  const [x, y, w, h] = cellPos(n);
  ctx.fillStyle = status === 'prime' ? '#c8922a' :
                  status === 'composite' ? '#1a1a1a' :
                  status === 'marking' ? '#e84040' :
                  '#333';
  ctx.fillRect(x, y, w, h);
  if (status !== 'composite' && CELL >= 12) {
    ctx.fillStyle = status === 'prime' ? '#000' : '#999';
    ctx.font = `${Math.floor(CELL * 0.5)}px monospace`;
    ctx.textAlign = 'center';
    ctx.fillText(n, x + w / 2, y + h * 0.7);
  }
}

let markIdx = 0;
let marklist = [];

function sieveStep() {
  if (!running) return;

  if (marklist.length > 0 && markIdx < marklist.length) {
    // Mark composites of currentPrime
    const n = marklist[markIdx];
    state[n] = 'composite';
    composites.add(n);
    drawCell(n, 'composite');
    markIdx++;
    animId = setTimeout(sieveStep, 30);
    return;
  }

  // Declare current prime
  if (currentPrime <= LIMIT && !composites.has(currentPrime)) {
    state[currentPrime] = 'prime';
    drawCell(currentPrime, 'prime');
    window.__setStatus && window.__setStatus(`marking multiples of ${currentPrime} — click to restart`);
    // Build marklist of multiples
    marklist = [];
    for (let m = currentPrime * currentPrime; m <= LIMIT; m += currentPrime) {
      if (state[m] === 'unknown') marklist.push(m);
    }
    markIdx = 0;
    currentPrime++;
    animId = setTimeout(sieveStep, 200);
  } else if (currentPrime <= LIMIT) {
    currentPrime++;
    animId = setTimeout(sieveStep, 50);
  } else {
    // Mark remaining as prime
    for (let n = 2; n <= LIMIT; n++) {
      if (state[n] === 'unknown') { state[n] = 'prime'; drawCell(n, 'prime'); }
    }
    const count = [...state].filter(s => s === 'prime').length;
    window.__setStatus && window.__setStatus(`${count} primes ≤ ${LIMIT} — click to restart`);
  }
}

window.__programRestart = init;
init();
