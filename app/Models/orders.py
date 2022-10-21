from app import db
from sqlalchemy.sql import func
from app.Components import model

class Order(db.Model, model.Component):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    size = db.Column(db.Integer, db.ForeignKey('size.id'))
    quantity = db.Column(db.Integer, nullable=False)

    dateCreated = db.Column(db.TIMESTAMP, server_default=func.now())