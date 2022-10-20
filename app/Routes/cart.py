from flask import request
from app import app
from app.models import Cart, CartItem
from flask_login import login_required, current_user
from app.Components.response import Response

@login_required
@app.route('/api/v1/user/cart', methods=['POST', 'GET'])
def cart():
    if current_user.user_type == 'Seller':
        return Response(
            status=403,
            message="error",
        )
    
    if request.method == 'POST':
        data = request.get_json()
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        
        if not cart:
            cart = Cart(user_id=current_user.id)
            cart.create()
        
        cartItem = CartItem(
            cart_id = cart.id,
            item_id = data['item_id'],
            quantity = data['quantity']
        )

        cartItem.create()

        return Response(
            status=201
        )
    
    if request.method == 'GET':
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        
        if not cart:
            cart = Cart(user_id=current_user.id)
            cart.create()

        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()

        if cart_items:
            items = {}
            for i, item in enumerate(cart_items):
                items[i] = item.to_dict()

            return Response(
                status=200,
                data= items
            )

        return Response(
            status=200,
        )
        