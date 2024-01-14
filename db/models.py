import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'

	user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	nickname = Column(String, nullable=False)
	email = Column(String, nullable=False, unique=True)
	hashed_password = Column(String, nullable=False)
	is_active = Column(Boolean(), default=True)
	access_token = Column(String, nullable=False, unique=True)