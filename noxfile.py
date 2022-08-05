import nox

nox.options.sessions = ["lint"]

SOURCES = ["dash_rq_demo", "run_locally.py", "worker.py"]


@nox.session()
def lint(session):
    """Lint python source"""
    session.install("black", "isort", "flake8")
    session.run("black", "--check", *SOURCES)
    session.run("isort", "--check", *SOURCES)
    session.run("flake8", *SOURCES)


@nox.session(name="format")
def format_(session):
    """Format Python source"""
    session.install("black", "isort")
    session.run("black", *SOURCES)
    session.run("isort", *SOURCES)
