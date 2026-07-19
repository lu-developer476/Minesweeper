const boardEl = document.getElementById("board");
const minesEl = document.getElementById("mines");
const flagsEl = document.getElementById("flags");
const remainingEl = document.getElementById("remaining");
const progressEl = document.getElementById("progress");
const statusEl = document.getElementById("status");
const timerEl = document.getElementById("timer");
const bestEl = document.getElementById("best");
const difficultyEl = document.getElementById("difficulty");
const btnNew = document.getElementById("btnNew");
const btnHint = document.getElementById("btnHint");
const btnPause = document.getElementById("btnPause");
const btnTheme = document.getElementById("btnTheme");

let currentState = null;
let timer = null;
let elapsedSeconds = 0;
let hintCell = null;
let loadingGame = false;
let paused = false;

function setStatus(text){
  statusEl.textContent = text;
}

function formatTime(seconds){
  const mm = String(Math.floor(seconds / 60)).padStart(2, "0");
  const ss = String(seconds % 60).padStart(2, "0");
  return `${mm}:${ss}`;
}

function bestKey(){
  return `best_time_${difficultyEl.value}`;
}

function renderBestTime(){
  const best = Number(localStorage.getItem(bestKey()) || 0);
  bestEl.textContent = best ? formatTime(best) : "—";
}

function startTimer(){
  clearInterval(timer);
  timer = setInterval(() => {
    if(paused) return;
    elapsedSeconds += 1;
    timerEl.textContent = formatTime(elapsedSeconds);
  }, 1000);
}

function stopTimerAndPersistIfNeeded(){
  clearInterval(timer);
  if(currentState?.win){
    const key = bestKey();
    const currentBest = Number(localStorage.getItem(key) || 0);
    if(!currentBest || elapsedSeconds < currentBest){
      localStorage.setItem(key, String(elapsedSeconds));
      renderBestTime();
    }
  }
}

function fitBoardToViewport(state){
  const wrapper = boardEl.parentElement;
  const wrapperRect = wrapper?.getBoundingClientRect();
  const horizontalBudget = Math.max(260, Math.floor(wrapperRect?.width || window.innerWidth - 34));
  const verticalBudget = Math.max(220, Math.floor(wrapperRect?.height || window.innerHeight - 255));
  const gap = window.innerWidth <= 420 ? 3 : 4;
  const boardPadding = 14;
  const maxByWidth = Math.floor((horizontalBudget - boardPadding - (state.cols - 1) * gap) / state.cols);
  const maxByHeight = Math.floor((verticalBudget - boardPadding - (state.rows - 1) * gap) / state.rows);
  const desktopCap = window.innerWidth >= 1200 ? 32 : 30;
  const ideal = Math.min(desktopCap, maxByWidth, maxByHeight);
  const cellSize = Math.max(window.innerWidth <= 420 ? 13 : 14, ideal);
  document.documentElement.style.setProperty("--cell-size", `${cellSize}px`);
  document.documentElement.style.setProperty("--cell-gap", `${gap}px`);
}

async function apiPost(url, data){
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 12000);
  try{
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": CSRF_TOKEN,
      },
      body: JSON.stringify(data ?? {}),
      signal: controller.signal,
    });
    const json = await res.json().catch(() => ({}));
    if(!res.ok) throw new Error(json?.error || `Error ${res.status}`);
    return json;
  }catch(err){
    if(err?.name === "AbortError"){
      throw new Error("Tiempo de espera agotado. Reintentá en unos segundos.");
    }
    throw err;
  }finally{
    clearTimeout(timeoutId);
  }
}

function setLoadingUi(isLoading){
  loadingGame = isLoading;
  btnNew.disabled = isLoading;
  difficultyEl.disabled = isLoading;
  btnHint.disabled = isLoading;
  btnPause.disabled = isLoading;
}

