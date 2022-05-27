from yesntga.util.plat import get_platform
from socket import gethostname

USE_X_SENDFILE = True
MAX_CONTENT_LENGTH = 100 * (1024 ** 2)

SQLALCHEMY_TRACK_MODIFICATIONS = False

RUN_TYPE = get_platform()
VERSION = gethostname() if RUN_TYPE == 'linux-docker' else 'PLACEHOLDER'