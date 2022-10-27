from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from app.Components import model

class User(UserMixin, db.Model, model.Component):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    userType = db.Column(db.String(6), nullable=False)
    
    dateCreated = db.Column(db.TIMESTAMP, server_default=func.now())
    dateUpdated = db.Column(db.TIMESTAMP, onupdate=func.now())
    
    def create(self):
        if self.query.filter_by(email= self.email).first():
            return False
        else:
            db.session.add(self)
            db.session.commit()
            return True



