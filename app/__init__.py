from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeeey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/ecommerce_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)

from app import routes
from app import models

@app.before_first_request
def create_tables():
    #db.drop_all()
    db.create_all()
    db.session.commit()

    # create sample gender
    gender = [
        "Male",
        "Female",
        "Kids-Boy",
        "Kids-Girl",
        "Unisex"
    ]

    if not models.Gender.query.all():
        for i in gender:
            gen = models.Gender(name=i)
            gen.create()

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))