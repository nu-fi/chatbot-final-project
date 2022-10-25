from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from apps.config import Config
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
ckeditor = CKEditor()
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    # csrf.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from apps.users.routes import users
    from apps.articles.routes import articles
    from apps.main.routes import main
    from apps.news.routes import news
    from apps.galleries.routes import galleries
    from apps.files.routes import files
    from apps.doctors.routes import doctors
    from apps.chatbot.routes import chatbot
    app.register_blueprint(users)
    app.register_blueprint(articles)
    app.register_blueprint(main)
    app.register_blueprint(news)
    app.register_blueprint(galleries)
    app.register_blueprint(files)
    app.register_blueprint(doctors)
    app.register_blueprint(chatbot)

    return app