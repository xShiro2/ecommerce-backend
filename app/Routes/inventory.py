from app import app, db
from flask_login import login_required, current_user
from flask import request
from app.Components.response import Response
from app.models import Shop, Product, QuantityStatus, Sold

@app.route('/api/v1/admin/inventory', methods=['GET'])
@login_required
def inventory():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )
    
    if request.method == 'GET':
        shop = Shop.query.filter_by(user=current_user.id).first()

        products = Product.query.filter_by(shop=shop.id).all()

        res = []
        for product in products:
            prod = product.to_dict(exclude=['category', 'gender', 'dateCreated', 'dateUpdated', 'description'])
            prod['quantity'] = QuantityStatus.query.filter_by(product=product.id).first().quantity
            prod['sold'] = Sold.query.filter_by(product=product.id).first().quantity
            prod['total'] = Sold.query.filter_by(product=product.id).first().quantity * product.price
            res.append(prod)

        return Response(
            data=res,
            status=200
        )