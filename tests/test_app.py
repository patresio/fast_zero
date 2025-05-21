from http import HTTPStatus


def test_root_deve_retornar_ola_mundo(client):
    """Testa se a rota raiz ('/') retorna o
    JSON esperado {'message': 'Olá Mundo!'.}"""
    response = client.get('/')
    assert response.json() == {'message': 'Olá Mundo!'}


def test_root_deve_retorna_status_code_200(client):
    """Testa se a rota raiz ('/') retorna o status code 200 (OK)."""
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


def test_root_html_deve_retornar_html(client):
    """Testa se a rota '/html' retorna um status code 200 (OK) e se o
    conteúdo HTML esperado está presente na resposta."""
    response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text


def test_create_user(client):
    """Testa a criação de um novo usuário.
    Verifica se o status code é CREATED (201) e se a resposta contém o ID,
    username e email do usuário criado, sem a senha.
    """
    # Arrange: Define os dados para o novo usuário
    user_payload = {
        'username': 'joaozinho',
        'email': 'joaozinho@mail.com',
        'password': 'secret',
    }

    # Act: Envia uma requisição POST para criar o usuário
    response = client.post('/users/', json=user_payload)

    # Assert: Verifica o status code e a estrutura da resposta
    assert response.status_code == HTTPStatus.CREATED

    response_data = response.json()
    # Verifica se a chave 'id' existe
    # Verifica se 'id' é um inteiro
    assert 'id' in response_data
    assert isinstance(response_data['id'], int)
    assert response_data['username'] == user_payload['username']
    assert response_data['email'] == user_payload['email']
    # Garante que a senha não é retornada
    assert 'password' not in response_data


def test_read_users(client):
    """Testa a leitura da lista de usuários.
    Primeiro, cria um usuário para garantir que a lista não esteja vazia.
    Depois, verifica se o status code é OK (200) e se o usuário criado está
    presente na lista retornada.
    """
    # Arrange: Create a user to ensure data exists for the read operation
    user_data_to_create = {
        'username': 'test_read_user',
        'email': 'test_read_user@example.com',
        'password': 'testpassword',
    }
    response_create = client.post('/users/', json=user_data_to_create)
    assert response_create.status_code == HTTPStatus.CREATED
    # Contains id, username, email
    created_user_data = response_create.json()

    # Act: Retrieve the list of users
    response = client.get('/users/')

    # Assert: Check status code and that the created user is in the list
    assert response.status_code == HTTPStatus.OK

    expected_user_in_list = {
        'id': created_user_data['id'],
        'username': user_data_to_create['username'],
        'email': user_data_to_create['email'],
    }
    # Assuming the database was empty before this test
    # (due to clear_db_before_each_test),
    # the 'users' list should contain exactly this one user.
    assert response.json() == {'users': [expected_user_in_list]}


def test_update_user(client):
    """Testa a atualização de um usuário existente.
    Primeiro, cria um usuário.
    Depois, tenta atualizar os dados desse usuário.
    Verifica se o status code é OK (200) e se os dados do usuário na resposta
    foram de fato atualizados.
    """
    # Arrange: Create a user to be updated
    user_data_to_create = {
        'username': 'testuser_before_update',
        'email': 'testuser_before@example.com',
        'password': 'testpassword',
    }
    response_create = client.post('/users/', json=user_data_to_create)
    assert response_create.status_code == HTTPStatus.CREATED
    created_user_data = response_create.json()
    user_id_to_update = created_user_data['id']

    # Data for update
    user_data_to_update = {
        'username': 'testuser_after_update',
        'email': 'testuser_after@example.com',
        'password': 'new_password',  # Password can also be updated
    }

    # Act: Update the user
    response = client.put(
        f'/users/{user_id_to_update}',
        json=user_data_to_update,
    )

    # Assert: Check status code and that the user data is updated
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user_id_to_update,
        'username': user_data_to_update['username'],
        'email': user_data_to_update['email'],
    }


def test_delete_user(client):
    """Testa a exclusão de um usuário existente.
    Primeiro, cria um usuário.
    Depois, tenta excluir esse usuário.
    Verifica se o status code é OK (200) e se a resposta contém os dados do
    usuário que foi excluído.
    """
    # Arrange: Create a user to be deleted
    user_data_to_create = {
        'username': 'user_to_delete',
        'email': 'delete@example.com',
        'password': 'testpassword',
    }
    response_create = client.post('/users/', json=user_data_to_create)
    assert response_create.status_code == HTTPStatus.CREATED
    created_user_data = response_create.json()
    user_id_to_delete = created_user_data['id']

    # Act: Delete the user
    response = client.delete(f'/users/{user_id_to_delete}')

    # Assert: Check status code and that the correct user data is returned
    assert response.status_code == HTTPStatus.OK
    # Assuming the DELETE endpoint returns the data
    # of the user that was deleted
    assert response.json() == created_user_data


def test_update_user_not_found(client):
    """
    Testa a tentativa de atualização de um usuário que não existe.
    Verifica se o status code é NOT_FOUND (404) e se a
    mensagem de erro é a esperada.
    """
    response = client.put(
        '/users/100',  # ID que provavelmente não existe
        json={
            'username': 'joaozinho100',
            'email': 'joaozinho100@mail.com',
            'password': 'secret100',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_update_user_invalid_id_less_than_one(client):
    """
    Testa a tentativa de atualização de um usuário
    com um ID inválido (menor que 1).
    Verifica se o status code é NOT_FOUND (404), assumindo que IDs inválidos
    resultam em 'não encontrado'.
    """
    response = client.put(
        '/users/0',  # ID inválido
        json={
            'username': 'test',
            'email': 'test@example.com',
            'password': 'pwd',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_delete_user_not_found(client):
    """Testa a tentativa de exclusão de um usuário que não existe.
    Verifica se o status code é NOT_FOUND (404) e
    se a mensagem de erro é a esperada.
    """
    response = client.delete('/users/100')  # ID que provavelmente não existe
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_delete_user_invalid_id_less_than_one(client):
    """Testa a tentativa de exclusão de um usuário com um
    ID inválido (menor que 1).
    Verifica se o status code é NOT_FOUND (404), assumindo que
    IDs inválidos resultam em 'não encontrado'.
    """
    # Tenta deletar um usuário com ID 0, que é inválido
    response = client.delete('/users/0')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}
