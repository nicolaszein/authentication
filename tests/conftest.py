import pytest
from grades import app as GradesApp


@pytest.fixture(scope='function')
def app(request):
    app = GradesApp

    context = app.app_context()

    def teardown():
        context.pop()

    request.addfinalizer(teardown)

    context.push()

    return app


@pytest.fixture(scope='function')
def client(request, app):
    client = app.test_client()
    return client
