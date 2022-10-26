from flask import request
from flask_login import login_user, login_required, logout_user
from app import app
from app.models import User, Shop
from werkzeug.security import generate_password_hash, check_password_hash
from app.Components.response import Response

@app.route('/api/v1/signup', methods = ['POST'])
def signup():
    if request.method == 'POST':
        try:
            user = request.get_json()

            fname = user['firstName']
            lname = user['lastName']
            email = user['email']
            password = user['password']
            address = user['address']
            age = user['age']
            gender = user['gender']
            user_type = user['userType']
        
            password = generate_password_hash(password)

            user = User(
                first_name = fname, 
                last_name = lname,
                email = email,
                password = password,
                address = address,
                age = age,
                gender = gender,
                user_type = user_type,
            )

            result = user.create()

            if result:
                if user.user_type == 'Seller':
                    shop = Shop(seller_id=user.id)
                    shop.create()

                return Response(
                    status=201,
                    message="sucess"
                )

            return Response(
                status=409,
                message="error"
            )

        except Exception as e:
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
            #remember = request_data['remember']
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
                    "userType": user.user_type
                }
            )

        except ValueError as e:
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
