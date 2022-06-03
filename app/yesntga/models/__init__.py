from yesntga import db
from yesntga.models import depot
from sqlalchemy.exc import OperationalError
from yesntga.util.log import lg 
conn_successful = False 
conn_fail = False
conn_attempts = 0
while not conn_successful or not conn_fail:
    try:
        db.create_all()
        conn_successful = True
    except OperationalError as e:
        if conn_attempts >= 3:
            lg.critical('All attempts to connect to the database failed.')
            lg.exception(e)
            conn_fail = True
            break
        lg.critical(f"Failed to connect to database (attempt {conn_attempts}). Retrying...")
        conn_attempts += 1
