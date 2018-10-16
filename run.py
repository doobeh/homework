# Used as an inpoint for a Gunicorn service.

from homework.core import create_app

app = create_app()
