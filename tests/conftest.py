import pytest
from authentication import (
    App,
    MODELS
)
from authentication.db import DATABASE


@pytest.fixture(scope='function')
def app(request):
    app = App().start()

    context = app.app_context()

    def teardown():
        DATABASE.drop_tables(MODELS)
        context.pop()
        DATABASE.close()

    request.addfinalizer(teardown)

    context.push()

    return app


@pytest.fixture(scope='function')
def client(request, app):
    client = app.test_client()
    return client
