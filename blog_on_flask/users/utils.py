import os
from pathlib import Path

from secrets import token_hex
from PIL import Image
from flask import url_for, current_app


def save_picture(form_picture):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f'{random_hex}{f_ext}'
    picture_path = os.path.join(current_app.root_path, str(Path('static', 'profile_pics')), picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
