import datetime
import time

from core import Result, db


def slow_multiply(x, y, pid):
    result = Result.query.filter_by(pid=pid).first()
    result.started = datetime.datetime.now()
    db.session.add(result)
    db.session.commit()

    time.sleep(3)
    r = x * y

    result.completed = datetime.datetime.now()
    result.result = r
    db.session.add(result)
    db.session.commit()
