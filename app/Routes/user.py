from app import app
from flask_login import login_required, current_user
from flask import request
from app.Components.response import Response

@app.route('/api/v1/user', methods=['GET', 'POST', 'DELETE'])
@login_required
def users():
    if request.method == 'GET':
        return Response(
            status = 200,
            message= "",
            data = {
                "user": current_user.to_dict(),
            }
        )