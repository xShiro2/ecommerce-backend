from flask import request, send_file
from app import app
from app.Components.image_handler import get_img
from app.models import Product

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