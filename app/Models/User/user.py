from xmlrpc import server
from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    user_type = db.Column(db.String(6), nullable=False)
    
    date_created = db.Column(db.DateTime, server_default=func.now())
    date_updated = db.Column(db.DateTime, onupdate=func.now())
    
    def create(self):
        if self.query.filter_by(email= self.email).first():
            return False
        else:
            db.session.add(self)
            db.session.commit()
            return True
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



