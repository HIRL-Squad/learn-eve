import pytest


@pytest.fixture(scope='session')
def test_client():
    from app import create_server
    app = create_server(test=True)
    client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield client

    app.connection.drop_database('eve')