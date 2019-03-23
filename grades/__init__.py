from flask import Flask

from grades.web.healthcheck import app as healthcheck_app


class App:
    _app = None

    def start(self):
        if self._app:
            return None

        self._app = Flask(__name__)
        self.__register_blueprints()

        return self._app

    def run(self, *args):
        self._app.run(*args)

    def __register_blueprints(self):
        self._app.register_blueprint(healthcheck_app)


app = App().start()
