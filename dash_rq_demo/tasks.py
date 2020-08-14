import datetime
import time

from rq import get_current_job


def slow_loop(s, id_):
    """
    Converts a string to upper case character by character. Will update the
    database to log start and completion times.

    Parameters
    ----------
    s : str
        String to convert to upper case
    id_ : uuid.UUID
        The job id for the submitted task.
    """
    # Store completion percentage in redis under the process id
    job = get_current_job()
    job.meta["progress"] = 0
    job.save_meta()

    upper_case = []
    for i, c in enumerate(s):
        upper_case.append(c.upper())
        time.sleep(0.1)
        # update completion percentage so it's available from front-end
        job.meta["progress"] = 100 * (i + 1) / len(s)
        job.save_meta()

    res = "".join(upper_case)

    return res
