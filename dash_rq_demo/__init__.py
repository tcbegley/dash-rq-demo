import datetime
import uuid

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from rq.exceptions import NoSuchJobError
from rq.job import Job

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
        id_ = uuid.uuid4()

        # queue the task
        queue.enqueue(slow_loop, text, id_, job_id=str(id_))

        # record queuing in the database
        result = Result(id=id_, queued=datetime.datetime.now())
        db.session.add(result)
        db.session.commit()

        # log process id in dcc.Store
        return {"id": str(id_)}
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
        try:
            job = Job.fetch(data["id"], connection=conn)
            if job.get_status() == "finished":
                return job.result, 100, False
            progress = job.meta.get("progress", 0)
            return f"Processing - {progress:.1f}% complete", progress, True
        except NoSuchJobError:
            # if job no longer exists, retrive result from database
            result = Result.query.filter_by(id=data["id"]).first()
            if result and result.result:
                return result.result, 100, False
    return None, None, False
