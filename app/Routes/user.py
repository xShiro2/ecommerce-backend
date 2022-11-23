from app import app
from flask_login import login_required, current_user
from flask import request
from app.Components.response import Response
from app.models import Shop
    
@app.route('/api/v1/user', methods=['GET'])
@login_required
def users():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return Response(
                status = 401
            )
        return Response(
            status = 200,
            message= "",
            data = current_user.to_dict(exclude=['password']),
        )

@app.route('/api/v1/user/delivery', methods=['GET'])
@login_required
def delivery():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return Response(
                status = 401
            )

        data = {
            'fullname': current_user.firstName + ' ' + current_user.lastName,
            'number': current_user.number,
            'address': current_user.address
        }

        return Response(
            status = 200,
            message= "",
            data = data,
        )

@app.route('/api/v1/user/admin', methods=['GET'])
@login_required
def admin():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'GET':
        if not current_user.is_authenticated:
            return Response(
                status = 401
            )

        user = current_user.to_dict(exclude=['password'])
        shop = Shop.query.filter_by(user=current_user.id).first()

        if shop:
            user['shop'] = shop.id

        return Response(
            status = 200,
            data = user,
        )

