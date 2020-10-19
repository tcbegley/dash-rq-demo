import uuid
from collections import namedtuple

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from rq.exceptions import NoSuchJobError
from rq.job import Job

from .core import app, conn, queue
from .tasks import slow_loop

# use named tuple for return value of multiple output callback for readability
Result = namedtuple(
    "Result", ["result", "progress", "collapse_is_open", "finished_data"]
)

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
        # two stores, one to track which job was most recently started, one to
        # track which job was most recently completed. if they differ, then
        # there is a job still running.
        dcc.Store(id="submitted-store"),
        dcc.Store(id="finished-store"),
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
    Output("submitted-store", "data"),
    [Input("button", "n_clicks")],
    [State("text", "value")],
)
def submit(n_clicks, text):
    """
    Submit a job to the queue, log the id in submitted-store
    """
    if n_clicks:
        id_ = str(uuid.uuid4())

        # queue the task
        queue.enqueue(slow_loop, text, job_id=id_)

        # log process id in dcc.Store
        return {"id": id_}

    return {}


@app.callback(
    [
        Output("output", "children"),
        Output("progress", "value"),
        Output("collapse", "is_open"),
        Output("finished-store", "data"),
    ],
    [Input("interval", "n_intervals")],
    [State("submitted-store", "data")],
)
def retrieve_output(n, submitted):
    """
    Periodically check the most recently submitted job to see if it has
    completed.
    """
    if n and submitted:
        try:
            job = Job.fetch(submitted["id"], connection=conn)
            if job.get_status() == "finished":
                # job is finished, return result, and store id
                return Result(
                    result=job.result,
                    progress=100,
                    collapse_is_open=False,
                    finished_data={"id": submitted["id"]},
                )

            # job is still running, get progress and update progress bar
            progress = job.meta.get("progress", 0)
            return Result(
                result=f"Processing - {progress:.1f}% complete",
                progress=progress,
                collapse_is_open=True,
                finished_data=dash.no_update,
            )
        except NoSuchJobError:
            # something went wrong, display a simple error message
            return Result(
                result="Error: result not found...",
                progress=None,
                collapse_is_open=False,
                finished_data=dash.no_update,
            )
    # nothing submitted yet, return nothing.
    return Result(
        result=None, progress=None, collapse_is_open=False, finished_data={}
    )


@app.callback(
    Output("interval", "disabled"),
    [Input("submitted-store", "data"), Input("finished-store", "data")],
)
def disable_interval(submitted, finished):
    if submitted:
        if finished and submitted["id"] == finished["id"]:
            # most recently submitted job has finished, no need for interval
            return True
        # most recent job has not yet finished, keep interval going
        return False
    # no jobs submitted yet, disable interval
    return True
