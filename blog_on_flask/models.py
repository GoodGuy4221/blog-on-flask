from datetime import datetime
from uuid import uuid4

from flask_login import UserMixin
from blog_on_flask import db, login_manager


def uuid4_string(func):
    def wrapper(*args, **kwargs):
        uuid4_to_string = str(func(*args, **kwargs))
        return uuid4_to_string

    return wrapper


uuid4 = uuid4_string(uuid4)


@login_manager.user_loader
def load_user(user_uid):
    return User.query.get(user_uid)


class User(db.Model, UserMixin):
    uid = db.Column(db.String(36), primary_key=True, default=uuid4)
    username = db.Column(db.String(24), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    image_file = db.Column(db.String(64), nullable=True, default='default.png')
    password = db.Column(db.String(64), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_id(self):
        try:
            return self.uid
        except AttributeError:
            raise NotImplementedError("No `uid` attribute - override `get_id`") from None

    def __repr__(self):
        return f'Пользователь с логином: {self.username} | email: {self.email}'


class Post(db.Model):
    uid = db.Column(db.String(36), primary_key=True, default=uuid4)
    title = db.Column(db.String(128), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_uid = db.Column(db.String(36), db.ForeignKey('user.uid'), nullable=False)

    def __repr__(self):
        return f'Пост: {self.title} | {self.date_posted}'
