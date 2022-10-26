from app import db
from sqlalchemy.sql import func
from app.Components import model

class Shop(db.Model, model.Component):
    __tablename__ = 'shop'

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # name = db.Column(db.String(20), nullable=False)
    # location = db.Column(db.Text, nullable=False)
    # description = db.Column(db.Text)

    dateCreated = db.Column(db.TIMESTAMP, server_default=func.now())
    dateUpdated = db.Column(db.TIMESTAMP, onupdate=func.now())


