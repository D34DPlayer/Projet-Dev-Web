import asyncio
import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from .db import db
from .schemas import DBUser, TokenModel

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
DB_RETRIES = int(os.getenv("DB_RETRIES", 3))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE"))

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app = FastAPI(title="Boucherie", root_path="/api")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.on_event("startup")
async def startup():
    exception = None
    for retries in range(DB_RETRIES):
        try:
            await db.connect()
            break
        except ConnectionRefusedError as e:
            exception = e
            backoff = 2 ** retries / 10
            print(f"Couldn't connect to the database. Retrying in {backoff}s.")
            await asyncio.sleep(backoff)
    else:
        raise exception


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user = await DBUser.get(username)
    if user and pwd_context.verify(password, user.hashed_password):
        return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def is_connected(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await DBUser.get(username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token", tags=["security"], response_model=TokenModel)
@limiter.limit("3/minute")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """Provides an OAuth2 token if the credentials are right."""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
