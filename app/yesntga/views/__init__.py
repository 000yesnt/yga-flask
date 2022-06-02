from flask import Blueprint, make_response, render_template, request, current_app
from yesntga import app
import os.path

from werkzeug.exceptions import NotFound, InternalServerError
import json 

routebp = Blueprint('routes', __name__, template_folder='../templates')
errors = Blueprint('errors', __name__, template_folder='../templates')

@routebp.route('/health')
def health_check():
	with app.app_context() as a:
		payload = {
			'healthy': True,
			'version': current_app.config.get('VERSION'),
			'type': current_app.config.get('RUN_TYPE'),
			'meow': 'meow!',
			'ip': {
				'X-Real-IP': request.headers.get('X-Real-IP'),
				'X-Forwarded-For': request.headers.get('X-Forwarded-For'),
				'Forwarded': request.headers.get('Forwarded')
			}
		}
	r = make_response(json.dumps(payload))
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