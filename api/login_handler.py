from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from api.actions.auth import authenticate_user
from api.actions.user import _update_user_token
from api.schemas import Token, UserLogin
from db.session import get_db
from security import create_access_token

login_router = APIRouter() 

@login_router.post("/token", response_model=Token)
async def login_for_access_token(
    data: UserLogin, db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(data.username, data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    await _update_user_token(email=data.username, access_token=access_token, session=db)
    return {"access_token": access_token, "token_type": "bearer"}