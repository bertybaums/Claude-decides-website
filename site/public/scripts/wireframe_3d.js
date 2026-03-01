// 3D Rotating Wireframe — cube, icosahedron, dodecahedron
// Perspective projection with depth-based line brightness
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const AMBER = '#c8922a';
const BG = '#0f0f0f';
const WHITE = '#e8e4dc';
const DIMTEXT = '#6b6560';

const W = canvas.width;
const H = canvas.height;

// 3D math helpers
function rotX(v, a) {
  const [x,y,z] = v;
  const c = Math.cos(a), s = Math.sin(a);
  return [x, c*y - s*z, s*y + c*z];
}
function rotY(v, a) {
  const [x,y,z] = v;
  const c = Math.cos(a), s = Math.sin(a);
  return [c*x + s*z, y, -s*x + c*z];
}
function rotZ(v, a) {
  const [x,y,z] = v;
  const c = Math.cos(a), s = Math.sin(a);
  return [c*x - s*y, s*x + c*y, z];
}

function project(v, d = 4) {
  const [x,y,z] = v;
  const scale = d / (d + z + 3);
  return [x * scale, y * scale, z];
}

// Cube
const CUBE_VERTS = [
  [-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],
  [-1,-1, 1],[1,-1, 1],[1,1, 1],[-1,1, 1],
];
const CUBE_EDGES = [
  [0,1],[1,2],[2,3],[3,0], // back face
  [4,5],[5,6],[6,7],[7,4], // front face
  [0,4],[1,5],[2,6],[3,7], // connecting edges
];

// Icosahedron
const PHI = (1 + Math.sqrt(5)) / 2;
const ICO_VERTS_RAW = [
  [0, 1, PHI],[0,-1, PHI],[0, 1,-PHI],[0,-1,-PHI],
  [1, PHI, 0],[-1, PHI, 0],[1,-PHI, 0],[-1,-PHI, 0],
  [PHI, 0, 1],[-PHI, 0, 1],[PHI, 0,-1],[-PHI, 0,-1],
];
const ISCALE = 1 / Math.sqrt(1 + PHI * PHI);
const ICO_VERTS = ICO_VERTS_RAW.map(v => v.map(x => x * ISCALE));

// Icosahedron faces (from symmetry)
const ICO_FACES = [
  [0,1,8],[0,1,9],[0,4,5],[0,4,8],[0,5,9],
  [1,6,7],[1,6,8],[1,7,9],[2,3,10],[2,3,11],
  [2,4,5],[2,4,10],[2,5,11],[3,6,7],[3,6,10],
  [3,7,11],[4,8,10],[5,9,11],[6,8,10],[7,9,11],
];
// Build edges from faces (unique)
function facesToEdges(faces) {
  const edgeSet = new Set();
  const edges = [];
  for (const face of faces) {
    const n = face.length;
    for (let i = 0; i < n; i++) {
      const a = face[i], b = face[(i + 1) % n];
      const key = Math.min(a,b) + '_' + Math.max(a,b);
      if (!edgeSet.has(key)) {
        edgeSet.add(key);
        edges.push([a, b]);
      }
    }
  }
  return edges;
}
const ICO_EDGES = facesToEdges(ICO_FACES);

// Torus approximation using circles
function buildTorus(R, r, nR, nr) {
  const verts = [];
  const edges = [];
  for (let i = 0; i < nR; i++) {
    const theta = (2 * Math.PI * i) / nR;
    for (let j = 0; j < nr; j++) {
      const phi = (2 * Math.PI * j) / nr;
      const x = (R + r * Math.cos(phi)) * Math.cos(theta);
      const y = (R + r * Math.cos(phi)) * Math.sin(theta);
      const z = r * Math.sin(phi);
      verts.push([x / (R + r), y / (R + r), z / r * 0.8]);
    }
  }
  // Edges along rings
  for (let i = 0; i < nR; i++) {
    for (let j = 0; j < nr; j++) {
      const cur = i * nr + j;
      const nextI = ((i + 1) % nR) * nr + j;
      const nextJ = i * nr + (j + 1) % nr;
      edges.push([cur, nextI]);
      edges.push([cur, nextJ]);
    }
  }
  return { verts, edges };
}
const TORUS = buildTorus(1, 0.35, 24, 12);

