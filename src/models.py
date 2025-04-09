from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SqlEnum
from enum import Enum

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
    username = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    registration_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    posts = db.relationship("Post", backref="user")
    comments = db.relationship("Comments", backref="user")
    likes = db.relationship("Likes", backref="user")
    friends = db.relationship("Friends", backref="initiator", foreign_keys="Friends.user_id")
    favorites = db.relationship("Favorites", backref="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "registration_date": self.registration_date.isoformat() if self.registration_date else None,
            "posts": [post.serialize() for post in self.posts],
            "comments": [comment.serialize() for comment in self.comments],
            "friends": [friend.serialize() for friend in self.friends],
            "likes": [like.serialize() for like in self.likes],
            "favorites": [favorite.serialize() for favorite in self.favorites]
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
            "date": self.date.isoformat() if self.date else None,
            "status": self.status,
            "content": self.content,
            "comments": [comment.serialize() for comment in self.comments],
            "likes": [like.serialize() for like in self.likes]
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

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    species = db.Column(db.String(50), nullable=True)
    homeworld_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)
    homeworld = db.relationship("Planet", backref="characters")
    favorites = db.relationship("Favorites", backref="character", foreign_keys="Favorites.character_id")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "species": self.species,
            "homeworld_id": self.homeworld_id
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    climate = db.Column(db.String(50), nullable=True)
    population = db.Column(db.BigInteger, nullable=True)
    favorites = db.relationship("Favorites", backref="planet", foreign_keys="Favorites.planet_id")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "climate": self.climate,
            "population": self.population
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)
    added_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    __table_args__ = (
        db.CheckConstraint('NOT(character_id IS NULL AND planet_id IS NULL)', name='check_favorite_type'),
        db.UniqueConstraint('user_id', 'character_id', 'planet_id', name='unique_user_favorite')
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "added_date": self.added_date.isoformat() if self.added_date else None
        }

if __name__ == '__main__':
    from eralchemy2 import render_er
    render_er(db.Model, 'diagram.png')