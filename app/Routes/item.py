from flask import request
from app import app
from app.models import Shop, ShopItem, Item, Category, SubCategory
from flask_login import login_required, current_user
from app.Components.response import Response


@app.route('/api/v1/shop/item', methods=['POST', 'GET', 'DELETE'])
@login_required
def item():
    if current_user.user_type == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'POST':
        data = request.get_json()

        shop = Shop.query.filter_by(seller_id=current_user.id).first()
        category = Category.query.filter_by(user_id=current_user.id, name=data['category']).first()
        subcategory = SubCategory.query.filter_by(user_id=current_user.id, name=data['subcategory']).first()

        if shop:
            item = Item(
                name=data['name'],
                description=data['description'],
                price = data['price'],
                quantity = data['quantity'],
                category_id = category.id,
                subcategory_id = subcategory.id
            )

            shopItem = ShopItem(
                shop_id = shop.id,
                item=item
            )
            shopItem.create()
            item.create()

            return Response(
                status=201,
                message="success",
            )
    if request.method == 'GET':
        shop = Shop.query.filter_by(seller_id=current_user.id).first()
        if shop:
            items = getItems(shop.id)

            return Response(
                status = 200,
                data = {
                    "items": items
                }
            )

def getItems(shop_id):
    shopItems = ShopItem.query.filter_by(shop_id = shop_id).all()
    item_ids = [item.item_id for item in shopItems]
    items = {}

    for i, id in enumerate(item_ids):
        item = Item.query.get(id)
        items[i] = item.to_dict()
    return items