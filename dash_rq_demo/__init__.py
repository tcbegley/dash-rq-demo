import datetime
import uuid

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from .core import app, conn, db, queue
from .models import Result
from .tasks import slow_loop

EXPLAINER = """
This app demonstrates asynchronous execution of long running tasks in Dash
using Redis and RQ. When you type text in the box below and click on the
'Upper case' button, the text will be converted to upper case character by
character (with a time delay in each iteration of the loop). An interval checks
periodically for completion of the task, and also updates a progress bar in the
UI to inform the user of the progress being made.
"""

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        dcc.Interval(id="interval", interval=500),
        html.H2("Redis / RQ demo", className="display-4"),
        html.P(EXPLAINER),
        html.Hr(),
        dbc.Textarea(id="text", className="mb-3"),
        dbc.Button(
            "Upper case", id="button", color="primary", className="mb-3"
        ),
        dbc.Collapse(
            dbc.Progress(id="progress", className="mb-3"), id="collapse"
        ),
        html.P(id="output"),
    ]
)


@app.callback(
    Output("store", "data"),
    [Input("button", "n_clicks")],
    [State("text", "value")],
)
def submit(n_clicks, text):
    if n_clicks:
        pid = uuid.uuid4()

        # queue the task
        queue.enqueue(slow_loop, text, pid)

        # record queuing in the database
        result = Result(pid=pid, queued=datetime.datetime.now())
        db.session.add(result)
        db.session.commit()

        # log process id in dcc.Store
        return {"pid": str(pid)}
    return {}


@app.callback(
    [
        Output("output", "children"),
        Output("progress", "value"),
        Output("collapse", "is_open"),
    ],
    [Input("interval", "n_intervals")],
    [State("store", "data")],
)
def retrieve_output(n, data):
    if n and data:
        result = Result.query.filter_by(pid=data["pid"]).first()
        if result:
            if result.result:
                return result.result, 100, False
            elif result.started and not result.completed:
                percent = float(conn.get(data["pid"]))
                return f"Processing - {percent:.1f}% complete", percent, True
    return None, None, False
