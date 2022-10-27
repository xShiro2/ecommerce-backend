from app import db
from sqlalchemy.sql import func
from app.Components import model

class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def create(self):
        db.session.add(self)
        db.session.commit()

class CartItem(db.Model, model.Component):
    __tablename__ = 'cart_item'

    id = db.Column(db.Integer, primary_key=True)
    cart = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)

    dateAdded = db.Column(db.TIMESTAMP, server_default=func.now())
    dateUpdated = db.Column(db.TIMESTAMP, onupdate=func.now())