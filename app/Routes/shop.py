from flask import request
from app import app
from app.models import Shop
from flask_login import login_required, current_user
from app.Components.response import Response
from app.Components.image_handler import save_img, delete_img

@app.route('/api/v1/shop', methods=['POST', 'GET'])
@login_required
def shop():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'POST':
        name = request.form['shopName']
        description = request.form['description']
        address = request.form['address']
        image = request.files['image']

        shop = Shop.query.filter_by(user=current_user.id).first()
        if shop:
            if image:
                delete_img(shop.image)
                img_path = save_img(image)
                shop.image = img_path
            
            shop.shopName = name,
            shop.address = address,
            shop.description = description,
            shop.image = img_path

            shop.update()
        else:
            img_path = save_img(image)
            new_shop = Shop(
                shopName =name,
                address = address,
                description = description,
                user = current_user.id,
                image = img_path
            )

            new_shop.create()

        return Response(
            status = 201,
            message ="success",
        )
    
    if request.method == 'GET':
        shop = Shop.query.filter_by(user=current_user.id).first()

        if shop:
            data = shop.to_dict(exclude="image")

            return Response(
                status = 200,
                data=data
            )
        return Response(
            status = 204,
        )


        