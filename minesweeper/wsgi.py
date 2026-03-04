"""Compatibility WSGI module.

Allows deployments configured with `gunicorn minesweeper.wsgi:application`
to continue working after project package was renamed.
"""

from minesweeper_portfolio.wsgi import application
