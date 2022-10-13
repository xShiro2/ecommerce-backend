from app import db

class ShopItem(db.Model):
    __tablename__ = 'shop_item'

    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def create(self):
        db.session.add(self)
        db.session.commit()