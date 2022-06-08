from flask import Blueprint, make_response, render_template, request, current_app
from yesntga import app
from yesntga.models import conn_successful
import os.path
import jinja2

from werkzeug.exceptions import NotFound, InternalServerError
import json 
from os import urandom
from os.path import exists
from base64 import urlsafe_b64encode

routebp = Blueprint('routes', __name__, template_folder='../templates')
errors = Blueprint('errors', __name__, template_folder='../templates')

health: dict = None 
def get_h() -> dict:
	global health
	with app.app_context():
		if health:
			return health
		health = {
					'healthy': True if not current_app.config.get('API_LOAD_FAIL') or conn_successful else False,
					'api_failed': current_app.config.get('API_LOAD_FAIL', False),
					'db_failed': False if conn_successful else True,
					'type': 'view',
					'version': current_app.config.get('VERSION'),
					'type': current_app.config.get('RUN_TYPE'),
					'meow': 'meow!',
					'ip': {
						'X-Real-IP': request.headers.get('X-Real-IP'),
						'X-Forwarded-For': request.headers.get('X-Forwarded-For'),
						'Forwarded': request.headers.get('Forwarded')
					}
				}
		return health

@routebp.route('/')
def index():
	front = {
		'healthy': 'healthy' if get_h()['healthy'] else 'unhealthy',
		'running_on': get_h()['type'],
		'version': get_h()['version'],
		'pgtitle': 'sussy',
		'projects': [
			{
				'title': 'creature',
				'desc': 'communication',
				'url': 'cta.html'
			},
			{
				'title': 'my brother in christ you cannot dip your balls in hot oil',
				'desc': 'See how this phrase reminds the book "1894" by Jorjor Wel',
				'url': 'https://dbd.yesnt.ga/fog/locker/morbius.mp4'
			}
		]
	}
	for i in front['projects']:
		i['index'] = front['projects'].index(i)
	return render_template("front.html", **front)

@routebp.route('/health')
def health_check():
	r = make_response(json.dumps(get_h()))
	r.headers['Content-Type'] = 'application/json'
	return r

@routebp.route("/ip")
def ihaveyourip():
	return render_template('yourip.html', ip=request.headers.get("X-Real-IP", "sussy ball"))

@errors.app_errorhandler(NotFound)
def fuck_off(e):
	return render_template('404.html'), 404

@errors.app_errorhandler(InternalServerError)
def dude_holy_shit(e):
	return f"i cant be bothered with this shit: {e}", 500