# simple wsgi entrypoint for deploying with gunicorn
from .core import db, server

db.create_all()
application = server
