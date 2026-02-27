// Pascal's Triangle mod 2 — produces Sierpiński triangle
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');

function init() {
  const W = canvas.width, H = canvas.height;
  const CELL = Math.max(2, Math.floor(Math.min(W, H * 2) / 256));
  const rows = Math.floor(H / CELL);
  const cols = rows * 2;

  ctx.fillStyle = '#0f0f0f';
  ctx.fillRect(0, 0, W, H);

  // Build Pascal's triangle row by row using XOR (mod 2)
  let row = new Uint8Array(cols).fill(0);
  row[Math.floor(cols / 2)] = 1;

  for (let r = 0; r < rows; r++) {
    const next = new Uint8Array(cols).fill(0);
    for (let c = 0; c < cols; c++) {
      if (row[c]) {
        ctx.fillStyle = '#c8922a';
        const px = Math.floor(c * CELL);
        const py = r * CELL;
        ctx.fillRect(px, py, CELL, CELL);
      }
      next[c] = (row[(c - 1 + cols) % cols] + row[(c + 1) % cols]) % 2;
    }
    row = next;
  }

  window.__setStatus && window.__setStatus("Pascal's triangle mod 2 = Sierpiński triangle — click to re-render");
}

window.__programRestart = init;
init();
