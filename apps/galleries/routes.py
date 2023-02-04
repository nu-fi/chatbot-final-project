import secrets
from turtle import title
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, current_app
from apps.models import Gallery, Images_Gallery
from apps import db
from apps.galleries.forms import GalleryForm, ImageForm
from flask_login import current_user, login_required
import os
import secrets
from slugify import slugify

galleries = Blueprint('galleries', __name__)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/assets/img/galleries', picture_fn)
        
    form_picture.save(picture_path)
    return picture_fn 

@galleries.route("/admin/kategori-galeri", methods=['GET', 'POST'])
@login_required
def new_gallery():
    form = GalleryForm()
    galls = Gallery.query.all()
    if form.validate_on_submit():
        gall = Gallery(title=form.title.data, author=current_user, slug = slugify(request.form.get("title")))
        db.session.add(gall)
        db.session.commit()
        flash('Your Image Gallery has been added!', 'primary')

        return redirect(url_for('galleries.new_gallery'))
        
    return render_template('users/admin/galleries/galeri_kategori.html', form=form, galls=galls, title='Kategori Galeri')

@galleries.route("/admin/kategori-galeri/<int:gal_id>/delete", methods=['POST'])
@login_required
def gal_delete(gal_id):
    gal = Gallery.query.get_or_404(gal_id)
    db.session.delete(gal)
    db.session.commit()
    flash('Your Image Gallery has been deleted!', 'danger')
    return redirect(url_for('galleries.new_gallery'))

@galleries.route("/admin/kategori-galeri/<int:gal_id>/update", methods=['GET', 'POST'])
@login_required
def gal_update(gal_id):
    gal = Gallery.query.get_or_404(gal_id)
    form = GalleryForm()
    if form.validate_on_submit():
        gal.title = form.title.data
        gal.slug = slugify(request.form.get("title"))
        db.session.commit()
        flash('Your Gallery has been updated!', 'success')
        return redirect(url_for('galleries.new_gallery', gal_id=gal.id))
    elif request.method == 'GET':
        form.title.data = gal.title

    return render_template('users/admin/galleries/galeri_kategori.html', title='Update Kategori', legend='Update Kategori', form=form)


@galleries.route("/admin/galeri", methods=['GET', 'POST'])
@login_required
def new_image():
    gall = Gallery.query.all()
    gall_list = [( g.id, g.title) for g in gall]
    form = ImageForm()
    form.gallery.choices = gall_list
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)

        image = Images_Gallery(image_gallery=picture_file, gallery_id=form.gallery.data, author=current_user, description=form.description.data)
        db.session.add(image)
        db.session.commit()
        flash('Image has been added!', 'primary')
        return redirect(url_for('galleries.new_image'))
    imgs = Images_Gallery.query.all()
    return render_template('users/admin/galleries/upload_image.html', title='Gambar Galeri', legend='Tambah Gambar', form=form, imgs =imgs)

@galleries.route("/admin/image/<int:img_id>/update", methods=['GET', 'POST'])
@login_required
def img_update(img_id):
    img = Images_Gallery.query.get_or_404(img_id)
    gal = Gallery.query.all()
    gal_list = [( c.id, c.title) for c in gal]
   
    form = ImageForm()
    form.gallery.choices = gal_list
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            img.image_gallery = picture_file
        img.gallery_id = form.gallery.data
        img.description = form.description.data
        db.session.commit()
        flash('Your img has been updated!', 'success')
        return redirect(url_for('galleries.new_image'))
    elif request.method == 'GET':
        form.description.data = img.description
        form.gallery.data = img.gallery.title
        form.picture.data = img.image_gallery

    return redirect(url_for('galleries.new_image'))

@galleries.route("/admin/image/<int:img_id>/delete", methods=['POST'])
@login_required
def img_delete(img_id):
    news = Images_Gallery.query.get_or_404(img_id)
    # if artikel.author != current_user:
    #     abort(403)
    db.session.delete(news)
    db.session.commit()
    flash('Your Image has been deleted!', 'danger')
    return redirect(url_for('galleries.new_image'))