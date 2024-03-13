from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from jose import jwt, JWTError
from datetime import timedelta, datetime

SECRET_KEY = 'zd%t00xw9-&h1#shs$aqguplrc=$x@3jlh1_kwtd7u8z!@i$ym'
ALGORITHM = 'HS256'

async def get_current_user(access_token: str):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        id: str = payload.get('id')
        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return {'username': username, 'id': id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')
