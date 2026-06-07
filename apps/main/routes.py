from flask import Blueprint, render_template, request, url_for, jsonify, flash, redirect, current_app, send_from_directory, abort
from apps.chat import get_response
from apps.models import Article, Images_Gallery, News, Gallery, Files_Public, Category, Categoryn, Message, User, DataDokter, TempatPraktik
from apps import db, mail
from flask_mail import Message as Mess
from apps.main.forms import ContactForm, SearchForm
import os
from flask_cors import cross_origin
from sqlalchemy import or_

main = Blueprint('main', __name__)

@main.errorhandler(404)
def page_not_found(error):
   return render_template('error/404.html', title = '404'), 404

@main.route("/predict", methods=['POST'])
@cross_origin(origins=['http://127.0.0.1:5000/'])
def predict():
    text = request.get_json().get("message")
    if len(text) > 100:
        message = {"answer": "Maaf, permintaan Anda memiliki terlalu banyak karakter untuk saya proses..."}
        mess = Message(question=text)
        db.session.add(mess)
        db.session.commit()
        return jsonify(message)

    response = get_response(text)
    message = {"answer": response}

    if response == "Maaf, saya tidak mengerti pertanyaan anda...":
        mess = Message(question=text)
        db.session.add(mess)
        db.session.commit()
    else:
        mess = Message(question=text, status_data=True, response=response)
        db.session.add(mess)
        db.session.commit()

    return jsonify(message)

@main.route("/", methods=['GET', 'POST'])
@main.route("/beranda", methods=['GET', 'POST'])
def home():
    artikel_terbaru = Article.query.order_by(Article.date_posted.desc()).first()
    artikel = Article.query.filter(Article.id < artikel_terbaru.id).limit(3)
    berita = News.query.order_by(News.date_posted.desc()).limit(2)
    berita_terbaru = News.query.order_by(News.date_posted.desc()).limit(2)
    gall = Images_Gallery.query.order_by(Images_Gallery.date_posted.desc()).limit(3)

    form = SearchForm()
    dokters = DataDokter.query

    data_tp = TempatPraktik.query
    if form.validate_on_submit():
        searched = form.searched.data
        dokters = dokters.filter(or_(DataDokter.nama_lengkap.like('%' + searched + '%'), TempatPraktik.kota_praktik.like('%' + searched + '%')))
        dokters = dokters.order_by(DataDokter.nama_lengkap.desc()).all()
        return redirect(url_for('main.search'))
        

    return render_template('main/home.html', title="Beranda", artikel=artikel, artikel_terbaru=artikel_terbaru, berita=berita, berita_terbaru=berita_terbaru, gall=gall, form=form, data_tp=data_tp)

@main.route("/profile")
def profile():
    return render_template('main/profile.html', title="Profil Organisasi")

@main.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    dokters = DataDokter.query
    data_tp = TempatPraktik.query
    if form.validate_on_submit():
        searched = form.searched.data
        dokters = dokters.filter(or_(DataDokter.nama_lengkap.like('%' + searched + '%'), TempatPraktik.kota_praktik.like('%' + searched + '%')))
        dokters = dokters.order_by(DataDokter.nama_lengkap.desc()).all()
        return render_template('main/search.html', title="Cari Dokter", dokters=dokters, form=form, data_tp=data_tp)
    return render_template('main/search.html', title="Cari Dokter", dokters=dokters, form=form, data_tp=data_tp)

@main.route("/kata-sambutan")
def kata_sambutan():
    return render_template('main/kata_sambutan.html', title="Sambutan Ketua")

@main.route("/kontak", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email_sender = form.email.data
        message = form.message.data
        subject = form.subject.data
        msg_sender = Mess('Pesan ' + subject + ' Telah Diterima', sender=email_sender, recipients=[email_sender])
        msg_sender.body = f''' Pesan anda yang berisi: {message} telah diterima.
Terima kasih atas pesan yang telah diberikan. Mohon menunggu sebentar, kami akan menjawab pesan anda dengan segera.
    '''
        mail.send(msg_sender)

        msg_idaikb = Mess('Pesan ' + subject + ' Telah Diterima', sender=email_sender, recipients=['idaikalbar123@gmail.com'])
        msg_idaikb.body = f''' Anda memiliki pesan baru dari {email_sender} yang berisi: {message} telah diterima.
Mohon untuk menjawab pesan dengan segera.
    '''
        mail.send(msg_idaikb)
        flash('Pesan untuk email telah diterima. Terima Kasih.', 'info')
        return redirect(url_for('main.contact'))
    return render_template('main/kontak.html', title='Kontak Kami', form=form)

@main.route("/stunting")
def stunting():
    return render_template('main/stunting.html', title='Tentang Stunting')

# @main.route("/jurnal")
# def journal():
#     return url_for('https://a-jhr.com/a-jhr')

@main.route("/berkas/download/<slug>")
def file_download(slug):
    file = Files_Public.query.filter_by(slug=slug).first()
    path = os.path.join(current_app.root_path, 'static/assets/files/public')
    return send_from_directory(path, file.filename)

@main.route("/artikel")
def article():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.date_posted.desc()).paginate(page=page, per_page=4)
    next_url = url_for('main.article', page=articles.next_num) if articles.has_next else None
    prev_url = url_for('main.article', page=articles.prev_num) if articles.has_prev else None

    # if articles.next_url or  articles.prev_url == None:
    #     abort(404)

    return render_template('main/articles/artikel.html', title='Artikel', articles=articles, next_url=next_url, prev_url=prev_url)

