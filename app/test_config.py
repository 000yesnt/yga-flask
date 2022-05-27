from secrets import token_hex
from tempfile import TemporaryDirectory

__tempdir__ = TemporaryDirectory()
DEPOT_PATH = __tempdir__.name
SECRET_KEY = f'TEST_{token_hex(8)}'
SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"