from flask import Flask, jsonify

from authentication.web.healthcheck import app as healthcheck_app
from authentication.web.api import app as api_app
from authentication.web.api.exceptions import ValidatorError
from authentication.db import DATABASE

from authentication.models.user import User


MODELS = [User]


class App:
    _app = None

    def start(self):
        if self._app:
            return None

        app = Flask(__name__)
        self._app = app
        self.__register_blueprints()
        self.__create_tables()

        self.__register_error_handlers(app)
        self.__register_hooks(app)

        return self._app

    def run(self, *args):
        self._app.run(*args)

    def __register_blueprints(self):
        self._app.register_blueprint(healthcheck_app)
        self._app.register_blueprint(api_app)

    def __create_tables(self):
        DATABASE.connect()
        DATABASE.create_tables(MODELS)
        DATABASE.close()

    def __register_error_handlers(self, app):
        @app.errorhandler(ValidatorError)
        def handle_validator_error(e):
            return jsonify(errors=e.errors), 400

    def __register_hooks(self, app):
        @app.before_request
        def before_request():
            DATABASE.connect()

        @app.after_request
        def after_request(response):
            DATABASE.close()
            return response


app = App().start()
