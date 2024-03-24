from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from jose import jwt, JWTError
from datetime import timedelta, datetime

# Defining the secret key and algorithm used for JWT encoding and decoding
SECRET_KEY = 'zd%t00xw9-&h1#shs$aqguplrc=$x@3jlh1_kwtd7u8z!@i$ym'
ALGORITHM = 'HS256'

# This function is an async dependency that extracts and verifies JWT token information
async def get_current_user(access_token: str):
    try:
        # Decoding the JWT token to get payload
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        id: str = payload.get('id')
        # If 'username' or 'id' is missing in the token, raise an HTTP 401 error
        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        # Return a dictionary with username and id if the token is valid
        return {'username': username, 'id': id}
    except JWTError:
        # If there's an error in decoding the JWT, raise an HTTP 401 error
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')
