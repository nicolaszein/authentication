from flask import Flask, jsonify
from peewee import DoesNotExist

from authentication.web.healthcheck import app as healthcheck_app
from authentication.web.api import app as api_app
from authentication.web.app.routes import app as auth_app
from authentication.db import DATABASE

from authentication.models.user import User
from authentication.models.session import Session
from authentication.exceptions import InvalidCredentialsError, ValidatorError


MODELS = [User, Session]


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
        self._app.register_blueprint(auth_app)

    def __create_tables(self):
        DATABASE.connect(reuse_if_open=True)
        DATABASE.create_tables(MODELS)
        DATABASE.close()

    def __register_error_handlers(self, app):
        @app.errorhandler(ValidatorError)
        def handle_validator_error(e):
            return jsonify(errors=e.errors), 400

        @app.errorhandler(DoesNotExist)
        def object_not_found(e):
            return jsonify(errors='Resource not found'), 404

        @app.errorhandler(InvalidCredentialsError)
        def invalid_credentials(e):
            return jsonify(errors='Invalid Credentials'), 401

    def __register_hooks(self, app):
        @app.before_request
        def before_request():
            DATABASE.connect(reuse_if_open=True)

        @app.after_request
        def after_request(response):
            DATABASE.close()
            return response


app = App().start()