function neighbors(r, c, rows, cols){
  const out = [];
  for(let dr = -1; dr <= 1; dr += 1){
    for(let dc = -1; dc <= 1; dc += 1){
      if(dr === 0 && dc === 0) continue;
      const nr = r + dr;
      const nc = c + dc;
      if(nr >= 0 && nr < rows && nc >= 0 && nc < cols) out.push([nr, nc]);
    }
  }
  return out;
}

function getAiHint(state){
  const safeMoves = [];
  const grid = state.grid;
  for(const row of grid){
    for(const cell of row){
      if(!cell.revealed || !cell.count) continue;
      const around = neighbors(cell.r, cell.c, state.rows, state.cols);
      const hidden = [];
      let flagged = 0;
      for(const [nr, nc] of around){
        const n = grid[nr][nc];
        if(n.flagged) flagged += 1;
        if(!n.revealed && !n.flagged) hidden.push(n);
      }
      if(hidden.length && flagged === cell.count) safeMoves.push(...hidden);
    }
  }
  if(safeMoves.length) return safeMoves[Math.floor(Math.random() * safeMoves.length)];

  const fallback = [];
  for(const row of grid){
    for(const cell of row){
      if(!cell.revealed && !cell.flagged) fallback.push(cell);
    }
  }
  return fallback.length ? fallback[Math.floor(Math.random() * fallback.length)] : null;
}

function render(state){
  currentState = state;
  minesEl.textContent = state.mines;
  flagsEl.textContent = state.flaggedCount;
  remainingEl.textContent = state.remainingMines ?? Math.max(0, state.mines - state.flaggedCount);
  const safeCells = state.rows * state.cols - state.mines;
  const progress = safeCells ? Math.round((state.revealedCount / safeCells) * 100) : 0;
  progressEl.textContent = `${progress}%`;
  boardEl.classList.toggle("paused", paused);

  if(state.over){
    setStatus(state.win ? "Ganaste 🏁" : "Boom 💥");
    stopTimerAndPersistIfNeeded();
  }else if(paused){
    setStatus("Pausa activa");
  }else{
    setStatus("En juego");
  }

  fitBoardToViewport(state);
  boardEl.style.gridTemplateColumns = `repeat(${state.cols}, var(--cell-size))`;

  boardEl.innerHTML = "";
  for(const row of state.grid){
    for(const cell of row){
      const el = document.createElement("div");
      el.className = "cell";
      el.setAttribute("role", "gridcell");
      el.setAttribute("aria-label", describeCell(cell));
      el.dataset.r = String(cell.r);
      el.dataset.c = String(cell.c);

      if(hintCell && cell.r === hintCell.r && cell.c === hintCell.c) el.classList.add("hint-cell");

      if(cell.revealed){
        el.classList.add("revealed");
        if(cell.mine){
          el.classList.add("mine");
          el.innerHTML = '<span class="tiny">✹</span>';
        }else{
          el.textContent = cell.count ? String(cell.count) : "";
        }
      }else if(cell.flagged){
        el.classList.add("flagged");
        el.innerHTML = '<span class="tiny">⚑</span>';
      }

      let suppressNextClick = false;
      el.addEventListener("click", async (ev) => {
        ev.preventDefault();
        if(suppressNextClick){
          suppressNextClick = false;
          return;
        }
        if(currentState?.over || paused) return;
        hintCell = null;
        await onReveal(cell.r, cell.c);
      });

      el.addEventListener("contextmenu", async (ev) => {
        ev.preventDefault();
        if(currentState?.over || paused) return;
        hintCell = null;
        await onToggleFlag(cell.r, cell.c);
      });

      let longPressTimer = null;
      el.addEventListener("pointerdown", (ev) => {
        if(ev.pointerType === "mouse" || currentState?.over || paused) return;
        longPressTimer = setTimeout(async () => {
          hintCell = null;
          suppressNextClick = true;
          await onToggleFlag(cell.r, cell.c);
          longPressTimer = null;
        }, 520);
      });
      el.addEventListener("pointerup", () => clearTimeout(longPressTimer));
      el.addEventListener("pointercancel", () => clearTimeout(longPressTimer));
      el.addEventListener("pointerleave", () => clearTimeout(longPressTimer));

      el.addEventListener("dblclick", async (ev) => {
        ev.preventDefault();
        if(currentState?.over || paused || !cell.revealed || cell.mine) return;
        hintCell = null;
        await onReveal(cell.r, cell.c);
      });

      boardEl.appendChild(el);
    }
  }
}

