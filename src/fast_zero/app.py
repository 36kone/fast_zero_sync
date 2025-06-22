from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_whit_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(user_whit_id)

    return user_whit_id


@app.get('/users/', response_model=UserList)
def read_user():
    return {'users': database}


@app.get('/users/{id_user}', response_model=UserPublic)
def read_user_by_id(id_user: int):
    for user in database:
        if user.id == id_user:
            return user

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='User not found')
    else:
        user_whit_id = UserDB(id=user_id, **user.model_dump())

        database[user_id - 1] = user_whit_id

    return user_whit_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='User not found')
    else:
        del database[user_id - 1]
        return {'message': 'User deleted'}
