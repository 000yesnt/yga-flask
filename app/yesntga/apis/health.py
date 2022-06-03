from flask import Blueprint, make_response, render_template, request, current_app
from yesntga import app
from flask_restful import Resource, abort
import json
from os import urandom
from base64 import urlsafe_b64encode
class HealthCheck(Resource):
    def get(__self__):
        with app.app_context() as a:
            payload = {
            	'healthy': True,
                'api_failed': a.config.get('API_LOAD_FAIL', False),
                'type': 'api',
            	'version': current_app.config.get('VERSION'),
            	'type': current_app.config.get('RUN_TYPE'),
            	'meow': 'meow!',
            	'ip': {
            		'X-Real-IP': request.headers.get('X-Real-IP'),
            		'X-Forwarded-For': request.headers.get('X-Forwarded-For'),
            		'Forwarded': request.headers.get('Forwarded')
            	},
                'cachebuster': urlsafe_b64encode(urandom(16)).decode('utf-8')
            }
        r = make_response(json.dumps(payload))
        r.headers['Content-Type'] = 'application/json'
        return r