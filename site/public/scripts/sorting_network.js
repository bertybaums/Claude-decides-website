// Sorting Network — Bitonic Sort Visualization
// 16 wires. Animate data flowing through comparators.
// Values swap if out of order at each comparator. Color wires by value (hue).
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const N = 16; // wires

// Generate bitonic sort comparator network for N=16
// Returns list of layers; each layer is list of [i,j] pairs (independent comparators)
function bitonicNetwork(n) {
  const layers = [];
  function bitonicMerge(lo, cnt, asc) {
    if (cnt <= 1) return;
    const k = cnt >> 1;
    const layer = [];
    for (let i = lo; i < lo + k; i++) {
      layer.push(asc ? [i, i + k] : [i + k, i]);
    }
    layers.push(layer);
    bitonicMerge(lo, k, asc);
    bitonicMerge(lo + k, k, asc);
  }
  function bitonicSort(lo, cnt, asc) {
    if (cnt <= 1) return;
    const k = cnt >> 1;
    bitonicSort(lo, k, true);
    bitonicSort(lo + k, k, false);
    bitonicMerge(lo, cnt, asc);
  }
  bitonicSort(0, n, true);
  return layers;
}

const LAYERS = bitonicNetwork(N);
const TOTAL_LAYERS = LAYERS.length;

let values, displayValues, layerIdx, animProgress, swapping, swaps;
let wireY, wireX0, wireX1, layerXs;

function computeLayout() {
  const W = canvas.width, H = canvas.height;
  const topPad = H * 0.12, botPad = H * 0.12;
  const leftPad = W * 0.06, rightPad = W * 0.06;
  const wireSpacing = (H - topPad - botPad) / (N - 1);

  wireY = Array.from({ length: N }, (_, i) => topPad + i * wireSpacing);
  wireX0 = leftPad;
  wireX1 = W - rightPad;

  // X positions for each layer
  const layerW = (wireX1 - wireX0) / (TOTAL_LAYERS + 1);
  layerXs = Array.from({ length: TOTAL_LAYERS }, (_, i) => wireX0 + (i + 0.5) * layerW);
}

function valueToHue(v, n) {
  return (v / (n - 1)) * 270; // blue (cold) to red (hot)... actually use 0-270
}

function hslToStr(h, s, l) {
  return `hsl(${h},${s}%,${l}%)`;
}

function init() {
  cancelAnimationFrame(animId);
  computeLayout();

  // Random permutation of 0..N-1
  values = Array.from({ length: N }, (_, i) => i);
  for (let i = values.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [values[i], values[j]] = [values[j], values[i]];
  }
  displayValues = [...values];
  layerIdx = 0;
  animProgress = 0;
  swapping = false;
  swaps = [];

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  window.__setStatus && window.__setStatus(`sorting ${N} elements — click to restart`);
  run();
}

