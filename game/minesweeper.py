from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Set
import random

Coord = Tuple[int, int]

@dataclass
class GameState:
    rows: int
    cols: int
    mines: int
    mines_set: Set[Coord]
    revealed: Set[Coord]
    flagged: Set[Coord]
    counts: List[List[int]]
    over: bool = False
    win: bool = False

def _neighbors(r: int, c: int, rows: int, cols: int):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                yield nr, nc

def new_game(rows: int, cols: int, mines: int, seed: int | None = None) -> GameState:
    if rows <= 0 or cols <= 0:
        raise ValueError("rows/cols must be positive")
    max_mines = rows * cols - 1
    mines = max(1, min(mines, max_mines))

    rng = random.Random(seed)
    all_cells = [(r, c) for r in range(rows) for c in range(cols)]
    mines_set = set(rng.sample(all_cells, mines))

    counts = [[0 for _ in range(cols)] for _ in range(rows)]
    for (r, c) in mines_set:
        for nr, nc in _neighbors(r, c, rows, cols):
            counts[nr][nc] += 1

    return GameState(
        rows=rows,
        cols=cols,
        mines=mines,
        mines_set=mines_set,
        revealed=set(),
        flagged=set(),
        counts=counts,
        over=False,
        win=False,
    )

def reveal(state: GameState, r: int, c: int) -> None:
    if state.over:
        return
    if (r, c) in state.flagged:
        return
    if not (0 <= r < state.rows and 0 <= c < state.cols):
        return

    if (r, c) in state.mines_set:
        state.revealed.add((r, c))
        state.over = True
        state.win = False
        return

    # flood fill for zeros
    stack = [(r, c)]
    visited = set()
    while stack:
        cr, cc = stack.pop()
        if (cr, cc) in visited:
            continue
        visited.add((cr, cc))

        if (cr, cc) in state.flagged:
            continue

        state.revealed.add((cr, cc))
        if state.counts[cr][cc] == 0:
            for nr, nc in _neighbors(cr, cc, state.rows, state.cols):
                if (nr, nc) not in state.revealed and (nr, nc) not in state.mines_set:
                    stack.append((nr, nc))

    _check_win(state)

def toggle_flag(state: GameState, r: int, c: int) -> None:
    if state.over:
        return
    if not (0 <= r < state.rows and 0 <= c < state.cols):
        return
    if (r, c) in state.revealed:
        return
    if (r, c) in state.flagged:
        state.flagged.remove((r, c))
    else:
        state.flagged.add((r, c))
    _check_win(state)

def _check_win(state: GameState) -> None:
    if state.over:
        return
    total_safe = state.rows * state.cols - state.mines
    if len(state.revealed) >= total_safe:
        state.over = True
        state.win = True

def to_public_payload(state: GameState) -> dict:
    # What the frontend needs to render
    grid = []
    for r in range(state.rows):
        row = []
        for c in range(state.cols):
            cell = {"r": r, "c": c}
            coord = (r, c)
            if coord in state.revealed:
                cell["revealed"] = True
                cell["mine"] = coord in state.mines_set
                cell["count"] = state.counts[r][c]
            else:
                cell["revealed"] = False
                cell["flagged"] = coord in state.flagged
            row.append(cell)
        grid.append(row)

    return {
        "rows": state.rows,
        "cols": state.cols,
        "mines": state.mines,
        "revealedCount": len(state.revealed),
        "flaggedCount": len(state.flagged),
        "over": state.over,
        "win": state.win,
        "grid": grid,
    }

def serialize(state: GameState) -> dict:
    return {
        "rows": state.rows,
        "cols": state.cols,
        "mines": state.mines,
        "mines_set": list(map(list, state.mines_set)),
        "revealed": list(map(list, state.revealed)),
        "flagged": list(map(list, state.flagged)),
        "counts": state.counts,
        "over": state.over,
        "win": state.win,
    }

def deserialize(data: dict) -> GameState:
    return GameState(
        rows=int(data["rows"]),
        cols=int(data["cols"]),
        mines=int(data["mines"]),
        mines_set=set(tuple(x) for x in data.get("mines_set", [])),
        revealed=set(tuple(x) for x in data.get("revealed", [])),
        flagged=set(tuple(x) for x in data.get("flagged", [])),
        counts=data.get("counts") or [],
        over=bool(data.get("over", False)),
        win=bool(data.get("win", False)),
    )
