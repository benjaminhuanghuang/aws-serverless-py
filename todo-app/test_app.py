import app
import pytest
from chalice import NotFoundError
import json
from basicauth import encode

@pytest.fixture
def api():
    from chalice.local import LocalGateway
    from chalice.config import Config
    return LocalGateway(app.app, Config())

def test_list_todos(api):
    response = api.handle_request(method='GET', path='/todo', headers={}, body=None)
    assert 200 == response['statusCode']
    assert [{'item':'buy milk'},{'item':'mow lawn'}] == json.loads(response['body'])

def test_index(api):
    headers = {'Authorization': encode("abc", "abc")}
    response = api.handle_request(method='GET', path='/', headers=headers, body=None)
    assert 200 == response['statusCode']


def test_get_todo():
    assert { 'item' : 'buy milk'} == app.get_todo('1')

def test_get_todo_missing():
    with pytest.raises(NotFoundError):
        app.get_todo('999')
