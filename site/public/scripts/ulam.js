// Ulam Spiral — primes arranged in a spiral reveal diagonal patterns
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

function sieve(n) {
  const isPrime = new Uint8Array(n + 1).fill(1);
  isPrime[0] = isPrime[1] = 0;
  for (let i = 2; i * i <= n; i++)
    if (isPrime[i]) for (let j = i * i; j <= n; j += i) isPrime[j] = 0;
  return isPrime;
}

function init() {
  const W = canvas.width, H = canvas.height;
  const CELL = 5;
  const cols = Math.floor(W / CELL);
  const rows = Math.floor(H / CELL);
  const N = cols * rows;

  const isPrime = sieve(N + 1);

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  // Generate spiral coordinates
  let x = Math.floor(cols / 2), y = Math.floor(rows / 2);
  let dx = 1, dy = 0;
  let segLen = 1, segCount = 0, turns = 0;

  for (let n = 1; n <= N; n++) {
    if (x >= 0 && x < cols && y >= 0 && y < rows) {
      if (isPrime[n]) {
        const t = n / N;
        const r = Math.floor(180 + t * 40);
        const g = Math.floor(80 + t * 40);
        const b = Math.floor(20 + t * 20);
        ctx.fillStyle = `rgb(${r},${g},${b})`;
        ctx.fillRect(x * CELL, y * CELL, CELL - 1, CELL - 1);
      }
    }

    x += dx; y += dy;
    segCount++;
    if (segCount === segLen) {
      segCount = 0;
      // Turn left
      [dx, dy] = [-dy, dx];
      turns++;
      if (turns % 2 === 0) segLen++;
    }
  }

  window.__setStatus && window.__setStatus(`Ulam spiral — ${isPrime.reduce((s, v) => s + v, 0)} primes up to ${N} — diagonal lines emerge — click to re-render`);
}

window.__programRestart = init;
init();
