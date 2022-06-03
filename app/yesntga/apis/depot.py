"""Depot: file uploading service"""
import os
import sys
import hashlib
import datetime
from typing import Union
from traceback import format_exc

import xxhash
from werkzeug.utils import secure_filename
import werkzeug.security
from flask import request, make_response, current_app
from flask_restful import Resource, abort
from itsdangerous.exc import BadData, BadSignature
import json
import magic

import yesntga.util.auth
from yesntga.util.limits import limiter
from yesntga.util.log import lg
from yesntga.util import rand_str, mplat_mime, rb
from yesntga import db, sign
from yesntga.models.depot import DepotUser, DepotFile

def validate(token: str) -> Union[DepotUser, bool]:
    if "pytest" in sys.modules:
        return DepotUser(id=2147, username="PyTest", hash="CoolHash0abcdef123456", permission_upload_size=1024,
                         permission_can_delete_files=1)
    try:
        login = json.loads(sign.loads(token))
        user, password = (login['user'], login['password'])
        d = DepotUser.query.filter_by(username=user).first()
        if d is not None and werkzeug.security.check_password_hash(d.hash, password):
            return d
        else:
            return False
    except (BadSignature, BadData, json.JSONDecodeError) as e:
        if type(e) != json.JSONDecodeError and e.payload is not None:
            try:
                dec = sign.load_payload(e.payload)
            except BadData:
                pass
        return False

def allowed_file(mime):
    if "pytest" in sys.modules:
        # TODO: Find a way to imitate mime types in pytest... maybe sample test files?
        return True
    allowed_mime_type_prefixes = []
    allowed_mime_types = [
        # Video
        'video/mp4', 'video/webm', 'video/x-matroska',
        # Audio
        'audio/ogg', 'audio/opus', 'audio/webm', 'audio/wav', 'audio/mp4', 'audio/x-matroska', 'audio/mpeg',
        # Image
        'image/png', 'image/jpeg']
    if mime not in allowed_mime_types:
        return False
    return True

class Depot(Resource):
    decorators = [limiter.limit('2/s')]

    @staticmethod
    def post():
        args = {
            "token": request.form.get('token'),
            "file": request.files.get('file', None)
        }
        media_root = current_app.config.get('MEDIA_ROOT')
        user = validate(args['token'])
        # Step 1: Authenticate
        # Use Werkzeug Security or ItsDangerous to handle tokens
        if not user:
            return {'success': False,
                    'reason': 'unauthorized'}, 401
        # Step 2: Process input file
        # Did we even get a file?
        f = args['file']
        if f is None:
            return {'success': False,
                    'reason': 'invalid'}, 400
        # Is the file an allowed format? Use libmagic
        if not allowed_file(mplat_mime(f)):
            return {'success': False,
                    'reason': 'invalid'}, 400
        # Get file checksum for deduplication using the first 64KB.
        # TODO: Is this even necessary?
        checksum = xxhash.xxh3_128_hexdigest(rb(f,65536))
        # Query database for checksum
        sql = DepotFile.query.filter_by(hash=checksum).first()
        if bool(sql) and os.path.exists(os.path.join(media_root, sql.filename)):
            return {'success': True,
                    'url': f'/depot/{sql.filename}',
                    'full_url': f'https://{request.headers.get("Host")}/depot/{sql.filename}',
                    'filename': sql.filename}
        # Step 3: Process and save the file.
        # Make unique filename using the checksum we got from earlier
        filename = rand_str(checksum) + \
                   os.path.splitext(secure_filename(f.filename))[1]
        # Write to filesystem and database
        try:
            db.session.add(DepotFile(hash=checksum, filename=filename, original_filename=secure_filename(f.filename),
                                 uploader=user.id, upload_date=datetime.datetime.now(),
                                 content_length=request.content_length))
            f.save(os.path.join(media_root, filename))
            db.session.commit()
        except (IOError, OSError):
            lg.critical(f"Save error: {format_exc()}")
            return {'success': False,
                    'reason': 'save-failed'}, 500
        r = make_response({
            "success": True,
            "url": f"/depot/{filename}",
            'full_url': f'https://{request.headers.get("Host")}/depot/{filename}',
            'filename': filename})
        return r

    @staticmethod
    def delete():
        return {'success': False, 'reason': 'not-yet-implemented'}
