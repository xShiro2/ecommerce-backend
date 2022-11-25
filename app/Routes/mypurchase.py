from flask import request
from app import app
from app.models import Product, Order, OrderStatus, Shop
from flask_login import login_required, current_user
from app.Components.response import Response

@login_required
@app.route('/api/v1/mypurchase', methods=['GET'])
def mypurchase():
    if current_user.userType == 'Seller':
        return Response(
            status=403,
            message="error",
        )
    
    if request.method == 'GET':
        orders = Order.query.order_by(Order.dateCreated.desc()).filter_by(user=current_user.id).all()

        products = []
        for order in orders:
            product = Product.query.get(order.product)
            status = OrderStatus.query.get(order.status)
            shop = Shop.query.get(product.shop)

            prod = product.to_dict(exclude=['description', 'shop', 'dateCreated', 'dateUpdated'])
            prod['category'] = product.cat.name
            prod['gender'] = product.gen.name
            prod['quantity'] = order.quantity
            prod['shop'] = shop.shopName
            prod['status'] = {'id': status.id, 'name': status.name}
            prod['fullname'] = order.fullname
            prod['number'] = order.number
            prod['address'] = order.address
            prod['dateCreated'] = order.dateCreated
            prod['orderID'] = order.id
            prod['total'] = order.quantity * product.price

            products.append(prod)

        return Response(
            status=200,
            data=products
        )
