from datetime import timedelta
from typing import Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from security import create_access_token
from settings import ACCESS_TOKEN_EXPIRE_MINUTES

class UserDAL:
	'''data access layer for operating user info'''
	def __init__(self, db_session: AsyncSession):
		self.db_session=db_session
	
	async def create_user(
			self, nickname: str, email: str, hashed_password: str
	) -> User:
		access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
		access_token = create_access_token(
        data={"sub": email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
		new_user = User(
			nickname=nickname,
			email=email,
			hashed_password=hashed_password,
			access_token=access_token
		)
		self.db_session.add(new_user)
		await self.db_session.flush()
		return new_user
	
	async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
		query = update(User).where(and_(User.user_id == user_id, User.is_active == True)).values(is_active=False).returning(User.user_id)
		res = await self.db_session.execute(query)
		deleted_user_id_row = res.fetchone()
		if deleted_user_id_row is not None:
			return deleted_user_id_row[0]
		
	async def get_user_by_id(self, user_id: UUID) -> Union[UUID, None]:
		query = select(User).where(User.user_id == user_id)
		res = await self.db_session.execute(query)
		user_row = res.fetchone()
		if user_row is not None:
			return user_row[0]
		
	async def get_me(self, access_token: str) -> Union[UUID, None]:
		query = select(User).where(User.access_token == access_token)
		res = await self.db_session.execute(query)
		user_row = res.fetchone()
		if user_row is not None:
			return user_row[0]
		
	async def get_user_by_email(self, email: str) -> Union[User, None]:
		query = select(User).where(User.email == email)
		res = await self.db_session.execute(query)
		user_row = res.fetchone()
		if user_row is not None:
			return user_row[0]
		
	async def update_user(self, **kwargs) -> Union[UUID, None]:
		query = update(User).where(User.is_active == True).values(kwargs).returning(User.user_id)
		res = await self.db_session.execute(query)
		update_user_id_row = res.fetchone()
		if update_user_id_row is not None:
			return update_user_id_row[0]
		
	async def update_user_token(self, email: str, access_token: str) -> Union[UUID, None]:
		query = update(User).where(User.email == email).values(access_token=access_token).returning(User.user_id)
		res = await self.db_session.execute(query)
		update_user_id_row = res.fetchone()
		if update_user_id_row is not None:
			return update_user_id_row[0]