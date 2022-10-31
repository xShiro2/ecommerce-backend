from flask import request
from app import app
from app.models import Shop, Product, Gender, Category, QuantityStatus
from flask_login import login_required, current_user
from app.Components.response import Response
from app.Components.image_handler import save_img, delete_img

@app.route('/api/v1/admin/product', methods=['POST', 'GET'])
@login_required
def products():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'POST':
        productName = request.form['productName']
        description = request.form['description']
        price = request.form['price']
        gender_id = request.form['gender']
        category_id = request.form['category']

        shop = Shop.query.filter_by(user=current_user.id).first_or_404()
        if shop:
            img_path = save_img(request.files['image'])
            gender = Gender.query.filter_by(id=gender_id).first()
            category = Category.query.filter_by(id=category_id, shop=shop.id).first()
            product = Product(
                shop = shop.id,
                productName=productName,
                description=description,
                price = price,
                image = img_path,
                gender = gender.id,
                category = category.id
            )

            product.create()

            quantityStatus = QuantityStatus(
                product=product.id,
                quantity = 0,
                status = False
            )

            quantityStatus.create()

            return Response(
                status=201,
                message="success",
            )
    
    if request.method == 'GET':
        shop  = Shop.query.filter_by(user=current_user.id).first()
        products = Product.query.filter_by(shop=shop.id).all()

        res = []
        for product in products:
            prod = product.to_dict()
            prod['category'] = product.cat.name
            prod['gender'] = product.gen.name
            
            res.append(prod)

        return Response(
            data=res,
            status=200
        )

@app.route('/api/v1/admin/product/<id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def product(id):
    if request.method == 'DELETE':
        shop = Shop.query.filter_by(user=current_user.id).first()
        product = Product.query.filter_by(id=id, shop=shop.id).first()
        
        if product:
            delete_img(product.image)
            quantityStatus = QuantityStatus.query.filter_by(product=product.id).first()
            quantityStatus.delete()
            
            product.delete()
            
            return Response(
                status=200
            )

        return Response(
                status=404
        )
    
    if request.method == 'GET':
        shop = Shop.query.filter_by(user=current_user.id).first()
        product = Product.query.filter_by(id=id, shop=shop.id).first()
        
        if product:
            prod = product.to_dict()
            prod['category'] = product.cat.name
            prod['gender'] = product.gen.name
            return Response(
                status=200,
                data=prod
            )
    
    if request.method == 'POST':
        productName = request.form['productName']
        description = request.form['description']
        price = request.form['price']
        gender_id = request.form['gender']
        category_id = request.form['category']
        image = request.files.get('image')

        shop = Shop.query.filter_by(user=current_user.id).first()
        product = Product.query.filter_by(id=id, shop=shop.id).first()

        if product:
            if image:
                delete_img(product.image)
                img_path = save_img(image)
                product.image = img_path
            
            gender = Gender.query.filter_by(id=gender_id).first()
            category = Category.query.filter_by(id=category_id, shop=shop.id).first()

            product.productName = productName
            product.description = description
            product.price = price
            product.gender = gender.id
            product.category = category.id

            product.update()

            return Response(
                status=201
            )