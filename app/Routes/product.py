from flask import request
from app import app
from app.models import Shop, Product, Gender, Category, QuantityStatus
from flask_login import login_required, current_user
from app.Components.response import Response

@app.route('/api/v1/admin/product', methods=['POST', 'GET'])
@login_required
def products():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'POST':
        data = request.get_json()

        shop = Shop.query.filter_by(user=current_user.id).first_or_404()
        if shop:
            gender = Gender.query.filter_by(id=data['gender']).first()
            category = Category.query.filter_by(id=data['category'], shop=shop.id).first()
            product = Product(
                shop = shop.id,
                productName=data['productName'],
                description=data['description'],
                price = data['price'],

                gender = gender.id,
                category = category.id
            )

            product.create()

            quantityStatus = QuantityStatus(
                product=product.id,
                quantity = 0,
                status = False
            )

            quantityStatus.create()

            return Response(
                status=201,
                message="success",
            )
    
    if request.method == 'GET':
        shop  = Shop.query.filter_by(user=current_user.id).first()
        products = Product.query.filter_by(shop=shop.id).all()

        res = []
        for product in products:
            prod = product.to_dict()
            prod['category'] = product.cat.name
            prod['gender'] = product.gen.name
            
            res.append(prod)

        return Response(
            data=res,
            status=200
        )

@app.route('/api/v1/admin/product/<id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def product(id):
    if request.method == 'DELETE':
        shop = Shop.query.filter_by(user=current_user.id).first()
        product = Product.query.filter_by(id=id, shop=shop.id).first()
        
        if product:
            quantityStatus = QuantityStatus.query.filter_by(product=product.id).first()
            quantityStatus.delete()
            
            product.delete()

            return Response(
                status=200
            )

        return Response(
                status=404
        )
    
    if request.method == 'GET':
        shop = Shop.query.filter_by(user=current_user.id).first()
        product = Product.query.filter_by(id=id, shop=shop.id).first()
        
        if product:
            prod = product.to_dict()
            prod['category'] = product.cat.name
            prod['gender'] = product.gen.name
            return Response(
                status=200,
                data=prod
            )
    
    if request.method == 'POST':
        data = request.get_json()

        shop = Shop.query.filter_by(user=current_user.id).first()
        product = Product.query.filter_by(id=id, shop=shop.id).first()

        if product:
            gender = Gender.query.filter_by(id=data['gender']).first()
            category = Category.query.filter_by(id=data['category'], shop=shop.id).first()

            product.productName = data['productName']
            product.description = data['description']
            product.price = data['price']
            product.gender = gender.id
            product.category = category.id

            product.update()

            return Response(
                status=201
            )