function drawState(highlightLayer, progress) {
  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw wires
  for (let w = 0; w < N; w++) {
    const hue = valueToHue(displayValues[w], N);
    ctx.strokeStyle = hslToStr(hue, 80, 60);
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(wireX0, wireY[w]);
    ctx.lineTo(wireX1, wireY[w]);
    ctx.stroke();
  }

  // Draw comparator connectors for each layer
  for (let li = 0; li < TOTAL_LAYERS; li++) {
    const lx = layerXs[li];
    const layer = LAYERS[li];
    const isActive = li === highlightLayer;

    for (const [i, j] of layer) {
      const lo = Math.min(i, j), hi = Math.max(i, j);
      const y1 = wireY[lo], y2 = wireY[hi];

      if (isActive) {
        ctx.strokeStyle = 'rgba(255,255,255,0.85)';
        ctx.lineWidth = 2.5;
      } else if (li < highlightLayer) {
        ctx.strokeStyle = 'rgba(80,80,80,0.5)';
        ctx.lineWidth = 1;
      } else {
        ctx.strokeStyle = 'rgba(120,120,120,0.4)';
        ctx.lineWidth = 1;
      }

      // Vertical connector
      ctx.beginPath();
      ctx.moveTo(lx, y1);
      ctx.lineTo(lx, y2);
      ctx.stroke();

      // Endpoints
      ctx.fillStyle = isActive ? '#fff' : (li < highlightLayer ? '#555' : '#666');
      ctx.beginPath();
      ctx.arc(lx, y1, isActive ? 5 : 3, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(lx, y2, isActive ? 5 : 3, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // Animate swap: move values along wires during active layer
  if (highlightLayer < TOTAL_LAYERS && progress > 0) {
    for (const [i, j, swapped] of swaps) {
      const lo = Math.min(i, j), hi = Math.max(i, j);
      const lx = layerXs[highlightLayer];

      if (swapped) {
        // Show crossing wires
        const y1 = wireY[lo], y2 = wireY[hi];
        const hue1 = valueToHue(displayValues[lo], N);
        const hue2 = valueToHue(displayValues[hi], N);

        // Draw moving dots at intersection
        const ox = (lx - wireX0) * progress;
        ctx.fillStyle = hslToStr(hue2, 90, 70); // was hi, now going to lo
        ctx.beginPath();
        ctx.arc(wireX0 + ox, y1 + (y2 - y1) * progress, 6, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = hslToStr(hue1, 90, 70);
        ctx.beginPath();
        ctx.arc(wireX0 + ox, y2 + (y1 - y2) * progress, 6, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }

  // Value labels at right
  ctx.font = `${Math.max(9, Math.floor(canvas.height / (N * 2.5)))}px monospace`;
  for (let w = 0; w < N; w++) {
    const hue = valueToHue(displayValues[w], N);
    ctx.fillStyle = hslToStr(hue, 80, 65);
    ctx.fillText(String(displayValues[w]).padStart(2), wireX1 + 4, wireY[w] + 4);
  }
}

let pauseFrames = 0;

function run() {
  if (pauseFrames > 0) {
    pauseFrames--;
    animId = requestAnimationFrame(run);
    return;
  }

  if (layerIdx >= TOTAL_LAYERS) {
    // Done — restart with new array after pause
    drawState(TOTAL_LAYERS, 0);
    window.__setStatus && window.__setStatus(`sorted — ${TOTAL_LAYERS} layers, ${LAYERS.reduce((s,l)=>s+l.length,0)} comparators — click to restart`);
    pauseFrames = 80;
    // Reset after pause
    setTimeout(() => {
      values = Array.from({ length: N }, (_, i) => i);
      for (let i = values.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [values[i], values[j]] = [values[j], values[i]];
      }
      displayValues = [...values];
      layerIdx = 0;
      animProgress = 0;
      swaps = [];
    }, 2200);
    animId = requestAnimationFrame(run);
    return;
  }

  animProgress += 0.06;

  if (animProgress >= 1) {
    // Apply swaps
    const layer = LAYERS[layerIdx];
    for (const [i, j] of layer) {
      const lo = Math.min(i, j), hi = Math.max(i, j);
      if (displayValues[lo] > displayValues[hi]) {
        [displayValues[lo], displayValues[hi]] = [displayValues[hi], displayValues[lo]];
      }
    }
    layerIdx++;
    animProgress = 0;
    swaps = [];
    pauseFrames = 4;
  } else {
    // Compute swaps for this layer
    if (animProgress < 0.06) {
      const layer = LAYERS[layerIdx];
      swaps = layer.map(([i, j]) => {
        const lo = Math.min(i, j), hi = Math.max(i, j);
        return [lo, hi, displayValues[lo] > displayValues[hi]];
      });
    }
    drawState(layerIdx, animProgress);
  }

  window.__setStatus && window.__setStatus(
    `layer ${layerIdx + 1}/${TOTAL_LAYERS} — sorting ${N} elements — click to restart`
  );
  animId = requestAnimationFrame(run);
}

canvas.addEventListener('click', init);
window.__programRestart = init;
init();
