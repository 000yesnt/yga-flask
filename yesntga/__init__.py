from os import getcwd
import logging
from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import yesntga.util.limits
import yesntga.util.log
from itsdangerous import URLSafeSerializer

def initialize(conf: dict = None) -> Flask:
    """Application factory. Takes a dict including settings as only argument. 
    Returns a fully configured Flask app."""
    global db
    global app
    global sign
    app = Flask(__name__)
    if conf is not None:
        for k in conf:
            app.config[k] = conf[k]
    else:
        app.config.from_object('config')
    # Kick off logging early
    util.log.lg.setLevel(app.config.get('LOGLEVEL', logging.INFO))
    # Configure signer and database
    sign = URLSafeSerializer(app.config['SECRET_KEY'])
    db = SQLAlchemy(app)
    db.init_app(app)

    # Configure utilities
    util.limits.limiter.init_app(app)
    util.log.lg.debug(getcwd())
    util.log.lg.debug(str(app.url_map))
    app.jinja_env.globals.update(index_of=lambda lst, itm: lst.index(itm))

    # Configure routes
    import yesntga.views
    import yesntga.apis.depot
    __apibp__ = Blueprint('apis', __name__, template_folder='templates')
    __api__ = Api(__apibp__)
    __api__.add_resource(yesntga.apis.depot.Depot, '/api/depot')
    app.register_blueprint(yesntga.views.routebp)
    app.register_blueprint(yesntga.views.errors)

    return app

db = globals().get('db') or SQLAlchemy()
sign = globals().get('sign') or URLSafeSerializer('UNSAFE')
app = globals().get('app') or initialize()