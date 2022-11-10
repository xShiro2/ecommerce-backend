from app import db
from sqlalchemy.sql import func
from app.Components import model

class Order(db.Model, model.Component):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    
    fullname = db.Column(db.Text, nullable=False)
    number = db.Column(db.String(14), nullable=False)
    address = db.Column(db.Text, nullable=False)

    status = db.Column(db.Integer, db.ForeignKey('orderStatus.id'))
    dateCreated = db.Column(db.TIMESTAMP, server_default=func.now())

class OrderStatus(db.Model, model.Component):
    __tablename__ = 'orderStatus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)

class Sold(db.Model, model.Component):
    __tablename__ = 'sold'

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)