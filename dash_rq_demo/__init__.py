import datetime
import uuid

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from .core import app, db, queue
from .models import Result
from .tasks import slow_multiply

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        dcc.Interval(id="interval", interval=500),
        html.H2("Redis / RQ demo", className="display-4"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dbc.Input(type="number", placeholder="x", id="x")),
                dbc.Col(dbc.Input(type="number", placeholder="y", id="y")),
            ],
            className="mb-3",
        ),
        dbc.Button("Multiply", id="button", color="primary"),
        html.P(id="output"),
    ]
)


@app.callback(
    Output("store", "data"),
    [Input("button", "n_clicks")],
    [State("x", "value"), State("y", "value")],
)
def submit(n_clicks, x, y):
    if n_clicks:
        pid = uuid.uuid4()

        # queue the task
        queue.enqueue(slow_multiply, x, y, pid)

        # record queuing in the database
        result = Result(pid=pid, queued=datetime.datetime.now())
        db.session.add(result)
        db.session.commit()

        # log process id in dcc.Store
        return {"pid": str(pid)}
    return {}


@app.callback(
    Output("output", "children"),
    [Input("interval", "n_intervals")],
    [State("store", "data")],
)
def retrieve_output(n, data):
    if n and data:
        result = Result.query.filter_by(pid=data["pid"]).first()
        if result:
            if result.result:
                return result.result
            elif result.started and not result.completed:
                return "Processing..."
    return None
