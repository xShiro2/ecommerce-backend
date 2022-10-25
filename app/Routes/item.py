from flask import request
from app import app
from app.models import Shop, Item, Variant, Gender, Category
from flask_login import login_required, current_user
from app.Components.response import Response


@app.route('/api/v1/shop/item', methods=['POST', 'GET',  'DELETE'])
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
            category = Category.query.filter_by(name=data['category'], shop_id=shop.id).first()
            item = Item(
                shop_id = shop.id,
                name=data['name'],
                description=data['description'],
                price = data['price'],

                gender = gender.id,
                category = category.id
            )

            item.create()

            variants = data['variants']

            for size in variants.keys():
                var = Variant(item_id=item.id, size=size, quantity=variants[size])
                var.create()

            return Response(
                status=201,
                message="success",
            )
    
    if request.method == 'GET':
        shop  = Shop.query.filter_by(seller_id=current_user.id).first()
        items = Item.query.filter_by(shop_id=shop.id).all()

        res = []
        for item in items:
            variants = Variant.query.filter_by(item_id=item.id).all()
            sizes = []
            quantities=[]
            for variant in variants:
                sizes.append(variant.size)
                quantities.append(variant.quantity)

            res.append({
                'id': item.id,
                'productName': item.name,
                'description': item.description,
                'price': item.price,
                'category': item.cat.name,
                'sizes': sizes,
                'quantity': quantities,
                'gender': item.gen.name
            })

        return Response(
            data=res,
            status=200
        )
    
    if request.method == 'DELETE':
        data = request.get_json()

        item = Item.query.get_or_404(data['item_id'])

        item.delete()

        return Response(
            status=200
        )