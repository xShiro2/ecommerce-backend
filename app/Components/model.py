from app import db

class Component():
    def create(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self, exclude=[]):
        dic = {}
        for c in self.__table__.columns:
            if c.name not in exclude:
                dic[c.name] = getattr(self, c.name)

        return dic