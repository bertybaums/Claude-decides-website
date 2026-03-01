// Game Theory — Iterated Prisoner's Dilemma Tournament
// Strategies compete over 200 rounds; scores accumulate as animated bars
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const AMBER = '#c8922a';
const BG = '#0f0f0f';
const WHITE = '#e8e4dc';
const DIMTEXT = '#6b6560';

const W = canvas.width;
const H = canvas.height;

// Payoff matrix (row player gets):
//              Col: C    Col: D
// Row: C         3,3      0,5
// Row: D         5,0      1,1
const PAYOFF = {
  CC: [3, 3],
  CD: [0, 5],
  DC: [5, 0],
  DD: [1, 1],
};

function getPayoff(rowMove, colMove) {
  const key = rowMove + colMove;
  return PAYOFF[key];
}

// Strategy definitions
const STRATEGIES = [
  {
    name: 'Tit-for-Tat',
    color: AMBER,
    fn: (myHistory, oppHistory) => oppHistory.length === 0 ? 'C' : oppHistory[oppHistory.length - 1],
  },
  {
    name: 'Always Cooperate',
    color: '#4a9a4a',
    fn: () => 'C',
  },
  {
    name: 'Always Defect',
    color: '#cc4444',
    fn: () => 'D',
  },
  {
    name: 'Grudger',
    color: '#6688cc',
    fn: (myHistory, oppHistory) => oppHistory.includes('D') ? 'D' : 'C',
  },
  {
    name: 'Random',
    color: '#aa66aa',
    fn: () => Math.random() < 0.5 ? 'C' : 'D',
  },
];

const N_ROUNDS = 200;
const N = STRATEGIES.length;

// Pre-compute all matchups
function runTournament() {
  // scores[i] = total score for strategy i
  const scores = new Array(N).fill(0);
  // Round-by-round cumulative scores for animation
  const scoreHistory = Array.from({length: N}, () => [0]);

  for (let i = 0; i < N; i++) {
    for (let j = 0; j < N; j++) {
      if (i === j) continue; // skip self-play
      const mhI = [], mhJ = [];
      let cumI = 0, cumJ = 0;
      for (let r = 0; r < N_ROUNDS; r++) {
        const mI = STRATEGIES[i].fn(mhI, mhJ);
        const mJ = STRATEGIES[j].fn(mhJ, mhI);
        const [pi, pj] = getPayoff(mI, mJ);
        cumI += pi; cumJ += pj;
        mhI.push(mI); mhJ.push(mJ);
      }
      scores[i] += cumI;
      scores[j] += cumJ;
    }
  }

  // Build per-round cumulative scores by re-running all matchups round by round
  const roundScores = Array.from({length: N}, () => new Array(N_ROUNDS + 1).fill(0));

  for (let i = 0; i < N; i++) {
    for (let j = 0; j < N; j++) {
      if (i === j) continue;
      const mhI = [], mhJ = [];
      let cumI = 0;
      for (let r = 0; r < N_ROUNDS; r++) {
        const mI = STRATEGIES[i].fn(mhI, mhJ);
        const mJ = STRATEGIES[j].fn(mhJ, mhI);
        const [pi] = getPayoff(mI, mJ);
        cumI += pi;
        roundScores[i][r + 1] += roundScores[i][r] + pi;
        mhI.push(mI); mhJ.push(mJ);
      }
    }
    // Fix cumulative by recalculating properly
  }

  // Simpler: compute round-by-round totals
  const perRound = Array.from({length: N}, () => new Array(N_ROUNDS).fill(0));
  for (let i = 0; i < N; i++) {
    for (let j = 0; j < N; j++) {
      if (i === j) continue;
      const mhI = [], mhJ = [];
      for (let r = 0; r < N_ROUNDS; r++) {
        const mI = STRATEGIES[i].fn(mhI, mhJ);
        const mJ = STRATEGIES[j].fn(mhJ, mhI);
        const [pi] = getPayoff(mI, mJ);
        perRound[i][r] += pi;
        mhI.push(mI); mhJ.push(mJ);
      }
    }
  }

  // Cumulative
  const cumulative = Array.from({length: N}, () => [0]);
  for (let r = 0; r < N_ROUNDS; r++) {
    for (let i = 0; i < N; i++) {
      cumulative[i].push(cumulative[i][r] + perRound[i][r]);
    }
  }

  return { cumulative };
}

let tournament = null;
let currentRound = 0;
let running = true;
let phaseTimeout = null;

const BAR_X = 60;
const BAR_Y = 80;
const BAR_H_AREA = H - 280;
const BAR_W_MAX = W - 180;

const MATRIX_Y = BAR_Y + BAR_H_AREA + 60;
const ROW_H = 26;

