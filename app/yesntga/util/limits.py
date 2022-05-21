from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(default_limits=['4/second'], key_func=get_remote_address)