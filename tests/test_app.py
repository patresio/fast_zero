from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app

client = TestClient(app)


def test_root_deve_retornar_ola_mundo():
    client = TestClient(app)
    response = client.get('/')
    assert response.json() == {'message': 'Olá Mundo!'}


def test_root_deve_retorna_status_code_200():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


def test_root_html_deve_retornar_html():
    response = client.get('/html')
    assert response.json() == '<h1>Olá Mundo!</h1>'
