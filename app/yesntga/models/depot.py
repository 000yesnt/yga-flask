from yesntga import db
from sqlalchemy.dialects.mysql import INTEGER
class DepotUser(db.Model):
    __tablename__ = 'depot_users'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    hash = db.Column(db.String(512), unique=True, nullable=False)
    files = db.relationship("DepotFile")
    permission_upload_size = db.Column(db.Integer, nullable=False)
    permission_can_delete_files = db.Column(db.Boolean, nullable=False)

class DepotFile(db.Model):
    __tablename__ = 'depot_files'
    hash = db.Column(db.String(192), primary_key=True, unique=True, nullable=False)
    filename = db.Column(db.String(128), nullable=False, unique=False)
    original_filename = db.Column(db.String(300), nullable=True, unique=False)
    upload_date = db.Column(db.DateTime)
    content_length = db.Column(INTEGER(unsigned=True))
    uploader = db.Column(db.Integer, db.ForeignKey('depot_users.id'))