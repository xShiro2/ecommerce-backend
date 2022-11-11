from flask import request
from app import app
from app.models import Cart, Sold, CartItem, Product, QuantityStatus, Order, OrderStatus
from flask_login import login_required, current_user
from app.Components.response import Response

@login_required
@app.route('/api/v1/checkout', methods=['POST'])
def checkout():
    if current_user.userType == 'Seller':
        return Response(
            status=403,
            message="error",
        )
    
    if request.method == 'POST':
        data = request.get_json()
        fullname = data['fullname']
        num = data['phonenumber']
        address = data['address']

        cart = Cart.query.filter_by(user=current_user.id).first()
        cart_items = CartItem.query.filter_by(cart=cart.id).all()

        if cart_items:
            status = OrderStatus.query.filter_by(name="Pending").first()
            for item in cart_items:
                product = Product.query.get(item.product)
                quantityStatus = QuantityStatus.query.filter_by(product=product.id).first()

                order = Order(
                    user=current_user.id,
                    product=product.id,
                    quantity=item.quantity,

                    fullname=fullname,
                    number=num,
                    address=address,
                    
                    status = status.id
                )

                order.create()

                quantityStatus.quantity -= item.quantity
                quantityStatus.update()

                sold = Sold.query.filter_by(product=product.id).first()
                sold.quantity += item.quantity
                sold.update()

                item.delete()

            return Response(
                status=201
            )