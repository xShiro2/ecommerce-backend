from flask import request
from app import app, db
from app.models import Shop, Item, Variant
from flask_login import login_required, current_user
from app.Components.response import Response

@app.route('/api/v1/shop', methods=['POST', 'GET', 'DELETE'])
@login_required
def shop():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'POST':
        data = request.get_json()

        shop = Shop.query.filter_by(seller_id=current_user.id).first()
        if shop:
            shop.name = data['name']
            shop.location = data['location']
            shop.description = data['description']
            shop.seller_id = current_user.id
            shop.updated()

            return Response(
                status =  200,
                message = "success",
            )

        else:
            new_shop = Shop(
                name = data['name'],
                location = data['location'],
                description = data['description'],
                seller_id = current_user.id
            )
            new_shop.create()

            return Response(
                status = 201,
                message ="success",
            )
    
    if request.method == 'GET':
        shop = Shop.query.filter_by(seller_id=current_user.id).first_or_404()
        shop_items = Item.query.join(Shop).filter(Shop.seller_id==current_user.id).all()
        
        item_list = {}
        for i, item in enumerate(shop_items):
            variants = Variant.query.filter_by(item_id=item.id).all()
            variant_list = {}
            for var in variants:
                variant_list[var.size] = var.quantity

            att = item.to_dict(exclude="shop_id")
            att['gender'] = item.gen.name
            att['category'] = item.cat.name
        
            item_list[i] = {
                str(item.id) : att,
                "variants": variant_list
            }

        return Response(
            status = 200,
            data =   {
                "shop": shop.to_dict(exclude='seller_id'),
                "items" : item_list,
            }
        )
    


        