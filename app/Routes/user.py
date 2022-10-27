from app import app
from flask_login import login_required, current_user
from flask import request
from app.Components.response import Response
    
@app.route('/api/v1/user', methods=['GET', 'POST', 'DELETE'])
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

@app.route('/api/v1/user/admin', methods=['GET', 'POST', 'DELETE'])
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
        return Response(
            status = 200,
            message= "",
            data = current_user.to_dict(exclude=['password']),
        )

