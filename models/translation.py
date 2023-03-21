# models/translation.py
from extensions import db

class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    translation = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
