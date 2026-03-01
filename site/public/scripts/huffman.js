// Huffman Coding — building the optimal prefix-free code tree
// Merge lowest-frequency nodes bottom-up, animate the process
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const AMBER = '#c8922a';
const BG = '#0f0f0f';
const WHITE = '#e8e4dc';
const DIMTEXT = '#6b6560';
const DIM_NODE = '#2a2520';

const W = canvas.width;
const H = canvas.height;

// Sample text frequencies (English letter subset for clarity)
const FREQ_TABLE = [
  { char: 'E', freq: 127 },
  { char: 'T', freq: 91 },
  { char: 'A', freq: 82 },
  { char: 'O', freq: 75 },
  { char: 'I', freq: 70 },
  { char: 'N', freq: 67 },
  { char: 'S', freq: 63 },
  { char: 'H', freq: 61 },
  { char: 'R', freq: 60 },
  { char: 'D', freq: 43 },
  { char: 'L', freq: 40 },
  { char: 'C', freq: 28 },
];

// Huffman node
function makeLeaf(char, freq) {
  return { char, freq, left: null, right: null, isLeaf: true, code: '' };
}

function makeInternal(left, right) {
  return { char: null, freq: left.freq + right.freq, left, right, isLeaf: false, code: '' };
}

// Build Huffman tree step by step, returning intermediate states
function buildSteps(table) {
  // Start with leaf nodes sorted by freq
  let queue = table.map(({ char, freq }) => makeLeaf(char, freq));
  queue.sort((a, b) => a.freq - b.freq);

  const steps = [JSON.parse(JSON.stringify(queue))];

  while (queue.length > 1) {
    const a = queue.shift();
    const b = queue.shift();
    const merged = makeInternal(a, b);
    // Insert in sorted position
    let pos = 0;
    while (pos < queue.length && queue[pos].freq < merged.freq) pos++;
    queue.splice(pos, 0, merged);
    steps.push(JSON.parse(JSON.stringify(queue)));
  }

  return { steps, root: queue[0] };
}

// Assign codes by traversing the tree
function assignCodes(node, code = '') {
  if (!node) return {};
  node.code = code;
  if (node.isLeaf) return { [node.char]: code || '0' };
  return {
    ...assignCodes(node.left, code + '0'),
    ...assignCodes(node.right, code + '1'),
  };
}

// Layout the tree for drawing
// Returns { nodes: [{node, x, y}], edges: [{x1,y1,x2,y2,label}] }
function layoutTree(root) {
  if (!root) return { nodes: [], edges: [] };

  // Count leaves to determine width
  function countLeaves(n) {
    if (!n || n.isLeaf) return 1;
    return countLeaves(n.left) + countLeaves(n.right);
  }

  const nLeaves = countLeaves(root);
  const TREE_X = 30;
  const TREE_Y_TOP = 60;
  const TREE_W = W - 60;
  const TREE_H = H - 120;

  // Compute positions using in-order traversal for x
  let leafPos = 0;
  const positions = new Map();

  function depth(n) {
    if (!n || n.isLeaf) return 0;
    return 1 + Math.max(depth(n.left), depth(n.right));
  }
  const maxDepth = depth(root);

  function assignPos(n, d) {
    if (!n) return;
    if (n.isLeaf) {
      const x = TREE_X + (leafPos + 0.5) / nLeaves * TREE_W;
      const y = TREE_Y_TOP + TREE_H * 0.9;
      positions.set(n, { x, y });
      leafPos++;
    } else {
      assignPos(n.left, d + 1);
      assignPos(n.right, d + 1);
      const lx = positions.get(n.left).x;
      const rx = positions.get(n.right).x;
      const x = (lx + rx) / 2;
      const y = TREE_Y_TOP + (d / (maxDepth || 1)) * TREE_H * 0.9;
      positions.set(n, { x, y });
    }
  }
  assignPos(root, 0);

  const nodes = [];
  const edges = [];

  function collect(n) {
    if (!n) return;
    const { x, y } = positions.get(n);
    nodes.push({ node: n, x, y });
    if (n.left) {
      const { x: lx, y: ly } = positions.get(n.left);
      edges.push({ x1: x, y1: y, x2: lx, y2: ly, label: '0' });
      collect(n.left);
    }
    if (n.right) {
      const { x: rx, y: ry } = positions.get(n.right);
      edges.push({ x1: x, y1: y, x2: rx, y2: ry, label: '1' });
      collect(n.right);
    }
  }
  collect(root);

  return { nodes, edges };
}

