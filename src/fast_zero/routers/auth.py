from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.dependencies import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import (
    create_acess_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])

T_Session = Annotated[Session, Depends(get_session)]
T_OAuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
def login_for_acess_token(session: T_Session, form_data: T_OAuthForm):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail='Incorret email or password')

    acess_token = create_acess_token(data_payload={'sub': user.email})

    return {'acess_token': acess_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(
    user: User = Depends(get_current_user),
):
    new_access_token = create_acess_token(data_payload={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
