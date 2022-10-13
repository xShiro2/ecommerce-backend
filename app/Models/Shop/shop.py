from app import db

class Shop(db.Model):
    __tablename__ = 'shop'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    location = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


