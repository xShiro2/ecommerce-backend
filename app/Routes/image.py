from flask import request, send_file
from app import app
from app.Components.image_handler import get_img
from flask_login import current_user
from app.models import Product, Shop

@app.route('/api/v1/images/<id>', methods=['GET'])
def image(id):
    if request.method == 'GET':
        product = Product.query.filter_by(id=id).first()
        if product:
            img = get_img(product.image)
            return send_file(
                img,
                mimetype='image/png'
            )

@app.route('/api/v1/shop/images', methods=['GET'])
def shop_image():
    if request.method == 'GET':
        shop = Shop.query.filter_by(user=current_user.id).first()
        if shop:
            img = get_img(shop.image)
            return send_file(
                img,
                mimetype='image/png'
            )