from datetime import datetime
from flask import current_app
from apps import db, login_manager
from flask_login import UserMixin, current_user
from flask_security import RoleMixin
from itsdangerous.serializer import Serializer
# from itsdangerous import BadSignature, SignatureExpired


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(20), nullable=False)

    articles = db.relationship('Article', backref='author', lazy=True)
    news = db.relationship('News', backref='author', lazy=True)

    galleries = db.relationship('Gallery', backref='author', lazy=True)
    image_galleries = db.relationship('Images_Gallery', backref='author', lazy=True)

    berkas = db.relationship('DataDokter', backref='owner', lazy=True, uselist=False)

    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, default=2)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def is_administrator(self):
        if current_user.roles_id == 1:
            return self

    def __repr__(self) -> str:
        return super().__repr__()

class DataDokter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap = db.Column(db.String(100), unique=True, nullable=False)
    no_hp = db.Column(db.String(100), unique=True, nullable=False)
    batas_sip = db.Column(db.Date, nullable=False)
    status_data = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    

    def __repr__(self) -> str:
        return super().__repr__()

class TempatPraktik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tempat_praktik = db.Column(db.String(100), nullable=False)
    alamat_praktik = db.Column(db.String(200), nullable=False)    
    kota_praktik = db.Column(db.String(50), nullable=False)
    hari_praktik = db.Column(db.String(50), nullable=False)
    jam_mulai = db.Column(db.Time, nullable=False)
    jam_selesai = db.Column(db.Time, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('tempatpraktiks', lazy=True))

# class TempatPraktik(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     tempat_praktik = db.Column(db.String(100), nullable=False)
#     alamat_praktik = db.Column(db.String(200), nullable=False)    
#     kota_praktik = db.Column(db.String(50), nullable=False)
#     hari_praktik = db.Column(db.String(50), nullable=False)
#     jam_mulai = db.Column(db.Time, nullable=False)
#     jam_selesai = db.Column(db.Time, nullable=False)

#     datadokter_id = db.Column(db.Integer, db.ForeignKey('data_dokter.id'), nullable=False)

#     def __repr__(self) -> str:
#         return super().__repr__()

class Roles(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)

    users = db.relationship('User', backref='role', lazy=True, uselist=False)

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Role> ----> {self.title}'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_article = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, nullable=False, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)

    category = db.relationship('Category', backref=db.backref('article', lazy=True))

    def to_dict(self):
        return {
            'title': self.title,
            'image_article': self.image_article,
            'date_posted': self.date_posted,
            'content': self.content,
            'slug': self.slug,
            'category_id': self.category_id,
            'user_id': self.user_id
        }

    def __repr__(self) -> str:
        return super().__repr__()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50))

    def __repr__(self):
        return '<Category %r>' % self.name

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_news = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, nullable=False, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('categoryn.id'),
        nullable=False)

    categoryn = db.relationship('Categoryn', backref=db.backref('news', lazy=True))

    def __repr__(self) -> str:
        return super().__repr__()

class Categoryn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50))

    def __repr__(self):
        return '<Categoryn %r>' % self.name


class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    slug = db.Column(db.Text, nullable=False, unique=True)
    description = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    images = db.relationship('Images_Gallery', backref='gallery')

    def __repr__(self) -> str:
        return super().__repr__()

class Images_Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_gallery = db.Column(db.String(20))
    description = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'))

    def __repr__(self) -> str:
        return super().__repr__()

class Files_Public(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    filename = db.Column(db.String(50), nullable=False)

    slug = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self) -> str:
        return super().__repr__()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300))
    status_data = db.Column(db.Boolean, default=False)
    response = db.Column(db.String(300), default="No Answer")
    date_posted = db.Column(db.DateTime, default=datetime.now())
    
    # def __repr__(self):
    #     return '<Message %r>' % self.id