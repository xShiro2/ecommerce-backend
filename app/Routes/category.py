from flask import request
from app import app
from app.models import Category, SubCategory, Shop
from flask_login import login_required, current_user
from app.Components.response import Response

@app.route('/api/v1/shop/category', methods=['POST', 'DELETE'])
@login_required
def category():
    if current_user.user_type == 'Buyer':
        return Response(
            status=403,
            message="error",
        )
    
    if request.method == 'POST':
        data = request.get_json()

        shop = Shop.query.filter_by(seller_id = current_user.id).first()
        category = Category(
            name = data['name'],
            shop_id = shop.id
        )

        category.create()

        return Response(
                status=201,
                message="success",
            )
        
    if request.method == 'DELETE':
        data = request.get_json()

        shop = Shop.query.filter_by(seller_id = current_user.id).first_or_404()
        
        category = Category.query.filter_by(id=data['id'], shop_id = shop.id).first()
        category.delete()

        return Response(
            status= 200
        )

@app.route('/api/v1/shop/subcategory', methods=['POST', 'DELETE'])
@login_required
def subcategory():
    if current_user.user_type == 'Buyer':
        return Response(
            status=403,
            message="error",
        )
    
    if request.method == 'POST':
        data = request.get_json()

        shop = Shop.query.filter_by(seller_id = current_user.id).first()

        subcategory = SubCategory(
            name = data['name'],
            shop_id = shop.id
        )

        subcategory.create()

        return Response(
                status=201,
                message="success",
            )
        
    if request.method == 'DELETE':
        data = request.get_json()
        
        shop = Shop.query.filter_by(seller_id = current_user.id).first_or_404()
        
        subcategory = SubCategory.query.filter_by(id=data['id'], shop_id = shop.id).first()
        subcategory.delete()

        return Response(
            status= 200
        )


        
