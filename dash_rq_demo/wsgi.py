from .core import db, server

db.create_all()
application = server
