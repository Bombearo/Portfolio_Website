import os
import math
import secrets
from PIL import Image
from functools import wraps
from flask import url_for, current_app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_hex(form_picture):
    random_hex = secrets.token_hex(8)
    filename = secure_filename(form_picture.filename)
    _,f_ext = os.path.splitext(filename)
    return random_hex + f_ext

def save_picture(width,height,form_picture,picture_path):
    output_size = (width,height)
    resize_canvas(form_picture,picture_path,width,height)

def save_image(form_picture,pic_type,width,height):
    picture_fn = generate_hex(form_picture)
    picture_path = os.path.join(current_app.root_path,'static\\'+pic_type, picture_fn)
    save_picture(width,height,form_picture,picture_path)
    return picture_fn



def resize_canvas(old_image_path, new_image_path,
                  canvas_width, canvas_height):
    """
    Place one image on another image.

    Resize the canvas of old_image_path and store the new image in
    new_image_path. Center the image on the new canvas.
    """
    im = Image.open(old_image_path)
    im.thumbnail((canvas_width,canvas_height))
    old_width, old_height = im.size

    # Center the image
    x1 = int(math.floor((canvas_width - old_width) / 2))
    y1 = int(math.floor((canvas_height - old_height) / 2))

    mode = im.mode
    if len(mode) == 1:  # L, 1
        new_background = (255)
    if len(mode) == 3:  # RGB
        new_background = (255, 255, 255)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (255, 255, 255, 255)

    newImage = Image.new(mode, (canvas_width, canvas_height), new_background)
    newImage.paste(im, (x1, y1, x1 + old_width, y1 + old_height))
    newImage.save(new_image_path)
