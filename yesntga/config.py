MAX_CONTENT_LENGTH = 100 * (1024 ** 2)
MEDIA_ROOT = "/var/depot"
SQLALCHEMY_TRACK_MODIFICATIONS = False
with open("/run/secrets/mysql_password") as SECFILE_DB_PW, open("/run/secrets/flask_key") as SECFILE_SECRET_KEY:
    dbpw = SECFILE_DB_PW.readline().rstrip('\n')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://yga:{dbpw}@db/yga?charset=utf8mb4"
    SECRET_KEY = SECFILE_SECRET_KEY.readline().rstrip('\n')
USE_X_SENDFILE = True
