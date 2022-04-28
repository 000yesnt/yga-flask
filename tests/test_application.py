import os
import io
import time
import logging
import tempfile
import json

import sqlalchemy
import shutil
import pytest

import yesntga

DEPOT_API_URL = '/api/depot'
DEPOT_TEST_FILE = (io.BytesIO(b'yesnt was here'), 'yesnt.txt')

def depot_post(client, key, f=None):
    return client.post(DEPOT_API_URL, data=dict(
        auth=key,
        file=f
    ), content_type='multipart/form-data', follow_redirects=True)

def depot_del(client, key, f=None):
    return client.delete(DEPOT_API_URL, data=dict(
        auth=key,
        filename=f
    ), content_type='multipart/form-data', follow_redirects=True)

def depot_fetch_random_data():
    return io.BytesIO(os.urandom(2048)), 'yesnt.txt'

@pytest.fixture(scope='module')
def app_instance():
    with tempfile.TemporaryDirectory(prefix="pyt_alchemy_") as alchemy_temp_db, \
        tempfile.TemporaryDirectory(prefix="pyt_depot_") as depot_temp_dir:
        app = yesntga.initialize({
            "SECRET_KEY": "crazy_key_whoa_so_sekret",
            "MAX_CONTENT_LENGTH": 24 * (1024 ** 2),
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{alchemy_temp_db}{os.sep}pytest-{os.urandom(6).hex()}.db",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True,
            "DEBUG": True,
            'MEDIA_ROOT': depot_temp_dir,
            'LOGLEVEL': logging.DEBUG
        })
        yield app
        yesntga.db.session.close()
        yesntga.db.engine.dispose()
        del app

@pytest.fixture
def client(app_instance):
    with app_instance.test_client() as c:
        yield c

class TestCore:
    def test_not_override_idx(self, client):
        """The app should NOT override or have its own index."""
        r = client.get('/')
        assert b'not found' in r.data

class TestLynx:
    def test_lynx_serve_default(self, client):
        """Guarantee that /lynx is serving images instead of failing"""
        r = client.get('/lynx')
        assert b'ERR:' not in r.data
        assert '/int/lynx/' in r.headers.get('X-Accel-Redirect')
    def test_lynx_serve_webp(self, client):
        """Guarantee that /lynx/webp is serving WebPs ONLY, WITHOUT failres."""
        r = client.get('/lynx/webp')
        assert b'ERR:' not in r.data
        assert '/int/lynxwebp/' in r.headers.get('X-Accel-Redirect')

class TestDepot:
    passphrase = "123$Flask$Auth$Test$123"
    def test_depot_upload(self, client):
        r = depot_post(client, self.passphrase)
        assert r.status_code == 400
        logging.info(json.loads(r.data))

        r = depot_post(client, self.passphrase, (io.BytesIO(b'yesnt was here'), 'yesnt.txt'))
        logging.info(json.loads(r.data))
        assert r.status_code == 200

        # todo: reimpl this bs
        #r = depot_post(client, self.passphrase, depot_fetch_random_data())
        #logging.info(json.loads(r.data))
        #assert r.status_code == 413