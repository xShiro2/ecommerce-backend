from math import prod
from flask import request
from app import app
from app.models import Shop, Product, Gender, Category
from flask_login import login_required, current_user
from app.Components.response import Response


@app.route('/api/v1/admin/product', methods=['POST', 'GET',  'DELETE'])
@login_required
def item():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'POST':
        data = request.get_json()

        shop = Shop.query.filter_by(user=current_user.id).first_or_404()
        
        if shop:
            gender = Gender.query.filter_by(name=data['gender']).first()
            category = Category.query.filter_by(name=data['category'], shop=shop.id).first()
            product = Product(
                shop = shop.id,
                productName=data['productName'],
                description=data['description'],
                price = data['price'],
                quantity = data['quantity'],

                gender = gender.id,
                category = category.id
            )

            product.create()

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
            prod['category'] = Category.query.get_or_404(product.category).name
            prod['gender'] = Gender.query.get_or_404(product.gender).name
            
            res.append(prod)

        return Response(
            data=res,
            status=200
        )