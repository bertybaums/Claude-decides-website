// Genetic Algorithm — evolving bit strings toward a target
// Each row = one individual (bit string). Selection, crossover, mutation.
const canvas = document.getElementById('program-canvas');
const ctx = canvas.getContext('2d');
let animId;

const AMBER = '#c8922a';
const BG = '#0f0f0f';
const WHITE = '#e8e4dc';
const DIMTEXT = '#6b6560';

const W = canvas.width;
const H = canvas.height;

const BIT_LENGTH = 48;
const POP_SIZE = 30;
const MUTATION_RATE = 0.01;
const TOURNAMENT_K = 3;

// Fixed random target
const TARGET = Array.from({length: BIT_LENGTH}, () => Math.random() < 0.5 ? 1 : 0);

function fitness(individual) {
  let matches = 0;
  for (let i = 0; i < BIT_LENGTH; i++) {
    if (individual[i] === TARGET[i]) matches++;
  }
  return matches / BIT_LENGTH;
}

function randomIndividual() {
  return Array.from({length: BIT_LENGTH}, () => Math.random() < 0.5 ? 1 : 0);
}

function tournamentSelect(pop, fitnesses) {
  let best = -1, bestF = -1;
  for (let k = 0; k < TOURNAMENT_K; k++) {
    const idx = Math.floor(Math.random() * pop.length);
    if (fitnesses[idx] > bestF) { bestF = fitnesses[idx]; best = idx; }
  }
  return pop[best];
}

function crossover(a, b) {
  const point = 1 + Math.floor(Math.random() * (BIT_LENGTH - 2));
  return [...a.slice(0, point), ...b.slice(point)];
}

function mutate(individual) {
  return individual.map(bit => Math.random() < MUTATION_RATE ? 1 - bit : bit);
}

function nextGeneration(pop) {
  const fitnesses = pop.map(fitness);
  const newPop = [];
  for (let i = 0; i < POP_SIZE; i++) {
    const parent1 = tournamentSelect(pop, fitnesses);
    const parent2 = tournamentSelect(pop, fitnesses);
    let child = crossover(parent1, parent2);
    child = mutate(child);
    newPop.push(child);
  }
  return newPop;
}

// Layout
const CELL_W = Math.floor((W - 100) / BIT_LENGTH);
const CELL_H = Math.floor((H - 200) / (POP_SIZE + 2));
const GRID_X = 50;
const GRID_Y = 60;
const GRAPH_Y = GRID_Y + (POP_SIZE + 2) * (CELL_H + 1) + 20;
const GRAPH_H = H - GRAPH_Y - 30;

let population = [];
let generation = 0;
let bestFitnessHistory = [];
let avgFitnessHistory = [];
let running = true;
let phaseTimeout = null;

