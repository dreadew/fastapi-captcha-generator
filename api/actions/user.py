from typing import Union
from uuid import UUID

from api.schemas import ShowUser
from api.schemas import UserCreate
from db.dals import UserDAL
from db.models import User
from hashing import Hasher


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            nickname=body.nickname,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password)
        )
        return ShowUser(
            user_id=user.user_id,
            nickname=user.nickname,
            email=user.email,
            is_active=user.is_active,
            access_token=user.access_token
        )


async def _delete_user(user_id: UUID, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(
            user_id=user_id,
        )
        return deleted_user_id


async def _update_user(
    updated_user_params: dict, user_id: UUID, session
) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(
            user_id=user_id, **updated_user_params
        )
        return updated_user_id


async def _get_user_by_id(user_id: UUID, session) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(
            user_id=user_id,
        )
        if user is not None:
            return user
        
async def _get_me(access_token: str, session) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_me(
            access_token=access_token
        )
        if user is not None:
            return user
        
async def _update_user_token(email: str, access_token: str, session) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.update_user_token(
            email,
            access_token=access_token
        )
        if user is not None:
            return user