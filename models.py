"""Pet Model"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """Pet."""

    __tablename__ = "pets"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False)
    species = db.Column(db.Text,
                     nullable=False)
    photo_url = db.Column (db.Text,
                           nullable = True)
    age = db.Column (db.Integer,
                           nullable = True)
    notes = db.Column (db.Text,
                           nullable = True)
    available = db.Column (db.Boolean,
                           nullable = False)

    def __init__(self, name, species, photo_url=None, age=None, notes=None, available=True):
            self.name = name
            self.species = species
            self.photo_url = photo_url
            self.age = age
            self.notes = notes
            self.available = available