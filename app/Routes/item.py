from flask import request
from app import app
from app.models import Shop, Item, Size, Quantity, Gender, Category
from flask_login import login_required, current_user
from app.Components.response import Response


@app.route('/api/v1/shop/item', methods=['POST',  'DELETE'])
@login_required
def item():
    if current_user.user_type == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'POST':
        data = request.get_json()

        shop = Shop.query.filter_by(seller_id=current_user.id).first_or_404()
        
        if shop:
            gender = Gender.query.filter_by(name=data['gender']).first()
            category = Category.query.filter_by(name=data['category']).first()
            item = Item(
                shop_id = shop.id,
                name=data['name'],
                description=data['description'],
                price = data['price'],

                gender_id = gender.id,
                category_id = category.id
            )

            item.create()

            sizes = data['sizes']

            for size in sizes.keys():
                s = Size(item_id=item.id, value=size)
                s.create()

                quantity = Quantity(size_id=s.id, value=sizes[size])
                quantity.create()

            return Response(
                status=201,
                message="success",
            )
    
    if request.method == 'DELETE':
        data = request.get_json()

        item = Item.query.get_or_404(data['item_id'])

        item.delete()

        return Response(
            status=200
        )