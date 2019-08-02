import os

import dash
import dash_bootstrap_components as dbc
import flask
import redis
from flask_sqlalchemy import SQLAlchemy
from rq import Queue
from sqlalchemy.dialects.postgresql import UUID

server = flask.Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://localhost/mydb"
)
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(server)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(UUID(as_uuid=True))
    queued = db.Column(db.DateTime)
    started = db.Column(db.DateTime)
    completed = db.Column(db.DateTime)
    result = db.Column(db.Integer)

    def __repr__(self):
        return "<Result %r>" % self.result


app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

redis_url = os.getenv("REDISTOGO_URL", "redis://localhost:6379")
conn = redis.from_url(redis_url)
queue = Queue(connection=conn)
