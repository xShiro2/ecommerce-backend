from flask import request
from app import app
from app.models import Category, SubCategory
from flask_login import login_required, current_user
from app.Components.response import Response

@app.route('/api/v1/category', methods=['POST', 'GET', 'DELETE'])
@login_required
def category():
    if current_user.user_type == 'Buyer':
        return Response(
            status=403,
            message="error",
        )
    
    if request.method == 'POST':
        data = request.get_json()

        category = Category(
            name = data['category'],
            user_id = current_user.id
        )

        subcategory = SubCategory(
            name = data['subcategory'],
            user_id = current_user.id
        )

        category.create()
        subcategory.create()

        return Response(
                status=201,
                message="success",
            )
        
