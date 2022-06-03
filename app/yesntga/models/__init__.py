__all__ = ['depot'] # Hack

from yesntga import db
from yesntga.models import *
from sqlalchemy.exc import OperationalError
from yesntga.util.log import lg 
from time import sleep
conn_successful = False 
conn_attempts = 0
while not conn_successful:
    try:
        db.create_all()
        conn_successful = True
        break
    except OperationalError as e:
        if conn_attempts >= 3:
            lg.critical('All attempts to connect to the database failed.')
            lg.exception(e)
            raise e
        lg.critical(f"Failed to connect to database (attempt {conn_attempts}). Retrying in 3 seconds...")
        conn_attempts += 1
        sleep(3)
