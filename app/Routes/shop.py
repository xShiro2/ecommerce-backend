from flask import request
from app import app, db
from app.models import Shop, Item, Quantity, Size
from flask_login import login_required, current_user
from app.Components.response import Response

@app.route('/api/v1/shop', methods=['POST', 'GET', 'DELETE'])
@login_required
def shop():
    if current_user.user_type == 'Buyer':
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
            db.session.commit()

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
            sizes = Size.query.filter_by(item_id=item.id).all()
            quantities = {}
            for size in sizes:
                quantities[size.value] = Quantity.query.filter_by(size_id=size.id).first().value

            item_list[i] = {
                "item": item.to_dict(),
                "size": quantities
            }
            
        return Response(
            status = 200,
            data =   {
                "shop": shop.to_dict(),
                "items" : item_list,
            }
        )
    


        