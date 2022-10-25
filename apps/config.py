import os

class Config:
    SECRET_KEY = 'aa84a2e78ca27e834a2ab8aab8a0a924'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///idaii.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587 
    MAIL_USE_TLS = True
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_USERNAME = 'idaikalbar123@gmail.com'
    MAIL_PASSWORD = 'itqaepariuubvnqs'