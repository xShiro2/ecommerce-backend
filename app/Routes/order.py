from app import app, db
from flask_login import login_required, current_user
from flask import request
from app.Components.response import Response
from app.models import Order, Shop, Product, OrderStatus

@app.route('/api/v1/admin/orders', methods=['GET'])
@login_required
def orders():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )
    
    if request.method == 'GET':
        shop = Shop.query.filter_by(user=current_user.id).first()
        orders = Order.query.order_by(Order.dateCreated.desc()).join(Product.query.filter_by(shop=shop.id)).all()
        
        data = []
        for order in orders:
            detail = {}
            status = OrderStatus.query.get(order.status)
            product = Product.query.get(order.product)
            detail['id'] = order.id
            detail['productID'] = product.id
            detail['productName'] = product.productName
            detail['price'] = product.price
            detail['quantity'] = order.quantity
            detail['totalprice'] = order.quantity * product.price
            detail['dateCreated'] = order.dateCreated
            detail['buyer'] = {"fullname": order.fullname, "number": order.number, "address": order.address}
            detail['status'] = status.name
            data.append(detail)

        return Response(
            status=200,
            data= data
        )

@app.route('/api/v1/admin/order/status', methods=["POST"])
@login_required
def orderStatus():
    if request.method == "POST":
        data = request.get_json()
        order = Order.query.get(data['id'])
        status = OrderStatus.query.filter_by(name=data['status']).first()
        order.status = status.id
        order.update()

        return Response(
            status=200
        )