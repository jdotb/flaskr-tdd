import pytest
import os
from pathlib import Path
from project.app import app, init_db

TEST_DB = "test.db"


@pytest.fixture
def client():
    BASE_DIR = Path(__file__).resolve().parent.parent
    app.config["TESTING"] = True
    app.config["DATABASE"] = BASE_DIR.joinpath(TEST_DB)

    init_db()  # Setup
    yield app.test_client()  # Tests run here
    init_db()  # Teardown


def login(client, username, password):
    '''login helper fn'''
    return client.post(
        "/login",
        data=dict(username=username, password=password),
        follow_redirects=True,
    )


def logout(client):
    '''logout helper fn'''
    return client.get("/logout", follow_redirects=True)


def test_index(client):
    response = client.get("/", content_type="html/text")
    assert response.status_code == 200


def test_database(client):
    '''initial test - make sure db exists'''
    tester = Path("test.db").is_file()
    assert tester


def test_empty_db(client):
    '''make sure db is blank'''
    rv = client.get('/')
    assert b"No entries yet. Add some!" in rv.data


def test_login_logout(client):
    '''Test login/out with helper fun'''
    rv = login(client, app.config['USERNAME'], app.config['PASSWORD'])
    assert b"You were logged in" in rv.data
    rv = logout(client)
    assert b"You were logged out" in rv.data
    rv = login(client, app.config["USERNAME"] + "x", app.config["PASSWORD"])
    assert b"Invalid username" in rv.data
    rv = login(client, app.config["USERNAME"], app.config["PASSWORD"] + "x")
    assert b"Invalid password" in rv.data


def test_messages(client):
    """Ensure that user can post messages"""
    login(client, app.config["USERNAME"], app.config["PASSWORD"])
    rv = client.post(
        "/add",
        data=dict(title="<Hello>", text="<strong>HTML</strong> allowed here"),
        follow_redirects=True,
    )
    assert b"No entries here so far" not in rv.data
    assert b"&lt;Hello&gt;" in rv.data
    assert b"<strong>HTML</strong> allowed here" in rv.data


def test_index():
    tester = app.test_client()
    response = tester.get("/", content_type="html/text")

    assert response.status_code == 200
    assert response.data == b"Hello, World!"


def test_db():
    init_db()
    assert Path('flaskr.db').is_file()
