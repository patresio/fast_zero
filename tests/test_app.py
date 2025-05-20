from http import HTTPStatus


def test_root_deve_retornar_ola_mundo(client):
    response = client.get('/')
    assert response.json() == {'message': 'Olá Mundo!'}


def test_root_deve_retorna_status_code_200(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


def test_root_html_deve_retornar_html(client):
    response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text


def test_create_user(client):
    user_data = {
        'username': 'joaozinho',
        'email': 'joaozinho@mail.com',
        'password': 'secret',
    }
    response = client.post('/users/', json=user_data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'joaozinho',
        'email': 'joaozinho@mail.com',
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'joaozinho',
                'email': 'joaozinho@mail.com',
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'joaozinho12',
            'email': 'joaozinho@mail.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'joaozinho12',
        'email': 'joaozinho@mail.com',
    }


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'joaozinho12',
        'email': 'joaozinho@mail.com',
    }
