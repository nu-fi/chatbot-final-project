import secrets
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, current_app
from apps.models import Categoryn, News
from apps import db
from apps.news.forms import NewsForm, CategoryForm
from flask_login import current_user, login_required
import os
import secrets
from slugify import slugify

news = Blueprint('news', __name__)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/assets/img/news', picture_fn)
        
    form_picture.save(picture_path)
    return picture_fn 

@news.route("/admin/berita")
def news_admin():
    news = News.query.all()
    cat = Categoryn.query.all()
    return render_template('users/admin/news/berita_admin.html', title='Berita', news=news, cat=cat)

@news.route("/admin/berita/new", methods=['GET', 'POST'])
@login_required
def new_news():
    form = NewsForm()
    cat = Categoryn.query.all()
    cat_list = [( c.id, c.name) for c in cat]
    form.category.choices = cat_list
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)

        news = News(title=form.title.data, content=form.content.data, author=current_user, category_id=form.category.data, image_news=picture_file, slug = slugify(request.form.get("title")))
        db.session.add(news)
        db.session.commit()
        flash('Your News has been added', 'primary')
        return redirect(url_for('news.news_admin'))
    return render_template('users/admin/news/berita_baru.html', title='Tambah Berita', legend='Tambah Berita', form=form)


@news.route("/admin/berita/<int:berita_id>/update", methods=['GET', 'POST'])
@login_required
def news_update(berita_id):
    news = News.query.get_or_404(berita_id)
    cat = Categoryn.query.all()
    cat_list = [( c.id, c.name) for c in cat]
    if news.author != current_user:
        abort(403)
    form =NewsForm()
    form.category.choices = cat_list
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            news.image_news = picture_file
        news.title = form.title.data
        news.content = form.content.data
        news.category_id = form.category.data
        news.slug = slugify(request.form.get("title"))
        db.session.commit()
        flash('Your News has been updated!', 'success')
        return redirect(url_for('news.news_admin'))
    elif request.method == 'GET':
        form.title.data = news.title
        form.content.data = news.content
        form.picture.data = news.image_news

    image_file = url_for('static', filename='assets/img/news/' + news.image_news)
    return render_template('users/admin/news/berita_baru.html', title='Update Berita', legend='Update Berita', form=form, image_file=image_file)

@news.route("/admin/berita/<int:berita_id>/delete", methods=['POST'])
@login_required
def news_delete(berita_id):
    news = News.query.get_or_404(berita_id)
    # if artikel.author != current_user:
    #     abort(403)
    db.session.delete(news)
    db.session.commit()
    flash('Your News has been deleted!', 'danger')
    return redirect(url_for('news.news_admin'))

@news.route("/admin/kategori-berita", methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        cat = Categoryn(name=form.name.data, slug = slugify(request.form.get("name")))
        db.session.add(cat)
        db.session.commit()
        flash('Your Category News has been added!', 'primary')
        return redirect(url_for('news.new_category'))

    cat = Categoryn.query.all()
    return render_template('users/admin/news/kategori_berita.html', form=form, cat=cat, title='Kategori Berita')

@news.route("/admin/kategori-berita/<int:category_id>/delete", methods=['POST'])
@login_required
def cat_delete(category_id):
    cat = Categoryn.query.get_or_404(category_id)
    db.session.delete(cat)
    db.session.commit()
    flash('Your Category News has been deleted!', 'danger')
    return redirect(url_for('news.new_category'))

@news.route("/admin/kategori-berita/<int:category_id>/update", methods=['GET', 'POST'])
@login_required
def cat_update(category_id):
    cat = Categoryn.query.get_or_404(category_id)
    form =CategoryForm()
    if form.validate_on_submit():
        cat.name = form.name.data
        cat.slug = slugify(request.form.get("name"))
        db.session.commit()
        flash('Your Category News has been updated!', 'success')
        return redirect(url_for('news.new_category'))
    elif request.method == 'GET':
        form.name.data = cat.name

    return render_template('users/admin/news/kategori_berita.html', title='Update Kategori', legend='Update Kategori', form=form)