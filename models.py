import os
from sqlalchemy import Column, String, create_engine, Integer, Date, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy import Column, String, Integer
import os
import re


database_path = os.getenv("DATABASE_URL")
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = 'super secret key'
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Actor(db.Model):
    __tablename__ = 'Actor'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(6), nullable=False)

    movie = db.relationship("Movie", back_populates="actor")

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        """
        Create new model object
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete existing model object
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """
        Update existing model object
        """
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }


class Movie(db.Model):
    __tablename__ = 'Movie'
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    release_date = Column(Date)

    actor_id = Column(Integer, ForeignKey('Actor.id'))
    actor = db.relationship("Actor", back_populates="movie")

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        """
        Create new model object
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete existing model object
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """
        Update existing model object
        """
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
