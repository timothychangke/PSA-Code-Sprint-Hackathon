from . import db
from flask_login import UserMixin
from sqlalchemy import func

class Approved_courses(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(150), unique=True)
    organisation = db.Column(db.String(150))
    
class User_courses(db.Model, UserMixin):
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    courses = db.relationship('User_courses')