from flask import Blueprint

app = Blueprint('healthcheck', __name__)


@app.route('/health-check')
def health_check():
    return 'Ok'
