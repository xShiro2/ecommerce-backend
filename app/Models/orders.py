from app import db
from sqlalchemy.sql import func
from app.Components import model

class Order(db.Model, model.Component):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)

    dateCreated = db.Column(db.TIMESTAMP, server_default=func.now())