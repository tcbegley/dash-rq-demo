import os

import dash
import dash_bootstrap_components as dbc
import flask
import redis
from rq import Queue

server = flask.Flask(__name__)

app = dash.Dash(
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    serve_locally=False,
)

# redis connection and RQ queue. use redistogo service when dpeloying to Heroku
redis_url = os.getenv("REDISTOGO_URL", "redis://localhost:6379")
conn = redis.from_url(redis_url)
queue = Queue(connection=conn)
