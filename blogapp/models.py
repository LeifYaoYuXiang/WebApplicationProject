#encoding:utf-8
from datetime import datetime
from blogapp import db


class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50))
    tag = db.Column(db.String(10))
    time = db.Column(db.String)
    click = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Blog {}>'.format(self.title)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    information = db.Column(db.String(100))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.information)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,unique=True)
    email = db.Column(db.String(64), index=True,unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),index=True,unique=True)
    tag = db.Column(db.String(10))
    description = db.Column(db.String(140))
    download = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<name {}>'.format(self.name)
