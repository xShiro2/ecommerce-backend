from flask import request
from flask_login import login_user, login_required, logout_user
from app import app
from app.models import User, Cart
from werkzeug.security import generate_password_hash, check_password_hash
from app.Components.response import Response

@app.route('/api/v1/signup', methods = ['POST'])
def signup():
    if request.method == 'POST':
        try:
            user = request.get_json()

            user = User(
                firstName = user['firstName'],
                lastName = user['lastName'],
                email = user['email'],
                password = generate_password_hash(user['password']),
                address = user['address'],
                number = user['number'],
                age = user['age'],
                gender = user['gender'],
                userType = user['userType'],
            )
            
            result = user.create()

            if result:
                if user.userType == 'Buyer':        
                    cart = Cart(user=user.id)
                    cart.create()

                login_user(user, remember=True)
                
                return Response(
                    status=201,
                    message="sucess"
                )

            return Response(
                status=409,
                message="error"
            )

        except Exception as e:
            print(e)
            return Response(
                status=500,
                message="internal error"
            )

@app.route('/api/v1/login', methods= ['POST'])
def login():
    if request.method == 'POST':
        try:
            request_data = request.get_json()

            email = request_data['email']
            password = request_data['password']
            remember = True

            user = User().query.filter_by(email=email).first()

            if not user:
                return Response(
                    status=401,
                    message="error"
                )

            if not check_password_hash(user.password, password):
                return Response(
                    status=401,
                    message="error"
                )

            login_user(user, remember=remember)
            
            return Response(
                status=200,
                data={
                    "id": user.id,
                    "userType": user.userType
                }
            )

        except Exception as e:
            return Response(
                status=500,
                message="internal error"
            )

@app.route('/api/v1/logout')
@login_required
def logout():
    logout_user()

    return Response(
        status=200
    )
