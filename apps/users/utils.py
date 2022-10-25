import os
import secrets
from PIL import Image
from flask import url_for, current_app, abort
from flask_mail import Message
from functools import wraps
from flask_login import current_user
from apps import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/assets/img/profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)

    return picture_fn

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.roles_id == "1":
            return f(*args, **kwargs)
        else:
            abort(401)
    return wrap

def dokter_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.roles_id == "2":
            return f(*args, **kwargs)
        else:
            abort(401)
    return wrap

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='idaikalbar123@gmail.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link: {url_for('users.reset_token', token=token, _external=True) }
If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)