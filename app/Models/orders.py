from app import db
from sqlalchemy.sql import func

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Integer, nullable=False)

    dateCreated = db.Column(db.TIMESTAMP, server_default=func.now())

    def create(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}