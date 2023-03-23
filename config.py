import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'super-secret-i-can-read-anything-key'

SECURITY_PASSWORD_SALT = 'random_salt_i-can-read-anything'
SECURITY_PASSWORD_HASH = 'sha512_crypt'
