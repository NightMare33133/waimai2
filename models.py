from exts import db
from datetime import datetime
from hashlib import md5
from flask_login import UserMixin

class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200),nullable=False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    join_time = db.Column(db.DateTime,default=datetime.now)
    icon = db.Column(db.String(200),default='/images/jiaran2')
    money = db.Column(db.Integer, default=0)
    # BirthDay = db.Column(db.DateTime, nullable=True)
    # gravatar = db.Column(db.String(200), default='/static/images/diana2.jpg')

# class DishesModel(db.Model):
#     __tablename__ = "dishes"

class CommentModel(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    icon = db.Column(db.String(200))

    author = db.relationship("UserModel",backref="dishes")

class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    comment_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))


    comment = db.relationship("CommentModel", backref=db.backref("answers", order_by=create_time.desc()))
    author = db.relationship("UserModel", backref="answers")

class User(UserMixin, db.Model):
    # ...
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

class XiaDan(db.Model):
    __tablename__ = "xiadan"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dish = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    delivery_address = db.Column(db.String(200), nullable=False)
    arrival_time = db.Column(db.DateTime)
    telephone_number = db.Column(db.String(200), nullable=False)
    state = db.Column(db.Integer,default=0)

class Rider(db.Model):
    __tablename__ = "rider"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    money = db.Column(db.Integer,default=0)