function draw() {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = WHITE;
  ctx.font = '14px monospace';
  ctx.fillText('Genetic Algorithm — bit string evolution', GRID_X, 30);

  ctx.fillStyle = DIMTEXT;
  ctx.font = '12px monospace';
  ctx.fillText(`generation ${generation}   pop=${POP_SIZE}   bits=${BIT_LENGTH}   μ=${MUTATION_RATE}`, GRID_X, 50);

  // Draw target row
  const targetY = GRID_Y;
  ctx.fillStyle = DIMTEXT;
  ctx.font = '10px monospace';
  ctx.fillText('target:', GRID_X - 44, targetY + CELL_H - 2);

  for (let j = 0; j < BIT_LENGTH; j++) {
    const x = GRID_X + j * (CELL_W + 0);
    ctx.fillStyle = TARGET[j] === 1 ? AMBER : '#1a1a1a';
    ctx.fillRect(x, targetY, CELL_W - 1, CELL_H);
  }

  // Draw separator
  ctx.fillStyle = '#333';
  ctx.fillRect(GRID_X, GRID_Y + CELL_H + 2, BIT_LENGTH * CELL_W, 1);

  if (population.length === 0) return;

  const fitnesses = population.map(fitness);
  const bestF = Math.max(...fitnesses);
  const bestIdx = fitnesses.indexOf(bestF);

  // Sort population by fitness for display
  const order = fitnesses.map((f, i) => [f, i]).sort((a, b) => b[0] - a[0]).map(x => x[1]);

  for (let ri = 0; ri < POP_SIZE; ri++) {
    const i = order[ri];
    const individual = population[i];
    const f = fitnesses[i];
    const iy = GRID_Y + (ri + 2) * (CELL_H + 0);

    for (let j = 0; j < BIT_LENGTH; j++) {
      const x = GRID_X + j * CELL_W;
      const match = individual[j] === TARGET[j];
      if (individual[j] === 1) {
        ctx.fillStyle = match ? AMBER : '#aa3333';
      } else {
        ctx.fillStyle = match ? '#1e2e1e' : '#2a1515';
      }
      ctx.fillRect(x, iy, CELL_W - 1, CELL_H - 1);
    }

    // Fitness bar on right
    const fbx = GRID_X + BIT_LENGTH * CELL_W + 4;
    const fbw = Math.floor(f * 40);
    ctx.fillStyle = i === bestIdx ? AMBER : '#334433';
    ctx.fillRect(fbx, iy, fbw, CELL_H - 1);
  }

  // Fitness graph
  if (bestFitnessHistory.length > 1) {
    ctx.fillStyle = '#111';
    ctx.fillRect(GRID_X, GRAPH_Y, W - GRID_X - 30, GRAPH_H);

    const nH = bestFitnessHistory.length;

    // Avg fitness line
    ctx.strokeStyle = '#4a7a4a';
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (let i = 0; i < avgFitnessHistory.length; i++) {
      const x = GRID_X + (i / Math.max(nH - 1, 1)) * (W - GRID_X - 30);
      const y = GRAPH_Y + GRAPH_H - avgFitnessHistory[i] * GRAPH_H;
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Best fitness line
    ctx.strokeStyle = AMBER;
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (let i = 0; i < nH; i++) {
      const x = GRID_X + (i / Math.max(nH - 1, 1)) * (W - GRID_X - 30);
      const y = GRAPH_Y + GRAPH_H - bestFitnessHistory[i] * GRAPH_H;
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();

    ctx.fillStyle = AMBER;
    ctx.font = '11px monospace';
    ctx.fillText(`best: ${(bestF * 100).toFixed(1)}%`, GRID_X + 4, GRAPH_Y + 14);
    ctx.fillStyle = '#4a7a4a';
    ctx.fillText(`avg: ${(avgFitnessHistory[avgFitnessHistory.length - 1] * 100).toFixed(1)}%`, GRID_X + 80, GRAPH_Y + 14);

    ctx.fillStyle = DIMTEXT;
    ctx.font = '10px monospace';
    ctx.fillText('fitness', GRID_X - 48, GRAPH_Y + GRAPH_H / 2);
    ctx.fillText('gen', GRID_X + (W - GRID_X - 30) / 2, GRAPH_Y + GRAPH_H + 14);
  }
}

function step() {
  if (!running) return;

  if (generation === 0) {
    population = Array.from({length: POP_SIZE}, randomIndividual);
  } else {
    population = nextGeneration(population);
  }

  const fitnesses = population.map(fitness);
  const bestF = Math.max(...fitnesses);
  const avgF = fitnesses.reduce((a, b) => a + b, 0) / fitnesses.length;
  bestFitnessHistory.push(bestF);
  avgFitnessHistory.push(avgF);

  generation++;
  draw();
  window.__setStatus && window.__setStatus(`generation ${generation} — best fitness: ${(bestF * 100).toFixed(1)}% — click to restart`);

  if (bestF >= 1.0) {
    window.__setStatus && window.__setStatus(`converged at generation ${generation} — 100% fitness — click to restart`);
    return;
  }
  if (generation >= 500) {
    window.__setStatus && window.__setStatus(`generation 500 — best ${(bestF * 100).toFixed(1)}% — click to restart`);
    return;
  }

  const delay = generation < 20 ? 200 : generation < 100 ? 80 : 30;
  phaseTimeout = setTimeout(step, delay);
}

function init() {
  running = true;
  cancelAnimationFrame(animId);
  if (phaseTimeout) clearTimeout(phaseTimeout);
  population = [];
  generation = 0;
  bestFitnessHistory = [];
  avgFitnessHistory = [];
  draw();
  window.__setStatus && window.__setStatus('generation 0 — initializing — click to restart');
  phaseTimeout = setTimeout(step, 100);
}

window.__programRestart = init;
init();
