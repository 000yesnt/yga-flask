from os import environ
from yesntga.util.vault import Vault

MAX_CONTENT_LENGTH = 100 * (1024 ** 2)
MEDIA_ROOT = "/var/depot"
SQLALCHEMY_TRACK_MODIFICATIONS = False
v = Vault()
if environ.get('FLASK_ENV', 'production') != 'development':
    dbpw = v.get('mysql_password', '123456').rstrip('\n')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://yga:{dbpw}@db/yga?charset=utf8mb4"
else:
    print("Using SQLite in RAM!!!")
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
SECRET_KEY = v.get('flask_key','agsvsdga').rstrip('\n')
USE_X_SENDFILE = True
