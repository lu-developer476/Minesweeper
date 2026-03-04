from __future__ import annotations

import json
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

from .minesweeper import new_game, reveal, toggle_flag, serialize, deserialize, to_public_payload

SESSION_KEY = "minesweeper_state_v1"

@ensure_csrf_cookie
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "game/index.html")

def _get_state(request: HttpRequest):
    raw = request.session.get(SESSION_KEY)
    if not raw:
        return None
    try:
        return deserialize(raw)
    except Exception:
        return None

def _set_state(request: HttpRequest, state) -> None:
    request.session[SESSION_KEY] = serialize(state)
    request.session.modified = True

@require_POST
def api_new_game(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        payload = {}

    difficulty = (payload.get("difficulty") or "medium").lower()
    # Classic-ish presets
    presets = {
        "easy":   {"rows": 9,  "cols": 9,  "mines": 10},
        "medium": {"rows": 16, "cols": 16, "mines": 40},
        "hard":   {"rows": 16, "cols": 30, "mines": 99},
    }
    cfg = presets.get(difficulty, presets["medium"])

    state = new_game(**cfg)
    _set_state(request, state)
    return JsonResponse({"ok": True, "state": to_public_payload(state)})

@require_POST
def api_reveal(request: HttpRequest) -> JsonResponse:
    state = _get_state(request)
    if not state:
        return JsonResponse({"ok": False, "error": "No game in session. Start a new game."}, status=400)

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
        r = int(payload.get("r"))
        c = int(payload.get("c"))
    except Exception:
        return JsonResponse({"ok": False, "error": "Invalid payload."}, status=400)

    reveal(state, r, c)
    _set_state(request, state)
    return JsonResponse({"ok": True, "state": to_public_payload(state)})

@require_POST
def api_toggle_flag(request: HttpRequest) -> JsonResponse:
    state = _get_state(request)
    if not state:
        return JsonResponse({"ok": False, "error": "No game in session. Start a new game."}, status=400)

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
        r = int(payload.get("r"))
        c = int(payload.get("c"))
    except Exception:
        return JsonResponse({"ok": False, "error": "Invalid payload."}, status=400)

    toggle_flag(state, r, c)
    _set_state(request, state)
    return JsonResponse({"ok": True, "state": to_public_payload(state)})
