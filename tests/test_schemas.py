from fast_zero.schemas import Message


def test_message_schema():
    message_data = {'message': 'Olá Mundo!'}
    message = Message(**message_data)
    assert message.message == 'Olá Mundo!'


def test_message_schema_com_dados_diferentes():
    message_data = {'message': 'Teste'}
    message = Message(**message_data)
    assert message.message == 'Teste'
