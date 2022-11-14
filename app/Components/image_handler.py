import os
from PIL import Image

IMAGE_FOLDER = 'IMAGE_FOLDER/'
WIDTH = 800

def save_img(img):
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    path = IMAGE_FOLDER + img.filename + '.png'

    im = Image.open(img.stream)
    newHeight = int(WIDTH * im.height/im.width)
    im = im.resize((WIDTH, newHeight), resample=Image.LANCZOS)
    im.save(path, 'PNG')

    return img.filename

def delete_img(img):
    path = IMAGE_FOLDER + img + '.png'
    os.remove(path)

def get_img(img):
    path = IMAGE_FOLDER + img + '.png'
    img = open(path, 'rb')
    return img