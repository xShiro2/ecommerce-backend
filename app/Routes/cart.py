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
        product = Product.query.get(data['id'])
        quantity = data['quantity']
        cart = Cart.query.filter_by(user=current_user.id).first()
        cartItem = CartItem.query.filter_by(cart=cart.id, product=product.id).first()

        if cartItem:
            cartItem.quantity = quantity + cartItem.quantity
            cartItem.update()

            return Response(
                status=201
            )

        cartItem = CartItem(
            cart = cart.id,
            product = product.id,
            quantity = quantity
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
                product = Product.query.get(item.product)
                shop = Shop.query.get(product.shop)

                prod = product.to_dict(exclude=['image', 'description', 'shop', 'dateCreated', 'dateUpdated'])
                prod['category'] = product.cat.name
                prod['gender'] = product.gen.name
                prod['quantity'] = item.quantity
                prod['shop'] = shop.shopName
                items.append(prod)

            return Response(
                status=200,
                data= items,
                message=len(items)
            )

        return Response(
            status=200,
        )
        
@login_required
@app.route('/api/v1/user/cart/<id>', methods=['DELETE'])
def delete(id):
    if request.method == 'DELETE':
        cart = Cart.query.filter_by(user=current_user.id).first()
        cart_item = CartItem.query.filter_by(cart=cart.id, product=id).first()
        cart_item.delete()

        return Response(
            status=200
        )