import os

import dash_bootstrap_components as dbc
import flask
import redis
from dash import Dash
from rq import Queue

server = flask.Flask(__name__)

app = Dash(
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    serve_locally=False,
)

# redis connection and RQ queue
# use heroku-redis service when deploying to Heroku
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
conn = redis.from_url(redis_url)
queue = Queue(connection=conn)
