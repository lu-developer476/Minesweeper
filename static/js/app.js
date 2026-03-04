const boardEl = document.getElementById("board");
const minesEl = document.getElementById("mines");
const flagsEl = document.getElementById("flags");
const statusEl = document.getElementById("status");
const difficultyEl = document.getElementById("difficulty");
const btnNew = document.getElementById("btnNew");

let currentState = null;

function setStatus(text){
  statusEl.textContent = text;
}

async function apiPost(url, data){
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": CSRF_TOKEN,
    },
    body: JSON.stringify(data ?? {}),
  });
  const json = await res.json().catch(() => ({}));
  if(!res.ok){
    const msg = json?.error || `Error ${res.status}`;
    throw new Error(msg);
  }
  return json;
}

function render(state){
  currentState = state;
  minesEl.textContent = state.mines;
  flagsEl.textContent = state.flaggedCount;
  if(state.over){
    setStatus(state.win ? "Ganaste 🏁" : "Boom 💥");
  }else{
    setStatus("En juego");
  }

  boardEl.style.gridTemplateColumns = `repeat(${state.cols}, 30px)`;

  boardEl.innerHTML = "";
  for(const row of state.grid){
    for(const cell of row){
      const el = document.createElement("div");
      el.className = "cell";
      el.setAttribute("role", "gridcell");
      el.dataset.r = cell.r;
      el.dataset.c = cell.c;

      if(cell.revealed){
        el.classList.add("revealed");
        if(cell.mine){
          el.classList.add("mine");
          el.innerHTML = '<span class="tiny">✹</span>';
        }else{
          el.textContent = cell.count ? String(cell.count) : "";
        }
      }else{
        if(cell.flagged){
          el.classList.add("flagged");
          el.innerHTML = '<span class="tiny">⚑</span>';
        }
      }

      // Left click reveal
      el.addEventListener("click", async (ev) => {
        ev.preventDefault();
        if(currentState?.over) return;
        await onReveal(cell.r, cell.c);
      });

      // Right click flag
      el.addEventListener("contextmenu", async (ev) => {
        ev.preventDefault();
        if(currentState?.over) return;
        await onToggleFlag(cell.r, cell.c);
      });

      boardEl.appendChild(el);
    }
  }
}

async function newGame(){
  setStatus("Creando partida…");
  const difficulty = difficultyEl.value;
  const json = await apiPost("/api/new", { difficulty });
  render(json.state);
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

btnNew.addEventListener("click", () => newGame());

// Start immediately
newGame().catch(err => setStatus(err.message));
