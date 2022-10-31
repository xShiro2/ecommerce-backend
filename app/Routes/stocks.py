from flask import request
from app import app
from app.models import Shop, Product, QuantityStatus
from flask_login import login_required, current_user
from app.Components.response import Response

@app.route('/api/v1/admin/stocks', methods=['POST', 'GET'])
@login_required
def stocks():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'POST':
        data = request.get_json()
        shop = Shop.query.filter_by(user=current_user.id).first_or_404()
        product = Product.query.filter_by(shop=shop.id, id=data['id']).first_or_404()
        
        if product:
            quantityStatus = QuantityStatus.query.filter_by(product=product.id).first_or_404()

            quantityStatus.quantity = data['quantity']
            quantityStatus.status = data['status']
            quantityStatus.update()

            return Response(
                status=200
            )
        
        return Response(
            status=404
        )
    
    if request.method == 'GET':
        shop = Shop.query.filter_by(user=current_user.id).first_or_404()
        products = Product.query.filter_by(shop=shop.id).all()
        res = []
        if products:
            for product in products:
                quantityStatus = QuantityStatus.query.filter_by(product=product.id).first_or_404()
                dic = quantityStatus.to_dict()
                dic.pop('product')
                dic['productName'] = product.productName
                res.append(dic)

        return Response(
            status=200,
            data=res
        )

@login_required
@app.route('/api/v1/admin/stocks/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        data = request.get_json()
        quantityStatus = QuantityStatus.query.filter_by(id=id).first_or_404()

        if quantityStatus:
            quantityStatus.quantity = data['quantity']
            quantityStatus.status = data['status']
            
            quantityStatus.update()

            res = quantityStatus.to_dict()
            res.pop('product')
            res['productName'] = quantityStatus.prod.productName
            return Response(
                status=200,
                data=res
            )
        return Response(
            status=404
        )




