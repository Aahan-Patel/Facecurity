from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date
from uuid import uuid1
import pytz
import random
import string

# Kabir was here
db = SQLAlchemy()


def db_code(len):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(len))
    return result_str


class User(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(100))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    profile_picture = db.Column(db.String(100))
    block_id = db.Column(db.String(100))

    def __init__(self, type, name, email, password, profile_picture, block_id):
        self.name = name
        self.type = type
        self.email = email
        self.password = password
        self.profile_picture = profile_picture
        self.block_id = block_id


class Block(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(100))
    block_id = db.Column(db.String(100))

    def __init__(self, url, block_id):
        self.url = url
        self.block_id = block_id
