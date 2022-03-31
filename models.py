"""Models for Blogly."""
from sqlite3 import Timestamp
from xmlrpc.client import DateTime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User Class """

    __tablename__ = "users"

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(20),
                    nullable=False)
    last_name = db.Column(db.String(20),
                    nullable=False)
    image_url = db.Column(db.Text,
                    nullable=True)


class Post(db.Model):
    """ Post Class """

    __tablename__ = "posts"

    def __repr__(self):
        """Show info post information."""

        p = self
        return f"<Post {p.id} {p.title} Created at: \
            {p.created_at} by user {p.user_id}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(20),
                    nullable=False)
    content = db.Column(db.String(20),
                    nullable=False)
    created_at = db.Column(db.DateTime,
                    nullable=False,
                    default = db.func.now())
    user_id = db.Column(
                db.Integer,
                db.ForeignKey("users.id"))

    users = db.relationship('User',
                            backref="posts")
