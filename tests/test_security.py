from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_acess_token, settings


def test_jwt():
    data_payload = {'sub': 'test@test.com'}
    token = create_acess_token(data_payload)

    result = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHN])

    assert result['sub'] == data_payload['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete('/users/1', headers={'Authorization': 'Bearer token-invalido'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
