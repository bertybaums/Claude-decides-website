// Prime Gaps — the irregular rhythm of the primes
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

function init() {
  const W = canvas.width, H = canvas.height;
  const LIMIT = 5000;

  // Sieve
  const isPrime = new Uint8Array(LIMIT + 1).fill(1);
  isPrime[0] = isPrime[1] = 0;
  for (let i = 2; i * i <= LIMIT; i++)
    if (isPrime[i]) for (let j = i * i; j <= LIMIT; j += i) isPrime[j] = 0;

  const primes = [];
  for (let i = 2; i <= LIMIT; i++) if (isPrime[i]) primes.push(i);

  const gaps = [];
  for (let i = 1; i < primes.length; i++) gaps.push(primes[i] - primes[i - 1]);

  const maxGap = Math.max(...gaps);
  const padding = { t: 30, b: 40, l: 50, r: 20 };
  const plotW = W - padding.l - padding.r;
  const plotH = H - padding.t - padding.b;

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  // Draw bars
  const barW = plotW / gaps.length;
  for (let i = 0; i < gaps.length; i++) {
    const barH = (gaps[i] / maxGap) * plotH;
    const t = gaps[i] / maxGap;
    ctx.fillStyle = `hsl(${200 + t * 40}, 60%, ${30 + t * 40}%)`;
    ctx.fillRect(
      padding.l + i * barW,
      padding.t + plotH - barH,
      Math.max(1, barW - 0.3),
      barH
    );
  }

  // Axes
  ctx.fillStyle = '#555';
  ctx.font = '10px monospace';
  ctx.fillText('gap size', 2, padding.t + plotH / 2);
  ctx.fillText('0', padding.l - 20, padding.t + plotH + 14);
  ctx.fillText('5000', W - 60, padding.t + plotH + 14);
  ctx.fillText(`max gap: ${maxGap}`, padding.l, padding.t - 8);

  // Highlight twin primes (gap=2)
  const twinCount = gaps.filter(g => g === 2).length;
  ctx.fillStyle = '#c8922a';
  ctx.fillText(`twin primes (gap=2): ${twinCount}`, W / 2 - 80, padding.t - 8);

  window.__setStatus && window.__setStatus(`${primes.length} primes up to ${LIMIT} — gaps plotted — click to re-render`);
}

window.__programRestart = init;
init();
