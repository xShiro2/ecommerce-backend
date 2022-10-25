from flask import request
from app import app, db
from app.models import Category, Shop
from flask_login import login_required, current_user
from app.Components.response import Response

@login_required
@app.route('/api/v1/shop/category', methods=['POST', 'GET', 'DELETE'])
def category():
    if current_user.user_type == 'Buyer':
        return Response(
            status=403,
            message="error",
        )
    
    if request.method == 'POST':
        data = request.get_json()
        shop  = Shop.query.filter_by(seller_id=current_user.id).first()
        
        category = Category(
            shop_id = shop.id,
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
        shop  = Shop.query.filter_by(seller_id=current_user.id).first()
        categories = Category.query.filter_by(shop_id=shop.id).all()

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