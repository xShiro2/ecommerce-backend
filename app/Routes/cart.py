from flask import request
from app import app
from app.models import Cart, CartItem, Product, QuantityStatus, Shop, User
from flask_login import login_required, current_user
from app.Components.response import Response

@login_required
@app.route('/api/v1/user/cart', methods=['POST', 'GET'])
def cart():
    if current_user.userType == 'Seller':
        return Response(
            status=403,
            message="error",
        )
    
    if request.method == 'POST':
        data = request.get_json()
        cart = Cart.query.filter_by(user=current_user.id).first()
        
        if not cart:
            cart = Cart(user=current_user.id)
            cart.create()
        
        cartItem = CartItem(
            cart = cart.id,
            product = data['id'],
            quantity = data['quantity']
        )

        cartItem.create()

        return Response(
            status=201
        )
    
    if request.method == 'GET':
        cart = Cart.query.filter_by(user=current_user.id).first()
        
        if not cart:
            cart = Cart(user=current_user.id)
            cart.create()

        cart_items = CartItem.query.filter_by(cart=cart.id).all()

        if cart_items:
            items = []
            for item in cart_items:
                product = Product.query.filter_by(id=item.id).first()
                shop = Shop.query.get(product.shop)
                user = User.query.get(shop.user)

                prod = product.to_dict(exclude=['image', 'description', 'shop', 'dateCreated', 'dateUpdated'])
                prod['category'] = product.cat.name
                prod['gender'] = product.gen.name
                prod['quantity'] = item.quantity
                prod['seller'] = user.firstName +" "+ user.lastName
                prod['sellerAddress'] = user.address
                items.append(prod)

            return Response(
                status=200,
                data= items
            )

        return Response(
            status=200,
        )
        
@login_required
@app.route('/api/v1/user/cart/<id>', methods=['DELETE'])
def delete(id):
    if request.method == 'DELETE':
        cart = Cart.query.filter_by(user=current_user.id).first()
        cart_item = CartItem.query.filter_by(cart=cart.id, id=id).first()
        cart_item.delete()

        return Response(
            status=200
        )