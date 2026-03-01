// Gray-Scott Reaction-Diffusion — chemical pattern formation
// Two chemicals U and V interact:
//   dU/dt = Du·∇²U - U·V² + f·(1-U)
//   dV/dt = Dv·∇²V + U·V² - (f+k)·V
// Different (f,k) parameters produce spots, stripes, mazes — all from the same equations.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

let animId;

const SCALE = 2;
let GW, GH;
let U, V, Unext, Vnext;
let step = 0;
let presetIdx = 0;
let cycleStep = 0;   // step at which to cycle to next preset

const PRESETS = [
  { name: 'Spots',   f: 0.035, k: 0.065, Du: 0.16, Dv: 0.08 },
  { name: 'Stripes', f: 0.060, k: 0.062, Du: 0.16, Dv: 0.08 },
  { name: 'Maze',    f: 0.029, k: 0.057, Du: 0.16, Dv: 0.08 },
];

function initGrid() {
  const W = canvas.width, H = canvas.height;
  GW = Math.floor(W / SCALE);
  GH = Math.floor(H / SCALE);
  const n = GW * GH;
  U = new Float32Array(n);
  V = new Float32Array(n);
  Unext = new Float32Array(n);
  Vnext = new Float32Array(n);

  // U=1 everywhere, V=0 everywhere
  U.fill(1.0);
  V.fill(0.0);

  // Small random patch of V at center
  const patchR = Math.floor(Math.min(GW, GH) * 0.06);
  const cx = Math.floor(GW / 2);
  const cy = Math.floor(GH / 2);
  for (let dy = -patchR; dy <= patchR; dy++) {
    for (let dx = -patchR; dx <= patchR; dx++) {
      if (dx * dx + dy * dy <= patchR * patchR) {
        const i = (cy + dy) * GW + (cx + dx);
        if (i >= 0 && i < n) {
          U[i] = 0.5 + (Math.random() - 0.5) * 0.1;
          V[i] = 0.25 + (Math.random() - 0.5) * 0.1;
        }
      }
    }
  }
}

function laplacian(arr, x, y) {
  const n = GW * GH;
  const i  = y * GW + x;
  const ir = y * GW + ((x + 1) % GW);
  const il = y * GW + ((x - 1 + GW) % GW);
  const id = ((y + 1) % GH) * GW + x;
  const iu = ((y - 1 + GH) % GH) * GW + x;
  // 5-point stencil
  return arr[ir] + arr[il] + arr[id] + arr[iu] - 4 * arr[i];
}

function stepReaction(preset) {
  const { f, k, Du, Dv } = preset;
  const dt = 1.0;

  for (let y = 0; y < GH; y++) {
    for (let x = 0; x < GW; x++) {
      const i = y * GW + x;
      const u = U[i], v = V[i];
      const uvv = u * v * v;
      const lu = laplacian(U, x, y);
      const lv = laplacian(V, x, y);
      Unext[i] = Math.max(0, Math.min(1, u + dt * (Du * lu - uvv + f * (1 - u))));
      Vnext[i] = Math.max(0, Math.min(1, v + dt * (Dv * lv + uvv - (f + k) * v)));
    }
  }

  // Swap
  const tmp = U; U = Unext; Unext = tmp;
  const tmp2 = V; V = Vnext; Vnext = tmp2;
  step++;
}

function render() {
  const W = canvas.width, H = canvas.height;
  const imageData = ctx.createImageData(W, H);
  const data = imageData.data;

  for (let gy = 0; gy < GH; gy++) {
    for (let gx = 0; gx < GW; gx++) {
      const v = V[gy * GW + gx];
      // Map V concentration to color: dark=low, teal-white=high
      const t = Math.min(1, v * 4);  // amplify for visibility
      let r, g, b;
      if (t < 0.3) {
        const s = t / 0.3;
        r = Math.round(s * 0);
        g = Math.round(s * 60);
        b = Math.round(s * 80);
      } else if (t < 0.7) {
        const s = (t - 0.3) / 0.4;
        r = Math.round(s * 30);
        g = Math.round(60 + s * 130);
        b = Math.round(80 + s * 130);
      } else {
        const s = (t - 0.7) / 0.3;
        r = Math.round(30 + s * 200);
        g = Math.round(190 + s * 65);
        b = Math.round(210 + s * 45);
      }

      for (let dy = 0; dy < SCALE; dy++) {
        for (let dx = 0; dx < SCALE; dx++) {
          const px = gx * SCALE + dx;
          const py = gy * SCALE + dy;
          if (px >= W || py >= H) continue;
          const idx = (py * W + px) * 4;
          data[idx]   = r;
          data[idx+1] = g;
          data[idx+2] = b;
          data[idx+3] = 255;
        }
      }
    }
  }

  ctx.putImageData(imageData, 0, 0);
}

const STEPS_PER_FRAME = 8;
const STEPS_PER_PRESET = 4000;

function frame() {
  const preset = PRESETS[presetIdx];

  for (let i = 0; i < STEPS_PER_FRAME; i++) {
    stepReaction(preset);
  }

  render();

  const localStep = step - cycleStep;
  window.__setStatus && window.__setStatus(
    `${preset.name} — step ${localStep} — click to restart`
  );

  if (localStep >= STEPS_PER_PRESET) {
    // Move to next preset
    presetIdx = (presetIdx + 1) % PRESETS.length;
    cycleStep = step;
    // Re-seed
    initGrid();
  }

  animId = requestAnimationFrame(frame);
}

function init() {
  cancelAnimationFrame(animId);
  step = 0;
  presetIdx = 0;
  cycleStep = 0;
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  initGrid();
  window.__setStatus && window.__setStatus('Spots — step 0 — click to restart');
  animId = requestAnimationFrame(frame);
}

window.__programRestart = init;
init();
