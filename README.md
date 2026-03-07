# Minesweeper

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-Markup-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-Styling-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
![WhiteNoise](https://img.shields.io/badge/WhiteNoise-Static%20Files-444444?style=for-the-badge)
![Render](https://img.shields.io/badge/Render-Deploy-46E3B7?style=for-the-badge&logo=render&logoColor=black)
![MIT License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

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
