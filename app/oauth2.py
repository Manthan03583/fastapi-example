import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schema, database, models
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# secret key
SECRET_KEY = settings.secret_key
# Algorithm
ALGORITHM = settings.algorithm
# expriation time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = float(ACCESS_TOKEN_EXPIRE_MINUTES)) 
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id:str = str(payload.get("user_id"))

        if id is None:
            raise credentials_exception
        
        token_data = schema.TokenData(id = id)

    
    except PyJWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exeception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate crendentials", headers={"WWW-Authenticate" : "Bearer"})

    token = verify_access_token(token, credentials_exeception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user