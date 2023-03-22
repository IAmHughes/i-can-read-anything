from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(500), nullable=True)
    languages = relationship("UserLanguage", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserLanguage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(100), nullable=False)
    proficiency = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="languages")