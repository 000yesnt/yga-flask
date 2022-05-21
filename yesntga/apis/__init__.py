from flask import Blueprint
from flask_restful import Api
apibp = Blueprint('apis', __name__, template_folder='templates')
api = Api(apibp)
# This is fucking atrocious
import apis.depot

loadapis = [
    (apis.depot.Depot, "/api/depot"),
]

for (cls, url) in loadapis:
    api.add_resource(cls, url)