from pathlib import Path
from flask import Blueprint
from autodiscover import AutoDiscover


app = Blueprint('authentication', __name__)

ENDPOINT_PREFIX = '/api'

routes_path = Path('authentication/web/api/routes')
autodiscover_routes = AutoDiscover(path=routes_path)
autodiscover_routes()
