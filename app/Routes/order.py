from app import app, db
from flask_login import login_required, current_user
from flask import request
from app.Components.response import Response
from app.models import Order, Item

@app.route('/api/v1/user/cart/checkout', methods=['POST'])
@login_required
def order():
    if current_user.user_type == 'Seller':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'POST':
        data = request.get_json()
        item = Item.query.get(data['item_id'])
        quantity = data['quantity']

        if item.stocks < quantity or item.stocks == 0: 
            return Response(
                status=401,
                message="error"
            )

        order = Order(
            buyer_id = current_user.id,
            item_id = item.id,
            quantity = quantity,
        )

        order.create()
        item.updateQuantity(quantity)
        
        return Response(
            status=200
        )


