from src.todo_list_authentication.__init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()
# db = SQLAlchemy()


class User(db.Model, UserMixin):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')


class Note(db.Model):
    # __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