// Objects to cycle through
const OBJECTS = [
  {
    name: 'Cube',
    verts: CUBE_VERTS.map(v => v.map(x => x * 0.7)),
    edges: CUBE_EDGES,
    duration: 6000,
  },
  {
    name: 'Icosahedron',
    verts: ICO_VERTS,
    edges: ICO_EDGES,
    duration: 7000,
  },
  {
    name: 'Torus',
    verts: TORUS.verts,
    edges: TORUS.edges,
    duration: 8000,
  },
];

let objIdx = 0;
let angleX = 0, angleY = 0, angleZ = 0;
let startTime = null;
let running = true;

function drawObject(obj, ax, ay, az) {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText('3D Wireframe Rotation', 30, 30);
  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  ctx.fillText(obj.name, 30, 50);

  const cx = W / 2;
  const cy = H / 2 + 20;
  const scale = Math.min(W, H) * 0.32;

  // Transform all vertices
  const transformed = obj.verts.map(v => {
    let p = v;
    p = rotX(p, ax);
    p = rotY(p, ay);
    p = rotZ(p, az);
    return p;
  });

  // Project to 2D
  const projected = transformed.map(v => {
    const [px, py, pz] = project(v);
    return [cx + px * scale, cy - py * scale, pz];
  });

  // Find depth range for coloring
  const depths = transformed.map(v => v[2]);
  const minZ = Math.min(...depths);
  const maxZ = Math.max(...depths);
  const zRange = maxZ - minZ || 1;

  // Draw edges, color by average depth of endpoints
  for (const [a, b] of obj.edges) {
    if (a >= projected.length || b >= projected.length) continue;
    const [ax2, ay2, az2] = projected[a];
    const [bx, by, bz] = projected[b];
    const avgZ = (az2 + bz) / 2;
    const t = (avgZ - minZ) / zRange; // 0 = back, 1 = front
    const brightness = Math.floor(60 + t * 180);
    const amberR = Math.floor(100 + t * 100);
    const amberG = Math.floor(80 + t * 60);
    const amberB = Math.floor(10 + t * 30);

    ctx.strokeStyle = `rgba(${amberR},${amberG},${amberB},${0.3 + t * 0.7})`;
    ctx.lineWidth = 0.5 + t * 1.5;
    ctx.beginPath();
    ctx.moveTo(ax2, ay2);
    ctx.lineTo(bx, by);
    ctx.stroke();
  }

  // Draw vertices
  for (let i = 0; i < projected.length; i++) {
    const [vx, vy, vz] = projected[i];
    const t = (transformed[i][2] - minZ) / zRange;
    const r2 = 1 + t * 2;
    ctx.beginPath();
    ctx.arc(vx, vy, r2, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(200, 146, 42, ${0.3 + t * 0.7})`;
    ctx.fill();
  }

  // Object info
  ctx.fillStyle = DIMTEXT;
  ctx.font = '11px monospace';
  ctx.fillText(`${obj.verts.length} vertices   ${obj.edges.length} edges`, 30, H - 20);
  ctx.fillText(`front = bright  back = dim`, W - 180, H - 20);
}

let lastSwitch = 0;

function animate(ts = 0) {
  if (!running) return;
  if (!startTime) startTime = ts;

  const elapsed = ts - startTime;
  const obj = OBJECTS[objIdx];

  // Rotation speeds vary per object
  const speeds = [[0.003, 0.007, 0.002], [0.005, 0.004, 0.006], [0.002, 0.008, 0.003]];
  const [sx, sy, sz] = speeds[objIdx % speeds.length];
  angleX += sx;
  angleY += sy;
  angleZ += sz;

  drawObject(obj, angleX, angleY, angleZ);
  window.__setStatus && window.__setStatus(`${obj.name} rotating — click to restart`);

  if (elapsed - lastSwitch > obj.duration) {
    lastSwitch = elapsed;
    objIdx = (objIdx + 1) % OBJECTS.length;
    angleX = Math.random() * Math.PI;
    angleY = Math.random() * Math.PI;
    angleZ = 0;
  }

  animId = requestAnimationFrame(animate);
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  objIdx = 0;
  angleX = 0.3; angleY = 0.5; angleZ = 0.1;
  startTime = null;
  lastSwitch = 0;
  window.__setStatus && window.__setStatus('rotating — click to restart');
  animId = requestAnimationFrame(animate);
}

window.__programRestart = init;
init();