function drawMatrix() {
  const labels = STRATEGIES.map(s => s.name.substring(0, 3));
  const mx = 60, my = MATRIX_Y;
  const cellW = 60, cellH = 20;

  ctx.fillStyle = DIMTEXT;
  ctx.font = '11px monospace';
  ctx.fillText('Payoff matrix (row player):', mx, my - 10);

  // Header row
  const moves = ['C', 'D'];
  const outcomes = [['3','0'],['5','1']];
  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  ctx.fillText('', mx, my + 10);

  const cases = [
    { row: 'C', col: 'C', rowGets: 3, colGets: 3, label: 'Both cooperate' },
    { row: 'C', col: 'D', rowGets: 0, colGets: 5, label: 'Sucker\'s payoff' },
    { row: 'D', col: 'C', rowGets: 5, colGets: 0, label: 'Temptation' },
    { row: 'D', col: 'D', rowGets: 1, colGets: 1, label: 'Mutual defect' },
  ];

  const cols = ['Move', 'Opp', 'You get', 'They get', 'Name'];
  const colW = [60, 60, 80, 90, 160];
  let cx = mx;
  for (let c = 0; c < cols.length; c++) {
    ctx.fillStyle = DIMTEXT;
    ctx.font = '11px monospace';
    ctx.fillText(cols[c], cx, my + 6);
    cx += colW[c];
  }

  for (let i = 0; i < cases.length; i++) {
    const ca = cases[i];
    const ry = my + 20 + i * 18;
    let cx2 = mx;
    const data = [ca.row, ca.col, String(ca.rowGets), String(ca.colGets), ca.label];
    for (let c = 0; c < data.length; c++) {
      ctx.fillStyle = ca.rowGets === 5 ? AMBER : ca.rowGets === 0 ? '#cc4444' : '#888';
      ctx.font = '11px monospace';
      ctx.fillText(data[c], cx2, ry);
      cx2 += colW[c];
    }
  }
}

function draw(round) {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText("Prisoner's Dilemma Tournament", BAR_X, 36);

  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  ctx.fillText(`round ${round} / ${N_ROUNDS}`, BAR_X, 56);

  if (!tournament) return;

  const maxScore = Math.max(...tournament.cumulative.map(c => c[N_ROUNDS]));

  // Sort by score at current round for display order
  const order = STRATEGIES.map((_, i) => i)
    .sort((a, b) => tournament.cumulative[b][round] - tournament.cumulative[a][round]);

  const barH = Math.floor((BAR_H_AREA - (N - 1) * 12) / N);

  for (let rank = 0; rank < N; rank++) {
    const i = order[rank];
    const score = tournament.cumulative[i][round];
    const by = BAR_Y + rank * (barH + 12);
    const bw = (score / maxScore) * BAR_W_MAX;

    // Background track
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(BAR_X, by, BAR_W_MAX, barH);

    // Bar
    ctx.fillStyle = STRATEGIES[i].color;
    ctx.fillRect(BAR_X, by, Math.max(0, bw), barH);

    // Name
    ctx.fillStyle = '#111';
    ctx.font = `bold ${Math.min(13, barH - 4)}px monospace`;
    if (bw > 100) {
      ctx.fillText(STRATEGIES[i].name, BAR_X + 6, by + barH - 5);
    } else {
      ctx.fillStyle = STRATEGIES[i].color;
      ctx.fillText(STRATEGIES[i].name, BAR_X + Math.max(0, bw) + 6, by + barH - 5);
    }

    // Score
    ctx.fillStyle = WHITE;
    ctx.font = '12px monospace';
    ctx.fillText(score.toLocaleString(), BAR_X + BAR_W_MAX + 8, by + barH - 5);

    // Rank
    ctx.fillStyle = DIMTEXT;
    ctx.font = '11px monospace';
    ctx.fillText(`#${rank + 1}`, BAR_X - 30, by + barH - 5);
  }

  // Draw payoff matrix
  drawMatrix();
}

function advance() {
  if (!running) return;
  if (currentRound >= N_ROUNDS) {
    const order = STRATEGIES.map((_, i) => i)
      .sort((a, b) => tournament.cumulative[b][N_ROUNDS] - tournament.cumulative[a][N_ROUNDS]);
    const winner = STRATEGIES[order[0]].name;
    window.__setStatus && window.__setStatus(`round ${N_ROUNDS}/${N_ROUNDS} — ${winner} wins — click to restart`);
    return;
  }

  currentRound = Math.min(currentRound + 2, N_ROUNDS);
  draw(currentRound);
  window.__setStatus && window.__setStatus(`round ${currentRound}/${N_ROUNDS} — click to restart`);
  const delay = currentRound < 20 ? 80 : currentRound < 100 ? 30 : 15;
  phaseTimeout = setTimeout(advance, delay);
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  if (phaseTimeout) clearTimeout(phaseTimeout);
  tournament = runTournament();
  currentRound = 0;
  draw(0);
  window.__setStatus && window.__setStatus('round 0/200 — click to restart');
  phaseTimeout = setTimeout(advance, 500);
}

window.__programRestart = init;
init();
