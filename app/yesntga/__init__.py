from gevent import monkey
monkey.patch_all()

import logging
from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from yesntga.util.limits import limiter
from yesntga.util.log import lg
from itsdangerous import URLSafeSerializer
import importlib
import traceback

def initialize(conf: dict = None) -> Flask:
    """Application factory. Takes a dict including settings as only argument. 
    Returns a fully configured Flask app."""
    global db
    global app
    global sign

    app = Flask(__name__)
    app.config.from_object('base_config')

    if conf is not None:
        lg.info('LOADING Dict Config')
        for k in conf:
            app.config[k] = conf[k]
    else:
        lg.info('LOADING Normal (Env var) Config')
        app.config.from_envvar('CONFIG_PATH')

    # Configure signer and database
    sign = URLSafeSerializer(app.config.get('SECRET_KEY'))
    db = SQLAlchemy(app)
    db.init_app(app)

    # Configure utilities
    limiter.init_app(app)
    app.jinja_env.globals.update(index_of=lambda lst, itm: lst.index(itm))

    # Configure routes
    import yesntga.views
    app.register_blueprint(yesntga.views.routebp)
    app.register_blueprint(yesntga.views.errors)

    # Configure APIs
    __apibp__ = Blueprint('apis', __name__, template_folder='templates')
    __api__ = Api(__apibp__)

    app.config['LOADED_APIS'] = []
    for i in app.config.get('APIS'): 
        try:
            mod = importlib.import_module(i[0])
            api = mod.__dict__.get(i[1])
            __api__.add_resource(api, i[2])
            app.config['LOADED_APIS'].append(i[1])
        except Exception as e:
            lg.critical(f'FAILED to load API {i}')
            lg.exception(e)
            app.config['API_LOAD_FAIL'] = True
    app.register_blueprint(__apibp__)

    lg.info("App initialized successfully!!!")
    lg.debug(str(app.url_map))

    return app

db: SQLAlchemy = globals().get('db')
sign: URLSafeSerializer = globals().get('sign')
app: Flask = globals().get('app')

if __name__ == 'yesntga':
    app = initialize()