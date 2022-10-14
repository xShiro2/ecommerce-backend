from app import db
from sqlalchemy.sql import func

class Item(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    shopitem_id = db.relationship('ShopItem', backref='item')
    
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stocks = db.Column(db.Integer, nullable=False)
    
    date_created = db.Column(db.DateTime, server_default=func.now())
    date_updated = db.Column(db.DateTime, onupdate=func.now())

    def updateStock(self, quantity: int):
        self.stocks = self.stocks - quantity
        db.session.commit()
    
    def create(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



