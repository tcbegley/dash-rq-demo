from rq import Connection, Worker

from dash_rq_demo import app, conn, queue

if __name__ == "__main__":
    with app.server.app_context():
        with Connection(conn):
            w = Worker([queue])
            w.work()
