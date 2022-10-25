from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, current_app
from apps.models import Article, Category
from apps import db
from apps.articles.forms import ArticleForm, CategoryForm
from flask_login import current_user, login_required
import os
import secrets
from slugify import slugify

articles = Blueprint('articles', __name__)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/assets/img/articles', picture_fn)
        
    form_picture.save(picture_path)
    return picture_fn 

@articles.route("/admin/artikel")
def article_admin():
    articles=Article.query.order_by(Article.date_posted.desc())
    cat = Category.query.all()
    return render_template('users/admin/articles/artikel_admin.html', title='Artikel', articles=articles, cat=cat)

@articles.route("/admin/artikel/new", methods=['GET', 'POST'])
@login_required
def new_article():
    form = ArticleForm()
    cat = Category.query.all()
    cat_list = [( c.id, c.name) for c in cat]
    form.category.choices = cat_list
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        article = Article(title=form.title.data, content=form.content.data, author=current_user, category_id=form.category.data, image_article=picture_file, slug = slugify(request.form.get("title")))
        db.session.add(article)
        db.session.commit() 
        flash('Your Article has been added', 'primary')
        return redirect(url_for('articles.article_admin'))
    return render_template('users/admin/articles/create_article.html', title='Tambah Artikel', legend='Tambah Artikel', form=form)

@articles.route("/admin/artikel/<int:artikel_id>/update", methods=['GET', 'POST'])
@login_required
def article_update(artikel_id):
    artikel = Article.query.get_or_404(artikel_id)
    cat = Category.query.all()
    cat_list = [( c.id, c.name) for c in cat]
    if artikel.author != current_user:
        abort(403)
    form =ArticleForm()
    form.category.choices = cat_list
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            artikel.image_article = picture_file
        artikel.title = form.title.data
        artikel.content = form.content.data
        artikel.category_id = form.category.data
        artikel.slug = slugify(request.form.get("title"))
        db.session.commit()
        flash('Your Article has been updated!', 'success')
        return redirect(url_for('articles.article_admin'))
    elif request.method == 'GET':
        form.title.data = artikel.title
        form.content.data = artikel.content
        form.category.data = artikel.category
        form.picture.data = artikel.image_article

    image_file = url_for('static', filename='assets/img/articles/' + artikel.image_article)
    return render_template('users/admin/articles/create_article.html', title='Update Artikel', legend='Update Artikel', form=form, image_file=image_file)

@articles.route("/artikel/<int:artikel_id>/delete", methods=['POST'])
@login_required
def article_delete(artikel_id):
    artikel = Article.query.get_or_404(artikel_id)
    # if artikel.author != current_user:
    #     abort(403)
    db.session.delete(artikel)
    db.session.commit()
    flash('Your Article has been deleted!', 'danger')
    return redirect(url_for('articles.article_admin'))

@articles.route("/admin/kategori-artikel", methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        cat = Category(name=form.name.data, slug = slugify(request.form.get("name")))
        db.session.add(cat)
        db.session.commit()
        flash('Your Category Article has been added!', 'primary')
        return redirect(url_for('articles.new_category'))

    cat = Category.query.all()
    return render_template('users/admin/articles/kategori_artikel.html', form=form, cat=cat, title='Kategori Artikel')

@articles.route("/admin/kategori-artikel/<int:category_id>/delete", methods=['POST'])
@login_required
def cat_delete(category_id):
    cat = Category.query.get_or_404(category_id)
    db.session.delete(cat)
    db.session.commit()
    flash('Your Category Article has been deleted!', 'danger')
    return redirect(url_for('articles.new_category'))

@articles.route("/admin/kategori-artikel/<int:category_id>/update", methods=['GET', 'POST'])
@login_required
def cat_update(category_id):
    cat = Category.query.get_or_404(category_id)
    form =CategoryForm()
    if form.validate_on_submit():
        cat.name = form.name.data
        cat.slug = slugify(request.form.get("name"))
        db.session.commit()
        flash('Your Category Article has been updated!', 'success')
        return redirect(url_for('articles.new_category'))
    elif request.method == 'GET':
        form.name.data = cat.name

    return render_template('users/admin/articles/kategori_artikel.html', title='Update Kategori', legend='Update Kategori', form=form)
