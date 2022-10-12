from flask import request
from flask_login import login_user, current_user, login_required, logout_user
from app import app
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/api/v1/signup', methods = ['POST'])
def signup():
    if request.method == 'POST':
        user = request.get_json()

        fname = user['firstName']
        lname = user['lastName']
        email = user['email']
        password = user['password']
        address = user['address']
        age = user['age']
        gender = user['gender']
        user_type = user['userType']
        
        try:
            password = generate_password_hash(password)

            user = User(
                first_name = fname, 
                last_name = lname,
                email = email,
                password = password,
                address = address,
                age = age,
                gender = gender,
                user_type = user_type
            )

            result = user.create()

            if result:
                return {
                    'status': 201,
                    'message': 'Signup Successful',
                }, 201

            return {
                'status': 409,
                'message': 'Email already exists',
            }, 409

        except Exception as e:
            return {
                'message': str(e),
                'status': 500,
            }, 500

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
                return {
                    'status': 401,
                    'message': 'Email does not exist'
                }, 401

            if not check_password_hash(user.password, password):
                return {
                    'status': 401,
                    'message': 'Password incorrect'
            }, 401

            login_user(user, remember=remember)
            
            return {
                'message': 'Login Successful',
                'data': {
                    "id":current_user.id,
                    'userType': current_user.user_type
                },
                'status': 200
            }, 200

        except ValueError as e:
            return {
                'message': str(e),
                'status': 500,
            }, 500

@app.route('/api/v1/logout')
@login_required
def logout():
    logout_user()

    return {
        'status': 200,
        'message': 'Logout Successful'
    }, 200

@app.route('/api/v1/users', methods=['GET'])
@login_required
def users():
    if request.method == 'GET':
        return {
            'id': current_user.id
        }, 200