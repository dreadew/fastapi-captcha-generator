import re, uuid

from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator, constr

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")

class TunedModel(BaseModel):
	class Config:
		'''tells pydantic to convert even non dict obj to json'''

		orm_mode = True

class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID

class ShowUser(TunedModel):
	user_id: uuid.UUID
	nickname: str
	email: EmailStr
	is_active: bool
	access_token: str

class ShowCaptcha(TunedModel):
	image_b64: str
	icon_locations: list
	icons_b64: list[str]

class UserFind(BaseModel):
	access_token: str

class UserLogin(BaseModel):
	username: str
	password: str

class UserCreate(BaseModel):
	nickname: str
	email: EmailStr
	password: str

	@validator('nickname')
	def validate_nickname(cls, value):
		if not LETTER_MATCH_PATTERN.match(value):
			raise HTTPException(status_code=422, detail='Name should contain only letters')
		return value
	
class UpdateUserRequest(BaseModel):
		nickname: Optional[constr(min_length=1)]
		email: Optional[EmailStr]

		@validator('nickname')
		def validate_nickname(cls, value):
			if not LETTER_MATCH_PATTERN.match(value):
				raise HTTPException(status_code=422, detail='Name should contain only letters')
			return value
		
class Token(BaseModel):
    access_token: str
    token_type: str