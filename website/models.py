# Create DB models
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class WorkLog(db.Model):
    __tablename__ = 'worklog'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    date = db.Column(db.Date())
    start_time = db.Column(db.Time(timezone=False), default=func.now())
    end_time = db.Column(db.Time(timezone=False), default=func.now())
    # F-key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, date, start_time, end_time, content, user_id):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.content = content
        self.user_id = user_id


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    identity = db.Column(db.String(50))
    worklogs = db.relationship('WorkLog')

    def __init__(self, name, email, password, identity):
        self.name = name
        self.email = email
        self.password = password
        self.identity = identity
