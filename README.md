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

Videojuego web del **Buscaminas** hecho con **Python + Django**, con frontend en **JavaScript, HTML y CSS** y una interfaz responsive en escala de grises con tema claro/oscuro.

## Estado actual

El proyecto se encuentra en estado **funcional y desplegable** como aplicación web de portfolio:

- Backend Django con endpoints JSON para crear partida, revelar celdas y alternar banderas.
- Estado de partida guardado en sesión; por defecto usa sesiones firmadas en cookies para evitar depender de base de datos durante el gameplay en deploys cloud.
- Lógica propia de Buscaminas con protección del primer click, expansión automática de zonas vacías, banderas, detección de victoria/derrota y apertura por doble click/chord sobre números revelados.
- Frontend responsive con tablero adaptable al viewport, contador de minas/banderas/restantes, progreso, cronómetro, récord por dificultad en `localStorage`, pausa, tema claro/oscuro y accesos rápidos por teclado.
- Pista IA local basada en reglas simples: busca movimientos seguros cuando las banderas alrededor de un número coinciden con su conteo; si no encuentra, sugiere una celda oculta como fallback.
- Configuración lista para producción con Gunicorn, WhiteNoise, `collectstatic`, variables de entorno y Blueprint de Render.
- Cobertura de pruebas unitarias para reglas clave del motor: primer click seguro, chord reveal y payload público tras derrota.

## Stack tecnológico

| Capa | Tecnología |
| --- | --- |
| Backend | Python 3.12.2, Django 5.x |
| Frontend | JavaScript ES6+, HTML5, CSS3 |
| Persistencia | Sesión Django; SQLite para base de datos de desarrollo/migraciones estándar |
| Static files | WhiteNoise |
| Servidor WSGI | Gunicorn |
| Deploy | Render Blueprint (`render.yaml`) / Procfile |
| Configuración | Variables de entorno con `python-dotenv` |
| Tests | Django TestCase |

## Funcionalidades

- Dificultades disponibles:
  - **Inexperto**: 8×8 con 8 minas.
  - **Normal**: 9×9 con 10 minas.
  - **Complejo**: 16×16 con 40 minas.
  - **Difícil**: 16×30 con 99 minas.
  - **Pesadilla**: 18×30 con 120 minas.
- Controles:
  - Click izquierdo: revelar celda.
  - Click derecho: colocar o quitar bandera.
  - Doble click sobre un número revelado: abrir las celdas vecinas cuando las banderas coinciden con el número.
  - Tecla `H`: pedir pista.
  - Tecla `N`: nueva partida.
  - Tecla `P`: pausar o reanudar.
  - Tecla `T`: alternar tema.
- UI responsive para mobile, tablet, laptop y desktop.
- Temporizador con guardado del mejor tiempo por dificultad.
- Revelado de minas al perder y actualización de progreso durante la partida.

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

La configuración se lee desde variables de entorno y, en local, puede cargarse desde un archivo `.env`:

| Variable | Uso | Valor por defecto |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Secret key de Django | Valor inseguro solo para desarrollo |
| `DJANGO_DEBUG` | Activa debug con `1` | `0` |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos separados por coma | `localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Orígenes CSRF confiables separados por coma | vacío |
| `DJANGO_SESSION_ENGINE` | Backend de sesiones | `django.contrib.sessions.backends.signed_cookies` |
| `DJANGO_USE_MANIFEST_STATICFILES` | Usa manifest de estáticos con `1` | `0` |
| `DJANGO_SESSION_COOKIE_SECURE` | Cookie de sesión segura con `1` | `0` |
| `DJANGO_CSRF_COOKIE_SECURE` | Cookie CSRF segura con `1` | `0` |

En Render, la app también toma `RENDER_EXTERNAL_HOSTNAME` para agregar automáticamente el host público a `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS`.

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
│   ├── minesweeper.py      # Motor del juego y serialización del estado
│   ├── tests.py            # Pruebas unitarias de reglas principales
│   ├── urls.py             # Rutas API del juego
│   └── views.py            # Vistas Django y endpoints JSON
├── minesweeper_portfolio/
│   ├── settings.py         # Configuración de Django, sesiones, estáticos y seguridad
│   ├── urls.py             # URLs raíz
│   └── wsgi.py             # WSGI para Gunicorn
├── static/
│   ├── css/styles.css      # Interfaz responsive y temas
│   ├── js/app.js           # Cliente del juego e interacción con API
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
