// Erdős-Rényi Random Graph — Giant Component
// n=80 nodes in a circle. Edges added slowly.
// Giant component highlighted in amber. Critical threshold p=1/n marked.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const N = 80;
const CRITICAL = 1 / N;
const CONNECTIVITY = Math.log(N) / N;
const NODE_RADIUS = 5;

let edges, parent, sz, edgeList, edgeIdx, p, frameDelay, frameCount;

// Union-Find
function makeUF() {
  parent = Array.from({ length: N }, (_, i) => i);
  sz = new Array(N).fill(1);
}
function find(x) {
  while (parent[x] !== x) { parent[x] = parent[parent[x]]; x = parent[x]; }
  return x;
}
function union(a, b) {
  const ra = find(a), rb = find(b);
  if (ra === rb) return;
  if (sz[ra] < sz[rb]) { parent[ra] = rb; sz[rb] += sz[ra]; }
  else { parent[rb] = ra; sz[ra] += sz[rb]; }
}
function componentOf(x) { return find(x); }

function giantComponent() {
  const count = {};
  for (let i = 0; i < N; i++) {
    const r = find(i);
    count[r] = (count[r] || 0) + 1;
  }
  let maxSize = 0, giantRoot = -1;
  for (const [r, s] of Object.entries(count)) {
    if (s > maxSize) { maxSize = s; giantRoot = parseInt(r); }
  }
  const inGiant = new Set();
  for (let i = 0; i < N; i++) {
    if (find(i) === giantRoot) inGiant.add(i);
  }
  return { size: maxSize, nodes: inGiant };
}

function nodePos(i) {
  const angle = (2 * Math.PI * i / N) - Math.PI / 2;
  const W = canvas.width, H = canvas.height;
  const rx = Math.min(W, H) * 0.40;
  const ry = Math.min(W, H) * 0.40;
  return [W / 2 + rx * Math.cos(angle), H / 2 + ry * Math.sin(angle)];
}

function shuffleEdges() {
  // All possible edges, shuffled
  const all = [];
  for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) all.push([i, j]);
  for (let i = all.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [all[i], all[j]] = [all[j], all[i]];
  }
  return all;
}

function init() {
  cancelAnimationFrame(animId);
  edges = [];
  makeUF();
  edgeList = shuffleEdges();
  edgeIdx = 0;
  p = 0;
  frameCount = 0;

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  window.__setStatus && window.__setStatus('p=0.000 — giant component: 0 nodes — click to restart');
  run();
}

function run() {
  const maxEdges = (N * (N - 1)) / 2;

  // Add a few edges per frame
  const addPerFrame = 1;
  for (let i = 0; i < addPerFrame && edgeIdx < edgeList.length; i++) {
    const [a, b] = edgeList[edgeIdx++];
    edges.push([a, b]);
    union(a, b);
  }

  p = edges.length / maxEdges;

  const { size: gSize, nodes: gNodes } = giantComponent();

  // Draw
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw threshold marker
  const critEdges = Math.round(CRITICAL * maxEdges);
  const connEdges = Math.round(CONNECTIVITY * maxEdges);
  const W = canvas.width;

  // Draw edges — dim for non-giant, amber for giant
  for (const [a, b] of edges) {
    const inG = gNodes.has(a) && gNodes.has(b);
    const [x1, y1] = nodePos(a);
    const [x2, y2] = nodePos(b);
    ctx.strokeStyle = inG ? 'rgba(200,146,42,0.45)' : 'rgba(80,80,80,0.3)';
    ctx.lineWidth = inG ? 1.2 : 0.6;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  // Draw nodes
  for (let i = 0; i < N; i++) {
    const [x, y] = nodePos(i);
    const inG = gNodes.has(i);
    ctx.fillStyle = inG ? '#c8922a' : '#444';
    ctx.beginPath();
    ctx.arc(x, y, inG ? NODE_RADIUS + 1 : NODE_RADIUS - 1, 0, Math.PI * 2);
    ctx.fill();
  }

  // Draw threshold line at bottom
  const barY = canvas.height - 18;
  const barX = 20, barW = W - 40;
  ctx.fillStyle = '#222';
  ctx.fillRect(barX, barY - 4, barW, 8);

  // Progress
  const progW = Math.min(1, p / 0.25) * barW;
  ctx.fillStyle = '#c8922a';
  ctx.fillRect(barX, barY - 3, progW, 6);

  // Mark critical threshold
  const critX = barX + (CRITICAL / 0.25) * barW;
  ctx.strokeStyle = '#f46';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(critX, barY - 10);
  ctx.lineTo(critX, barY + 10);
  ctx.stroke();

  ctx.fillStyle = '#f46';
  ctx.font = '10px monospace';
  ctx.fillText('1/n', critX - 8, barY - 12);

  window.__setStatus && window.__setStatus(`p=${p.toFixed(4)} — giant component: ${gSize} nodes — click to restart`);

  frameCount++;
  if (edgeIdx < edgeList.length) {
    animId = requestAnimationFrame(run);
  } else {
    window.__setStatus && window.__setStatus(`p=${p.toFixed(3)} — fully connected: ${gSize} nodes — click to restart`);
  }
}

canvas.addEventListener('click', init);
window.__programRestart = init;
init();
