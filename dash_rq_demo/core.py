import os

import dash
import dash_bootstrap_components as dbc
import flask
import redis
from flask_sqlalchemy import SQLAlchemy
from rq import Queue

server = flask.Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://localhost/dash-rq-demo"
)
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(server)

app = dash.Dash(
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    serve_locally=False,
)

redis_url = os.getenv("REDISTOGO_URL", "redis://localhost:6379")
conn = redis.from_url(redis_url)
queue = Queue(connection=conn)
