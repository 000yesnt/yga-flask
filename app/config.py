from os import environ, getcwd
from socket import gethostname
from yesntga.util.vault import Vault
from yesntga.util.plat import get_platform
# I shouçd probably not be putting Python code here but ehhhh I make my own rules

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

RUN_TYPE = get_platform()
VERSION = gethostname() if RUN_TYPE == 'linux-docker' else 'PLACEHOLDER'