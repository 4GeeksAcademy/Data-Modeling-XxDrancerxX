from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum
from sqlalchemy import Enum as SqlEnum


db = SQLAlchemy()


class FriendshipStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"
    REJECTED = "rejected"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    posts = db.relationship("Post", backref="user")
    comments = db.relationship("Comments", backref="user")
    likes = db.relationship("Likes", backref="user")
    friends = db.relationship("Friends", backref="initiator", foreign_keys="Friends.user_id")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "posts": [post.serialize() for post in self.posts],
            "comments": [comment.serialize() for comment in self.comments],
            "friends": [friend.serialize() for friend in self.friends],
            "likes": [like.serialize() for like in self.likes]
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=True, default="active")
    comments = db.relationship("Comments", backref="post")
    content = db.Column(db.Text, nullable=True)
    likes = db.relationship("Likes", backref="post")

    def serialize(self):
        return {
            "id": self.id,
            "status": self.status,
            "comments": [comment.serialize() for comment in self.comments],
            "content": self.content,
            "likes": [like.serialize() for like in self.likes]
            # do not serialize the password, its a security breach
        }


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'friend_id'),)
    status = db.Column(SqlEnum(FriendshipStatus), nullable=False, default=FriendshipStatus.PENDING)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "friend_id": self.friend_id,
            "status": self.status.value
        }


class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id

        }


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(250), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "date": self.date,
            "text": self.text
        }


from eralchemy2 import render_er
render_er(db.Model, 'diagram.png')