@main.route("/artikel/<slug>")
def article_detail(slug):
    artikel = Article.query.filter_by(slug=slug).first()    
    cat = Category.query.all()
    artikel_terbaru = Article.query.order_by(Article.date_posted.desc()).paginate(per_page=4)
    # image_file = url_for('static', filename='assets/img/articles/' + artikel.image_article)
    return render_template('main/articles/artikel_detail.html', artikel=artikel, title=artikel.title, artikel_terbaru=artikel_terbaru, cat=cat)

@main.route("/kategori-artikel/<slug>")
def article_category(slug):
    cat = Category.query.filter_by(slug=slug).first()
    artikel = Article.query.filter_by(category_id=cat.id).order_by(Article.date_posted.desc()).paginate(per_page=10)
    next_url = url_for('main.article_category', page=artikel.next_num) if artikel.has_next else None
    prev_url = url_for('main.article_category', page=artikel.prev_num) if artikel.has_prev else None
    return render_template('main/articles/artikel_kategori.html', artikel=artikel, title=cat.name, cat=cat, next_url=next_url, prev_url=prev_url)

@main.route("/user/<string:username>")
def user_articles(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    articles = Article.query.filter_by(author=user).order_by(Article.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('main/articles/user_artikel.html', title='Artikel', articles=articles, user=user)

@main.route("/berita")
def new():
    page = request.args.get('page', 1, type=int)
    newss = News.query.order_by(News.date_posted.desc()).paginate(page=page, per_page=5)
    next_url = url_for('main.new', page=newss.next_num) if newss.has_next else None
    prev_url = url_for('main.new', page=newss.prev_num) if newss.has_prev else None
    return render_template('main/news/berita.html', title='Berita', newss=newss, next_url=next_url, prev_url=prev_url)

@main.route("/berita/<slug>")
def news_detail(slug):
    berita = News.query.filter_by(slug=slug).first()
    cat = Categoryn.query.all()
    berita_terbaru = News.query.order_by(News.date_posted.desc()).paginate(per_page=4)
    return render_template('main/news/berita_detail.html', title=berita.title, berita=berita, cat=cat, berita_terbaru=berita_terbaru)

@main.route("/kategori-berita/<slug>")
def news_category(slug):
    cat = Categoryn.query.filter_by(slug=slug).first()
    berita = News.query.filter_by(category_id=cat.id).order_by(News.date_posted.desc()).paginate(per_page=10)
    next_url = url_for('main.news_category', page=berita.next_num) if berita.has_next else None
    prev_url = url_for('main.news_category', page=berita.prev_num) if berita.has_prev else None
    return render_template('main/news/berita_kategori.html', berita=berita, title=cat.name, cat=cat, next_url=next_url, prev_url=prev_url)

@main.route("/galeri")
def gallery():
    page = request.args.get('page', 1, type=int)
    gall = Gallery.query.order_by(Gallery.date_posted.desc()).paginate(page=page, per_page=3)
    image = Images_Gallery.query.group_by(Images_Gallery.gallery_id).distinct()
    next_url = url_for('main.gallery', page=gall.next_num) if gall.has_next else None
    prev_url = url_for('main.gallery', page=gall.prev_num) if gall.has_prev else None
    return render_template('main/galleries.html', title='Galeri', gall=gall, image=image, next_url=next_url, prev_url=prev_url)

@main.route("/galeri/<int:gal_id>/<slug>")
def gallery_detail(gal_id, slug):
    imgs = Images_Gallery.query.filter_by(gallery_id=gal_id)
    gall = Gallery.query.filter_by(id=gal_id, slug=slug).first()
    return render_template('main/galeri_detail.html', imgs=imgs, gall=gall)

@main.route("/berkas")
def file():
    page = request.args.get('page', 1, type=int)
    files = Files_Public.query.order_by(Files_Public.id.desc()).paginate(page=page, per_page=4)
    return render_template('main/berkas_public.html', title='Berkas', files=files)

@main.route("/berkas/<slug>")
def file_view(slug):
    file = Files_Public.query.filter_by(slug=slug).first()
    return render_template('main/berkas_detail.html', title='Berkas Detail', file=file)