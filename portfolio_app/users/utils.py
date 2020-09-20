import os
import secrets
from PIL import Image
from functools import wraps
from flask import url_for, current_app

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_hex(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    return random_hex + f_ext

def save_picture(width,height,form_picture,picture_path):
    output_size = (width,height)
    i = Image.open(form_picture)
    i.thumbnail (output_size)
    i.save(picture_path)

def save_image(form_picture,pic_type,width,height):
    picture_fn = generate_hex(form_picture)
    picture_path = os.path.join(current_app.root_path,'static\\'+pic_type, picture_fn)
    save_picture(width,height,form_picture,picture_path)
    return picture_fn
