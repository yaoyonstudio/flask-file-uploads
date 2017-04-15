from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()

class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_name = db.Column(db.String(250), nullable=False)
    photo_source = db.Column(db.String(250), nullable=False)
    photo_thumb = db.Column(db.String(250), nullable=False)

    def __init__(self, id, photo_name, photo_source, photo_thumb):
        self.id = id
        self.photo_name = photo_name
        self.photo_source = photo_source
        self.photo_thumb = photo_thumb

    def __str__(self):
        return "Photo(id='%s')" % self.id

    def add(self, photo):
        db.session.add(photo)
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
