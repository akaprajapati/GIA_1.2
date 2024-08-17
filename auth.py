from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Example secret key (in a real app, use a strong secret and store it securely)
SECRET_KEY = "secretkeyexample"
ALGORITHM = "HS256"

# def get_current_user_id(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(
#                 status_code=401, detail="Could not validate credentials"
#             )
#         return user_id
#     except JWTError:
#         raise HTTPException(
#             status_code=401, detail="Could not validate credentials"
#         )


# def hash_password(password: str) -> str:
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed_password.decode('utf-8')


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials"
        )

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
