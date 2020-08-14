# simple wsgi entrypoint for deploying with gunicorn
from .core import server

application = server
