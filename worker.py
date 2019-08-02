from rq import Connection, Worker

from core import app, queue

if __name__ == "__main__":
    with app.server.app_context():
        with Connection():
            w = Worker([queue])
            w.work()
