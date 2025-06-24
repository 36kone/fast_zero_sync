from http import HTTPStatus

from jwt import decode

from fast_zero.security import ALGORITHN, SECRET_KEY, create_acess_token


def test_jwt():
    data_payload = {'sub': 'test@test.com'}
    token = create_acess_token(data_payload)

    result = decode(token, SECRET_KEY, algorithms=[ALGORITHN])

    assert result['sub'] == data_payload['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete('/users/1', headers={'Authorization': 'Bearer token-invalido'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
