from rq import Connection, Worker

from dash_rq_demo import conn, queue

if __name__ == "__main__":
    with Connection(conn):
        w = Worker([queue])
        w.work()
