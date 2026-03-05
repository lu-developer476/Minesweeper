# Minesweeper

Videojuego web del **Buscaminas** hecho con **Python + Django** con UI en **escala de grises**.

- Backend: Django + sesión (estado de partida) + API JSON.
- Frontend: grid interactivo (click = revelar, click derecho = bandera).
- Producción: Gunicorn + WhiteNoise (static) listo para deploy.

## Requisitos
- Python 3.12+
- pip

## Instalación (local)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
# source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abrí: http://127.0.0.1:8000

## Deploy (Render recomendado)
Incluye `render.yaml` listo.

1. Subí este repo a GitHub.
2. En Render → **New** → **Blueprint** → conectá el repo.
3. Deploy. Render ejecuta:
   - install deps
   - `collectstatic`
   - `migrate`
   - `gunicorn ...`

> Nota: en producción se usan variables de entorno (SECRET_KEY, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS).

## Estructura
- `game/minesweeper.py`: lógica (crear partida, revelar, banderas, win/lose).
- `game/views.py`: endpoints JSON + render del template.
- `templates/game/index.html`: UI.
- `static/`: CSS/JS.

## Licencia
MIT (usala sin miedo).