async function newGame(){
  if(loadingGame) return;
  setStatus("Creando partida…");
  setLoadingUi(true);
  elapsedSeconds = 0;
  timerEl.textContent = "00:00";
  clearInterval(timer);
  hintCell = null;
  paused = false;
  btnPause.textContent = "Pausar";
  renderBestTime();
  try{
    const json = await apiPost("/api/new", { difficulty: difficultyEl.value });
    render(json.state);
    startTimer();
  }catch(err){
    setStatus(`No se pudo iniciar: ${err.message}`);
  }finally{
    setLoadingUi(false);
  }
}

async function onReveal(r, c){
  try{
    const json = await apiPost("/api/reveal", { r, c });
    render(json.state);
  }catch(err){
    setStatus(err.message);
  }
}

async function onToggleFlag(r, c){
  try{
    const json = await apiPost("/api/toggle-flag", { r, c });
    render(json.state);
  }catch(err){
    setStatus(err.message);
  }
}

function toggleTheme(){
  const next = document.body.dataset.theme === "light" ? "dark" : "light";
  document.body.dataset.theme = next;
  localStorage.setItem("theme", next);
}

function describeCell(cell){
  const row = cell.r + 1;
  const col = cell.c + 1;
  if(cell.revealed && cell.mine) return `Mina en fila ${row}, columna ${col}`;
  if(cell.revealed) return cell.count ? `Celda revelada con ${cell.count} minas cerca en fila ${row}, columna ${col}` : `Celda vacía revelada en fila ${row}, columna ${col}`;
  if(cell.flagged) return `Bandera en fila ${row}, columna ${col}`;
  return `Celda oculta en fila ${row}, columna ${col}`;
}

function togglePause(){
  if(!currentState || currentState.over) return;
  paused = !paused;
  btnPause.textContent = paused ? "Reanudar" : "Pausar";
  setStatus(paused ? "Pausa activa" : "En juego");
  render(currentState);
}

function askHint(){
  if(paused){
    setStatus("Reanudá la partida para pedir una pista.");
    return;
  }
  if(!currentState){
    setStatus("La pista IA necesita una partida activa.");
    return;
  }
  if(currentState.over){
    setStatus("La partida terminó. Iniciá una nueva para usar Pista IA.");
    return;
  }
  hintCell = getAiHint(currentState);
  if(hintCell){
    setStatus(`Pista IA: probá en fila ${hintCell.r + 1}, columna ${hintCell.c + 1}`);
    render(currentState);
  }
}

btnNew.addEventListener("click", () => { newGame().catch((err) => setStatus(err.message)); });
btnHint.addEventListener("click", () => askHint());
btnPause.addEventListener("click", () => togglePause());
btnTheme.addEventListener("click", () => toggleTheme());
difficultyEl.addEventListener("change", () => { newGame().catch((err) => setStatus(err.message)); });

window.addEventListener("resize", () => {
  if(currentState) fitBoardToViewport(currentState);
});

window.addEventListener("keydown", (ev) => {
  if(ev.key.toLowerCase() === "h") askHint();
  if(ev.key.toLowerCase() === "n") newGame().catch((err) => setStatus(err.message));
  if(ev.key.toLowerCase() === "p") togglePause();
  if(ev.key.toLowerCase() === "t") toggleTheme();
});

const savedTheme = localStorage.getItem("theme");
if(savedTheme) document.body.dataset.theme = savedTheme;
renderBestTime();
newGame().catch((err) => setStatus(err.message));
