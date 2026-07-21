# Minesweeper

![Python](https://img.shields.io/badge/Python-3.12.2-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-Markup-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-Styling-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Dev%20DB-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
![WhiteNoise](https://img.shields.io/badge/WhiteNoise-Static%20Files-444444?style=for-the-badge)
![Render](https://img.shields.io/badge/Render-Blueprint-46E3B7?style=for-the-badge&logo=render&logoColor=black)
![MIT License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

Videojuego web del **Buscaminas** construido con **Python + Django** y un frontend en **JavaScript, HTML y CSS**. El proyecto está pensado como aplicación de portfolio: es responsive, funciona con estado de partida en sesión y está preparado para desplegarse en Render.

## Estado actual

El proyecto está **funcional, probado y desplegable**.

- Aplicación Django con una vista principal renderizada desde template y una API JSON para crear partidas, revelar celdas y alternar banderas.
- Motor propio de Buscaminas separado del frontend, con serialización/deserialización del estado para persistirlo en la sesión.
- Gameplay completo: primer click protegido, revelado expansivo de zonas vacías, banderas, conteo de minas cercanas, condición de victoria/derrota y apertura por doble click sobre números revelados.
- Estado de juego guardado por sesión. Por defecto se usan sesiones firmadas en cookies para no depender de una base de datos durante la partida en despliegues cloud.
- Interfaz responsive en escala de grises con tema oscuro/claro, tablero adaptable al viewport y soporte para mouse, teclado y pantallas táctiles.
- Indicadores de partida: minas totales, banderas, minas restantes, progreso, cronómetro, estado actual y mejor tiempo por dificultad guardado en `localStorage`.
- Pista local tipo “IA” basada en reglas simples: prioriza movimientos seguros cuando las banderas alrededor de un número coinciden con su conteo y, si no hay deducción, propone una celda oculta como fallback.
- Configuración productiva con Gunicorn, WhiteNoise, `collectstatic`, variables de entorno, `Procfile` y Blueprint de Render.
- Pruebas unitarias Django para reglas clave del motor: protección del primer click, chord reveal y payload público al perder.

## Stack tecnológico

| Capa | Tecnología |
| --- | --- |
| Backend | Python 3.12.2, Django 5.x |
| Frontend | JavaScript ES6+, HTML5, CSS3 |
| Persistencia | Sesiones Django; SQLite para desarrollo/migraciones estándar |
| Static files | WhiteNoise |
| Servidor WSGI | Gunicorn |
| Deploy | Render Blueprint (`render.yaml`) y `Procfile` |
| Configuración | Variables de entorno con `python-dotenv` |
| Tests | Django `TestCase` |

## Funcionalidades disponibles

### Dificultades

| Dificultad | Tablero | Minas |
| --- | ---: | ---: |
| Inexperto | 8×8 | 8 |
| Normal | 9×9 | 10 |
| Complejo | 16×16 | 40 |
| Difícil | 16×30 | 99 |
| Pesadilla | 18×30 | 120 |

### Controles

- **Click / tap:** revelar celda.
- **Click derecho:** colocar o quitar bandera.
- **Toque largo en mobile:** colocar o quitar bandera.
- **Doble click sobre un número revelado:** abrir celdas vecinas cuando las banderas alrededor coinciden con el número.
- **H:** pedir pista.
- **N:** iniciar nueva partida.
- **P:** pausar o reanudar.
- **T:** alternar tema.

### Interfaz

- Diseño responsive para mobile, tablet, laptop y desktop.
- Ajuste dinámico del tamaño de celda según el viewport.
- Pausa con overlay visual y bloqueo de interacción.
- Tema claro/oscuro persistido en `localStorage`.
- Accesibilidad básica con `role="grid"`, `role="gridcell"` y etiquetas ARIA por celda.
- Mensajes de estado y manejo de errores/timeout al comunicarse con la API.

## API interna

La API está pensada para el cliente web incluido en el proyecto. Todos los endpoints son `POST` y devuelven JSON.

| Endpoint | Descripción | Payload |
| --- | --- | --- |
| `/api/new` | Crea una nueva partida en sesión. | `{ "difficulty": "complejo" }` |
| `/api/reveal` | Revela una celda o ejecuta chord reveal si la celda ya estaba revelada. | `{ "r": 0, "c": 0 }` |
| `/api/toggle-flag` | Alterna bandera en una celda oculta. | `{ "r": 0, "c": 0 }` |

La respuesta exitosa tiene la forma general:

```json
{
  "ok": true,
  "state": {
    "rows": 16,
    "cols": 16,
    "mines": 40,
    "revealedCount": 0,
    "flaggedCount": 0,
    "remainingMines": 40,
    "over": false,
    "win": false,
    "grid": []
  }
}
```

## Requisitos

- Python 3.12+
- pip

## Instalación local

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abrí la aplicación en: <http://127.0.0.1:8000>

## Tests

```bash
python manage.py test
```

## Variables de entorno

La configuración se lee desde variables de entorno y, en local, puede cargarse desde un archivo `.env`.

| Variable | Uso | Valor por defecto |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Secret key de Django. | Valor inseguro solo para desarrollo |
| `DJANGO_DEBUG` | Activa debug con `1`. | `0` |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos separados por coma. | `localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Orígenes CSRF confiables separados por coma. | vacío |
| `DJANGO_SESSION_ENGINE` | Backend de sesiones. | `django.contrib.sessions.backends.signed_cookies` |
| `DJANGO_USE_MANIFEST_STATICFILES` | Usa manifest de estáticos con `1`. | `0` |
| `DJANGO_SESSION_COOKIE_SECURE` | Cookie de sesión segura con `1`. | `0` |
| `DJANGO_CSRF_COOKIE_SECURE` | Cookie CSRF segura con `1`. | `0` |

En Render, la app también usa `RENDER_EXTERNAL_HOSTNAME` para agregar automáticamente el host público a `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS`. Además, cuando `DJANGO_DEBUG=0`, se aceptan hosts y orígenes `*.onrender.com` como valor seguro por defecto para evitar errores de host inválido en despliegues estándar de Render.

## Deploy en Render

El repositorio incluye `render.yaml` listo para usar como Blueprint.

1. Subí este repo a GitHub.
2. En Render, creá un servicio desde **New → Blueprint** y conectá el repositorio.
3. Render ejecuta el build definido:
   - instala dependencias con `pip install -r requirements.txt`;
   - ejecuta `python manage.py collectstatic --noinput`;
   - ejecuta `python manage.py migrate`;
   - inicia con `gunicorn minesweeper_portfolio.wsgi:application`.

> En producción, configurá `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS` y `DJANGO_CSRF_TRUSTED_ORIGINS` según el dominio final.

## Estructura principal

```text
.
├── game/
│   ├── minesweeper.py      # Motor del juego, reglas y serialización del estado
│   ├── tests.py            # Pruebas unitarias de reglas principales
│   ├── urls.py             # Rutas API del juego
│   └── views.py            # Vista principal y endpoints JSON
├── minesweeper_portfolio/
│   ├── settings.py         # Configuración de Django, sesiones, estáticos y seguridad
│   ├── urls.py             # URLs raíz
│   └── wsgi.py             # WSGI para Gunicorn
├── static/
│   ├── css/styles.css      # Interfaz responsive, temas y estados visuales
│   ├── js/app.js           # Cliente del juego e interacción con la API
│   └── favicon.svg
├── templates/game/index.html
├── render.yaml             # Blueprint de Render
├── Procfile                # Comando web para plataformas Procfile-compatible
├── requirements.txt
├── runtime.txt
└── manage.py
```

## Licencia

Este proyecto está publicado bajo licencia MIT. Consultá el archivo [`LICENSE`](LICENSE) para más información.