const { steps, root } = buildSteps(FREQ_TABLE);
const codes = assignCodes(root);
const totalFreq = FREQ_TABLE.reduce((s, { freq }) => s + freq, 0);
const avgBits = Object.entries(codes).reduce((s, [ch, code]) => {
  const freq = FREQ_TABLE.find(f => f.char === ch)?.freq || 0;
  return s + (freq / totalFreq) * code.length;
}, 0);

const { nodes: treeNodes, edges: treeEdges } = layoutTree(root);

let stepIdx = 0;
let showingTree = false;
let running = true;
let phaseTimeout = null;

// Queue step visualization
const QUEUE_Y = 40;
const QUEUE_NODE_R = 22;

function drawQueueStep(queue) {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText('Huffman Tree — building bottom-up', 30, 26);

  const n = queue.length;
  const spacing = Math.min(80, (W - 60) / Math.max(n, 1));
  const startX = (W - spacing * (n - 1)) / 2;

  // Instructions
  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  const isFirst = stepIdx === 0;
  if (isFirst) {
    ctx.fillText('Start: leaf nodes sorted by frequency', 30, H - 20);
  } else {
    ctx.fillText(`Step ${stepIdx}: merged two smallest → internal node (freq sum)`, 30, H - 20);
  }

  queue.forEach((node, i) => {
    const x = startX + i * spacing;
    const y = QUEUE_Y + 80;
    const isNew = i === 0 && !isFirst;

    ctx.beginPath();
    ctx.arc(x, y, QUEUE_NODE_R, 0, Math.PI * 2);
    ctx.fillStyle = node.isLeaf ? AMBER : (isNew ? '#555' : DIM_NODE);
    ctx.fill();
    ctx.strokeStyle = isNew ? '#888' : node.isLeaf ? '#6b4a10' : '#333';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.fillStyle = node.isLeaf ? BG : WHITE;
    ctx.font = `bold ${node.isLeaf ? 13 : 11}px monospace`;
    ctx.textAlign = 'center';
    ctx.fillText(node.isLeaf ? node.char : '·', x, y + 5);
    ctx.textAlign = 'left';

    // Frequency label
    ctx.fillStyle = DIMTEXT;
    ctx.font = '11px monospace';
    ctx.textAlign = 'center';
    ctx.fillText(String(node.freq), x, y + QUEUE_NODE_R + 14);
    ctx.textAlign = 'left';

    // If internal, show children below
    if (!node.isLeaf && node.left && node.right) {
      drawSubtreeCompact(node, x, y + QUEUE_NODE_R + 30, 0, spacing * 0.7);
    }
  });
}

function drawSubtreeCompact(node, x, y, depth, spread) {
  if (!node || depth > 3) return;
  const nodeR = 14 - depth * 2;

  if (node.left) {
    const lx = x - spread / 2;
    const ly = y + 36;
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(lx, ly);
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(lx, ly, nodeR, 0, Math.PI * 2);
    ctx.fillStyle = node.left.isLeaf ? AMBER : DIM_NODE;
    ctx.fill();
    ctx.fillStyle = node.left.isLeaf ? BG : DIMTEXT;
    ctx.font = `${Math.max(8, 11 - depth * 2)}px monospace`;
    ctx.textAlign = 'center';
    ctx.fillText(node.left.isLeaf ? node.left.char : node.left.freq, lx, ly + 4);
    ctx.textAlign = 'left';

    drawSubtreeCompact(node.left, lx, ly, depth + 1, spread * 0.5);
  }

  if (node.right) {
    const rx = x + spread / 2;
    const ry = y + 36;
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(rx, ry);
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(rx, ry, nodeR, 0, Math.PI * 2);
    ctx.fillStyle = node.right.isLeaf ? AMBER : DIM_NODE;
    ctx.fill();
    ctx.fillStyle = node.right.isLeaf ? BG : DIMTEXT;
    ctx.font = `${Math.max(8, 11 - depth * 2)}px monospace`;
    ctx.textAlign = 'center';
    ctx.fillText(node.right.isLeaf ? node.right.char : node.right.freq, rx, ry + 4);
    ctx.textAlign = 'left';

    drawSubtreeCompact(node.right, rx, ry, depth + 1, spread * 0.5);
  }
}

