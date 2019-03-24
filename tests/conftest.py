import pytest
from grades import (
    app as GradesApp,
    MODELS
)
from grades.db import DATABASE


@pytest.fixture(scope='function')
def app(request):
    app = GradesApp

    context = app.app_context()

    def teardown():
        DATABASE.drop_tables(MODELS)
        context.pop()

    request.addfinalizer(teardown)

    context.push()

    return app


@pytest.fixture(scope='function')
def client(request, app):
    client = app.test_client()
    return client
