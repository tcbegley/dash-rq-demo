from sqlalchemy.dialects.postgresql import UUID

from .core import db


class Result(db.Model):
    """
    A model for the results table in the database.
    """
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    queued = db.Column(db.DateTime)
    started = db.Column(db.DateTime)
    completed = db.Column(db.DateTime)
    result = db.Column(db.Text)

    def __repr__(self):
        return "<Result %r>" % self.result
