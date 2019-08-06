import datetime
import time

from .core import conn, db
from .models import Result


def slow_loop(s, pid):
    """
    Converts a string to upper case character by character. Will update the
    database to log start and completion times.

    Parameters
    ----------
    s : str
        String to convert to upper case
    pid : uuid.UUID
        The process id for the submitted task.
    """
    # Update the database to confirm that task has started processing
    result = Result.query.filter_by(pid=pid).first()
    result.started = datetime.datetime.now()
    db.session.add(result)
    db.session.commit()

    # Store completion percentage in redis under the process id
    conn.set(str(pid), 0)

    upper_case = []
    for i, c in enumerate(s):
        upper_case.append(c.upper())
        time.sleep(0.1)
        # update completion percentage so it's available from front-end
        conn.set(str(pid), 100 * (i + 1) / len(s))

    # update the database to confirm that task has completed processing
    result.completed = datetime.datetime.now()
    result.result = "".join(upper_case)
    db.session.add(result)
    db.session.commit()

    # no longer need completion percentage stored in Redis
    conn.delete(str(pid))
