from yesntga.util.vault import Vault
from yesntga.util.plat import get_platform
from socket import gethostname
# I shouçd probably not be putting Python code here but ehhhh I make my own rules

MEDIA_ROOT = "/var/depot"
v = Vault()
dbpw = v.get('mysql_password', '123456').rstrip('\n')
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://yga:{dbpw}@db/yga?charset=utf8mb4"
SECRET_KEY = v.get('flask_key','UNSAFE').rstrip('\n')

RUN_TYPE = get_platform()
VERSION = gethostname() if RUN_TYPE == 'linux-docker' else 'PLACEHOLDER'