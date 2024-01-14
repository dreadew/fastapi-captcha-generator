from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import settings

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> Generator:
	'''dependency for getting async session'''
	try:
		session: AsyncSession = async_session()
		yield session
	finally:
		await session.close()