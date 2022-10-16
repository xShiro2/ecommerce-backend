from app import db
from sqlalchemy.sql import func

class Item(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    shopitem_id = db.relationship('ShopItem', backref='item')
    
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'))
    
    dateCreated = db.Column(db.TIMESTAMP, server_default=func.now())
    dateUpdated = db.Column(db.TIMESTAMP, onupdate=func.now())

    def updateQuantity(self, quantity: int):
        self.quantity = self.quantity - quantity
        db.session.commit()
    
    def create(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



