from app import app, db
from flask_login import login_required, current_user
from flask import request
from app.Components.response import Response
from app.models import Order, Product

@app.route('/api/v1/user/cart/checkout', methods=['POST'])
@login_required
def order():
    if current_user.userType == 'Seller':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'POST':
        data = request.get_json()
        product = Product.query.get(data['item_id'])
        quantity = data['quantity']

        if product.stocks < quantity or product.stocks == 0: 
            return Response(
                status=401,
                message="error"
            )

        order = Order(
            buyer_id = current_user.id,
            item_id = product.id,
            quantity = quantity,
        )

        order.create()
        
        return Response(
            status=200
        )