const NODE_R = 16;

function drawFullTree() {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText('Huffman Tree — complete', 30, 26);

  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  ctx.fillText(`avg code length: ${avgBits.toFixed(2)} bits/char  |  optimal prefix-free encoding`, 30, 46);

  // Draw edges
  for (const e of treeEdges) {
    ctx.strokeStyle = '#2a2520';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(e.x1, e.y1);
    ctx.lineTo(e.x2, e.y2);
    ctx.stroke();

    // Edge label (0/1)
    const mx = (e.x1 + e.x2) / 2;
    const my = (e.y1 + e.y2) / 2;
    ctx.fillStyle = '#555';
    ctx.font = '10px monospace';
    ctx.fillText(e.label, mx + 2, my);
  }

  // Draw nodes
  for (const { node, x, y } of treeNodes) {
    ctx.beginPath();
    ctx.arc(x, y, NODE_R, 0, Math.PI * 2);
    ctx.fillStyle = node.isLeaf ? AMBER : DIM_NODE;
    ctx.fill();
    ctx.strokeStyle = node.isLeaf ? '#6b4a10' : '#333';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.textAlign = 'center';
    if (node.isLeaf) {
      ctx.fillStyle = BG;
      ctx.font = 'bold 13px monospace';
      ctx.fillText(node.char, x, y - 2);
      ctx.font = '9px monospace';
      ctx.fillText(node.freq, x, y + 10);

      // Code below leaf
      ctx.fillStyle = AMBER;
      ctx.font = '10px monospace';
      ctx.fillText(node.code, x, y + NODE_R + 14);
    } else {
      ctx.fillStyle = DIMTEXT;
      ctx.font = '10px monospace';
      ctx.fillText(node.freq, x, y + 4);
    }
    ctx.textAlign = 'left';
  }

  // Code table
  const TABLE_X = W - 180;
  ctx.fillStyle = DIMTEXT;
  ctx.font = '11px monospace';
  ctx.fillText('char  code   bits', TABLE_X, 70);
  FREQ_TABLE.slice(0, 10).forEach(({ char }, i) => {
    const code = codes[char] || '';
    ctx.fillStyle = AMBER;
    ctx.font = '11px monospace';
    ctx.fillText(`  ${char}    ${code.padEnd(8)} ${code.length}`, TABLE_X, 88 + i * 16);
  });
}

function nextStep() {
  if (!running) return;

  if (stepIdx < steps.length) {
    drawQueueStep(steps[stepIdx]);
    window.__setStatus && window.__setStatus(`step ${stepIdx}/${steps.length - 1} — building tree — click to restart`);
    stepIdx++;
    phaseTimeout = setTimeout(nextStep, stepIdx === 1 ? 1200 : 900);
  } else if (!showingTree) {
    showingTree = true;
    drawFullTree();
    window.__setStatus && window.__setStatus(`tree complete — avg ${avgBits.toFixed(2)} bits/char — click to restart`);
  }
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  if (phaseTimeout) clearTimeout(phaseTimeout);
  stepIdx = 0;
  showingTree = false;
  draw();
  window.__setStatus && window.__setStatus('building Huffman tree — click to restart');
  phaseTimeout = setTimeout(nextStep, 400);
}

function draw() {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText('Huffman Coding', 30, 30);
  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  ctx.fillText('initializing...', 30, 60);
}

window.__programRestart = init;
init();
