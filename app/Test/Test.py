from app.models import Sold, User, Shop, Product, Gender, Category, QuantityStatus
from werkzeug.security import generate_password_hash
import os
from PIL import Image
import uuid
import random

DESCRIPTION = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
PATH = 'app/Test/Images'

def createUser(email, password, usertype):
    user = User(
        firstName = "First",
        lastName = "Last",
        email = email,
        password = generate_password_hash(password),
        address = "Test",
        age = 1,
        gender = 1,
        userType = usertype,
    )

    result = user.create()

    if result:
        if user.userType == 'Seller':
            image = getRandomImage()
            shop = Shop(
                user=user.id,
                shopName="Lorem Ipsum Shop",
                address ="Lorem Ipsum, Iloilo",
                description=DESCRIPTION,
                image=save_img(os.path.join(PATH, image))
            )
            shop.create()

        return user.id

def createCategory(id, categoryList):
    shop = Shop.query.filter_by(user=id).first()
    for category in categoryList:
        cat = Category(name=category, shop=shop.id)
        cat.create()

def createProducts(id, num):
    print(f"Creating {num} products...")
    shop = Shop.query.filter_by(user=id).first()
    categoryList = Category.query.filter_by(shop=shop.id).all()
    genderList = Gender.query.all()
    

    for i in range(1, num):
        gender = random.choice(genderList)
        category = random.choice(categoryList)
        image = getRandomImage()

        product = Product(
            shop=shop.id,
            productName= f"Product {i}",
            description = DESCRIPTION,
            price = random.randint(100, 10000),
            image = save_img(os.path.join(PATH, image)),
            gender=gender.id,
            category=category.id
        )

        product.create()

        quantityStatus = QuantityStatus(
            product=product.id,
            quantity = 100,
            status = True
        )

        sold = Sold(
            product=product.id,
            quantity = 0
        )
        sold.create()
        quantityStatus.create()
    
    print("Done!!!")

def getRandomImage():
    images = os.listdir(PATH)
    return random.choice(images)

def save_img(img_path):
    IMAGE_FOLDER = 'IMAGE_FOLDER'
    WIDTH = 800

    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    path = IMAGE_FOLDER + "/" + str(uuid.uuid4()) + '.png'

    im = Image.open(img_path)
    newHeight = int(WIDTH * im.height/im.width)
    im = im.resize((WIDTH, newHeight), resample=Image.LANCZOS)
    im.save(path, 'PNG')

    return path

def start():
    user = createUser(
        email="test@gmail.com",
        password="test",
        usertype='Seller'
    )

    createCategory(user, 
        ["Jeans", "T-Shirt", "Shorts", "Pants", "Polo", "Shoes", "Dress"]
    )

    createProducts(user, 100)


      

