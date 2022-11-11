from app import app, db
from flask_login import login_required, current_user
from flask import request
from app.Components.response import Response
from app.models import Order, Shop, Product, OrderStatus

@login_required
@app.route('/api/v1/admin/reports', methods=['GET'])
def reports():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

