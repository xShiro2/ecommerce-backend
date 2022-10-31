import os
from PIL import Image

IMAGE_FOLDER = 'IMAGE_FOLDER'

def save_img(img):
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    path = IMAGE_FOLDER + "/" + img.filename + '.png'
    im = Image.open(img.stream)
    im.save(path, 'PNG')

    return path

def delete_img(img_path):
    os.remove(img_path)

def get_img(img_path):
    img = open(img_path, 'rb')
    return img