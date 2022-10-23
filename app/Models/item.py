from app import db
from sqlalchemy.sql import func
from app.Components import model

class Item(db.Model, model.Component):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    gender = db.Column(db.Integer, db.ForeignKey('gender.id'))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    dateCreated = db.Column(db.TIMESTAMP, server_default=func.now())
    dateUpdated = db.Column(db.TIMESTAMP, onupdate=func.now())

class Category(db.Model, model.Component):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    item = db.relationship('Item', backref='cat', lazy='joined')

    dateCreated = db.Column(db.TIMESTAMP, server_default=func.now())
    dateUpdated = db.Column(db.TIMESTAMP, onupdate=func.now())

class Gender(db.Model, model.Component):
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    item = db.relationship('Item', backref='gen', lazy='joined')

# class Color(db.Model):
#     __tablename__ = 'color'

#     id = db.Column(db.Integer, primary_key=True)
#     item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
#     color = db.Column(db.String(64), nullable=False)

#     def create(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     def to_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Variant(db.Model, model.Component):
    __tablename__ = 'size'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    size = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
