from flask import request
from app import app
from app.models import Shop, Product, Gender, Category, QuantityStatus, User
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
            try:
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
            except Exception as e:
                print(e)
                return Response(
                    status=500
                )
    
    if request.method == 'GET':
        shop  = Shop.query.filter_by(user=current_user.id).first()
        if not shop:
            return Response(
                status=404,
            )
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

@app.route('/api/v1/products', methods=['GET'])
def getproducts():
    minNumber = 12
    if request.method == 'GET':
        prod_filter = request.args.get('filter')
        page = request.args.get('page')
        keyword = request.args.get('keyword')

        if page:
            page = int(page)
        else:
            page = 1

        prod_len = Product.query.join(QuantityStatus.query.filter_by(status=True)).all()
        products = Product.query.join(QuantityStatus.query.filter_by(status=True)).paginate(page=page, per_page=minNumber)
        
        if prod_filter:
            gender = []
            if prod_filter == 'men':
                gender = Gender.query.filter_by(name='Male').first()
            if prod_filter == 'women':
                gender = Gender.query.filter_by(name='Female').first()
            if prod_filter == 'kids':
                gender = Gender.query.filter_by(name='Kids').first()
            if prod_filter == 'best':
                pass
            if prod_filter == 'featured':
                pass
            if prod_filter == 'latest':
                products = Product.query.order_by(Product.dateCreated.desc()).join(QuantityStatus.query.filter_by(status=True)).paginate(page=page, per_page=minNumber)
                prod_len = Product.query.order_by(Product.dateCreated.desc()).all()
            if gender:
                products = Product.query.filter_by(gender=gender.id).join(QuantityStatus.query.filter_by(status=True)).paginate(page=page, per_page=minNumber)
                prod_len = Product.query.filter_by(gender=gender.id).join(QuantityStatus.query.filter_by(status=True)).all()
        else:
            pass

        if keyword:
            products = Product.query.filter(Product.productName.like('%'+keyword+'%')).paginate(page=page, per_page=minNumber)
            prod_len = Product.query.filter(Product.productName.like('%'+keyword+'%')).all()

        prods=[]
        for product in products:
            quantityStatus = QuantityStatus.query.filter_by(product=product.id).first()
            prod = product.to_dict(exclude='image')
            prod['category'] = product.cat.name
            prod['gender'] = product.gen.name
            prod['quantity'] = quantityStatus.quantity

            prods.append(prod)

        return Response(
            data=prods,
            message=len(prod_len),
            status=200
        )

        
@app.route('/api/v1/product/<id>', methods=['GET'])
def displayproduct(id):
    if request.method == 'GET':
        product = Product.query.filter_by(id=id).first()
        quantityStatus = QuantityStatus.query.filter_by(product=product.id).first()
        shop = Shop.query.get(product.shop)
        user = User.query.get(shop.user)

        prod = product.to_dict(exclude='image')
        prod['category'] = product.cat.name
        prod['gender'] = product.gen.name
        prod['quantity'] = quantityStatus.quantity
        prod['seller'] = user.firstName +" "+ user.lastName
        prod['sellerAddress'] = user.address

        return Response(
            data=prod,
            status=200
        )
