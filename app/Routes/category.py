from flask import request
from app import app, db
from app.models import Category, Shop, Gender
from flask_login import login_required, current_user
from app.Components.response import Response

@login_required
@app.route('/api/v1/shop/category', methods=['POST', 'GET'])
def category():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )
    
    if request.method == 'POST':
        data = request.get_json()
        shop  = Shop.query.filter_by(user=current_user.id).first()

        if Category.query.filter_by(name = data['categoryName'], shop = shop.id).first():
            return Response(
                status=409,
                message="error",
            )
        
        category = Category(
            shop = shop.id,
            name = data['categoryName']
        )

        category.create()

        return Response(
            data = {
                'id': category.id,
                'categoryName': category.name,
                'dateCreated': category.dateCreated,
                'dateUpdated': category.dateUpdated,
            },
            status=201
        )
    
    if request.method == 'GET':
        shop  = Shop.query.filter_by(user=current_user.id).first()
        categories = Category.query.filter_by(shop=shop.id).all()

        res = []
        for category in categories:
            res.append({
                'id': category.id,
                'categoryName': category.name,
                'dateCreated': category.dateCreated,
                'dateUpdated': category.dateUpdated,
            })
        
        return Response(
            data=res, 
            status=200
        )
    
@login_required
@app.route('/api/v1/shop/category/<id>', methods=['DELETE'])
def delete(id):
    if request.method == 'DELETE':
        category = Category.query.get_or_404(id)
        category.delete()

        return Response(
            status=200
        )

@login_required
@app.route('/api/v1/product/category', methods=['GET'])
def product_category():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'GET':
        shop  = Shop.query.filter_by(user=current_user.id).first()
        categories = Category.query.filter_by(shop=shop.id).all()
        genders = Gender.query.all()

        categoryList = []
        genderList = []

        for category in categories:
            categoryList.append({
                'id': category.id,
                'categoryName': category.name
            })

        for gender in genders:
            genderList.append({
                'id': gender.id,
                'gender': gender.name
            })
        
        return Response(
            data= {
                'categoryList': categoryList,
                'genderList': genderList
            },
            status=200
        )