from flask import Blueprint, render_template, request
from werkzeug.exceptions import NotFound, InternalServerError

routebp = Blueprint('routes', __name__, template_folder='../templates')
errors = Blueprint('errors', __name__, template_folder='../templates')


@routebp.route("/ip")
def ihaveyourip():
	return render_template('yourip.html', ip=request.headers.get("X-Real-IP", "sussy ball"))

@errors.app_errorhandler(NotFound)
def fuck_off(e):
	return render_template('404.html'), 404

@errors.app_errorhandler(InternalServerError)
def dude_holy_shit(e):
	return f"i cant be bothered with this shit: {e}", 500