from flask import Blueprint, make_response, render_template, request, current_app
from yesntga import app
from flask_restful import Resource, abort
import json
class HealthCheck(Resource):
    def get(__self__):
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